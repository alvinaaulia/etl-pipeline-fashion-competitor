import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from sqlalchemy import create_engine
import numpy as np

def validate_data(df):
    if df.empty:
        raise ValueError("No valid data to save")
        
    required_columns = ['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Missing required columns: {required_columns}")
    
    if df['Title'].isin(['Unknown Product', None]).any():
        raise ValueError("Invalid product titles found")
    
    return df

def save_to_csv(df, filepath='products.csv'):
    try:
        df = validate_data(df)
        df.to_csv(filepath, index=False)
        print(f"✅ Saved {len(df)} records to {filepath}")
    except Exception as e:
        print(f"❌ CSV Save Error: {e}")

def save_to_google_sheets(df, creds_path='etl-fashion-460408-6eb71c372cbb.json', sheet_name='Fashion Competitors'):
    try:
        df = validate_data(df)
        
        scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
        creds = Credentials.from_service_account_file(creds_path, scopes=scopes)
        client = gspread.authorize(creds)

        spreadsheet = client.open(sheet_name) if sheet_name in [s.title for s in client.openall()] else client.create(sheet_name)
        spreadsheet.share(None, perm_type='anyone', role='reader')
        
        sheet = spreadsheet.sheet1
        sheet.clear()
        
        df['timestamp'] = df['timestamp'].dt.strftime('%Y-%m-%d %H:%M:%S')
        data = [df.columns.tolist()] + df.astype(str).values.tolist()
        
        sheet.update(data, value_input_option='USER_ENTERED')
        print(f"✅ Uploaded {len(df)} records to Google Sheets")
        print(f"🔗 Spreadsheet URL: {spreadsheet.url}")
        
    except Exception as e:
        print(f"❌ Google Sheets Error: {e}")

def store_to_postgre(df, db_url):
    try:
        df = validate_data(df)
        
        engine = create_engine(db_url)
        with engine.connect() as conn:
            df.to_sql('products', conn, if_exists='append', index=False)
            print(f"✅ Stored {len(df)} records to PostgreSQL")
            
    except Exception as e:
        print(f"❌ Database Error: {e}")