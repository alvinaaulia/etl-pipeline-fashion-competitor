# main.py
from utils.extract import extract_all_products
from utils.transform import transform_data
from utils.load import save_to_csv, save_to_google_sheets, store_to_postgre

def run_etl_pipeline():
    raw_df = extract_all_products(max_pages=50)
    
    clean_df = transform_data(raw_df)
    
    save_to_csv(clean_df)
    save_to_google_sheets(clean_df)
    store_to_postgre(clean_df, "postgresql://developer:supersecretpassword@localhost:5432/etl_pipeline")
    
    print(f"ETL complete. Initial: {len(raw_df)} | Clean: {len(clean_df)}")

if __name__ == "__main__":
    run_etl_pipeline()