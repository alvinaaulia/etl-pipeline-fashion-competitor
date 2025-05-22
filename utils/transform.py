import pandas as pd
import numpy as np
from datetime import datetime

DIRTY_PATTERNS = {
    "Title": ["Unknown Product", None, ""],
    "Rating": ["Invalid Rating", "Not Rated", None],
    "Price": ["Price Unavailable", None, 0],
    "Colors": ["Colors N/A", None, 0]
}

def transform_data(df):
    if df.empty:
        return df

    df = df.copy()

    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    df = df[df['Price'].notna() & (df['Price'] > 0)]
    df['Price'] *= 16000

    def clean_rating(x):
        if pd.isna(x):
            return np.nan
        try:
            if isinstance(x, str) and '/' in x:
                x = x.split('/')[0].strip()
            x = float(x)
            return x if 0 <= x <= 5 else np.nan
        except:
            return np.nan

    df['Rating'] = df['Rating'].apply(clean_rating)
    df = df[df['Rating'].notna()]

    df['Colors'] = df['Colors'].astype(str).str.extract(r'(\d+)')[0]
    df['Colors'] = pd.to_numeric(df['Colors'], errors='coerce')
    df = df[df['Colors'].notna() & (df['Colors'] > 0)]

    df['Size'] = df['Size'].astype(str).str.replace('Size:', '').str.strip()
    df['Gender'] = df['Gender'].astype(str).str.replace('Gender:', '').str.strip()

    DIRTY_PATTERNS = {
        "Title": ["Unknown Product", None, ""],
        "Rating": [None],
        "Price": [None, 0],
        "Colors": [None, 0]
    }

    for col, patterns in DIRTY_PATTERNS.items():
        df = df[~df[col].isin(patterns)]

    df = df[df['Size'].astype(str).str.len() > 0]
    df = df[df['Gender'].astype(str).str.len() > 0]

    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df[df['timestamp'].notna()]

    df = df.drop_duplicates(
        subset=['Title', 'Price', 'Rating', 'Colors', 'Size', 'Gender'],
        keep='first'
    )
    df = df.reset_index(drop=True)

    print(f"✅ Final clean records: {len(df)}")
    return df
