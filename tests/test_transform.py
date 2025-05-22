import unittest
import pandas as pd
from utils.transform import transform_data

class TestTransform(unittest.TestCase):
    def setUp(self):
        self.raw_data = pd.DataFrame({
            'Title': ['T-shirt', 'Unknown Product', 'Jacket'],
            'Price': ['100', '200', 'Price Unavailable'],
            'Rating': ['4.5', 'Invalid Rating', '3.0'],
            'Colors': ['3 Colors', 'Colors N/A', '2 Colors'],
            'Size': ['Size: M', 'Size: L', 'Size: S'],
            'Gender': ['Gender: Men', 'Gender: Women', 'Gender: Unisex'],
            'timestamp': ['2025-05-20T12:00:00Z']*3
        })

    def test_transform_data(self):
        df_clean = transform_data(self.raw_data)
        self.assertFalse(df_clean.empty)
        self.assertTrue(all(df_clean['Title'] != 'Unknown Product'))
        self.assertTrue(all(df_clean['Price'] > 0))
        self.assertTrue(df_clean['Rating'].dtype == float)
        self.assertTrue(pd.api.types.is_numeric_dtype(df_clean['Colors']))
        self.assertTrue(all(df_clean['Size'].apply(lambda x: isinstance(x, str))))
        self.assertTrue(all(df_clean['Gender'].apply(lambda x: isinstance(x, str))))

if __name__ == '__main__':
    unittest.main()
