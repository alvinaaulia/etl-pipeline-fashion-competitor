import unittest
import pandas as pd
from unittest.mock import patch, MagicMock
from utils.load import save_to_csv, save_to_google_sheets, store_to_postgre

class TestLoad(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({
            'Title': ['T-shirt'],
            'Price': [160000],
            'Rating': [4.5],
            'Colors': [3],
            'Size': ['M'],
            'Gender': ['Men'],
            'timestamp': pd.to_datetime(['2025-05-20 12:00:00'])
        })

    def test_save_to_csv(self):
        save_to_csv(self.df, filepath='test_products.csv')
        with open('test_products.csv', 'r') as f:
            content = f.read()
        self.assertIn('T-shirt', content)

    @patch('utils.load.gspread.authorize')
    @patch('utils.load.Credentials.from_service_account_file')
    def test_save_to_google_sheets(self, mock_creds, mock_authorize):
        mock_client = MagicMock()
        mock_spreadsheet = MagicMock()
        mock_client.openall.return_value = [mock_spreadsheet]
        mock_client.open.return_value = mock_spreadsheet
        mock_spreadsheet.title = 'Fashion Competitors'
        mock_spreadsheet.sheet1 = MagicMock()
        mock_spreadsheet.url = 'https://fakeurl'
        mock_authorize.return_value = mock_client
        mock_creds.return_value = MagicMock()

        save_to_google_sheets(self.df, creds_path='dummy.json', sheet_name='Fashion Competitors')
        mock_client.open.assert_called()
        mock_spreadsheet.sheet1.update.assert_called()

    @patch('utils.load.create_engine')
    def test_store_to_postgre(self, mock_create_engine):
        mock_engine = MagicMock()
        mock_conn = MagicMock()
        mock_create_engine.return_value = mock_engine
        mock_engine.connect.return_value.__enter__.return_value = mock_conn

        store_to_postgre(self.df, db_url='postgresql://developer:supersecretpassword@localhost:5432/etl_pipeline')
        mock_conn.execute.assert_not_called() 

if __name__ == '__main__':
    unittest.main()
