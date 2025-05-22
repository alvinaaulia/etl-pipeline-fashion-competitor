import unittest
from unittest.mock import patch, Mock
from utils.extract import parse_price, parse_rating, parse_colors, scrape_page, extract_all_products
import re

class TestExtractFunctions(unittest.TestCase):

    def test_parse_price_valid(self):
        self.assertEqual(parse_price("Rp 1.250.000"), 1250000.0)
        self.assertEqual(parse_price("1.000"), 1000.0)

    def test_parse_price_invalid(self):
        self.assertIsNone(parse_price(""))
        self.assertIsNone(parse_price(None))
        self.assertIsNone(parse_price("N/A"))

    def test_parse_rating(self):
        self.assertEqual(parse_rating("Rating: 4.8 / 5"), 4.8)
        self.assertEqual(parse_rating("4.0 out of 5"), 4.0)
        self.assertIsNone(parse_rating("No rating"))

    def test_parse_colors(self):
        self.assertEqual(parse_colors("Colors: 5 options"), 5)
        self.assertIsNone(parse_colors("Colors: N/A"))

    @patch("utils.extract.requests.get")
    def test_scrape_page_success(self, mock_get):
        html = '''
        <div class="collection-card">
            <div class="product-details">
                <div class="product-title">Cool Jacket</div>
                <div class="price">Rp 500.000</div>
                <p>Rating: 4.5</p>
                <p>Colors: 3</p>
                <p>Size: M</p>
                <p>Gender: Unisex</p>
            </div>
        </div>
        '''
        mock_response = Mock(status_code=200, text=html)
        mock_get.return_value = mock_response

        products = scrape_page(1)
        self.assertEqual(len(products), 1)
        product = products[0]
        self.assertEqual(product["Title"], "Cool Jacket")
        self.assertEqual(product["Price"], 500000.0)
        self.assertEqual(product["Rating"], 4.5)
        self.assertEqual(product["Colors"], 3)
        self.assertEqual(product["Size"], "M")
        self.assertEqual(product["Gender"], "Unisex")

    @patch("utils.extract.requests.get")
    def test_scrape_page_fail(self, mock_get):
        mock_get.return_value = Mock(status_code=404)
        products = scrape_page(99)
        self.assertEqual(products, [])

    @patch("utils.extract.scrape_page")
    def test_extract_all_products(self, mock_scrape):
        mock_scrape.side_effect = [
            [{"Title": "Item A", "Price": 100.0, "Rating": 4.5, "Colors": 3, "Size": "M", "Gender": "Unisex", "timestamp": "2025-01-01T00:00:00Z"}],
            [{"Title": "Item B", "Price": 200.0, "Rating": 4.8, "Colors": 2, "Size": "L", "Gender": "Male", "timestamp": "2025-01-01T00:00:00Z"}],
            []
        ]
        df = extract_all_products(max_pages=3)
        self.assertEqual(len(df), 2)
        self.assertIn("Title", df.columns)
        self.assertIn("Price", df.columns)

if __name__ == "__main__":
    unittest.main()
