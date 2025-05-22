import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone
import pandas as pd

# def parse_price(price_str):
#     if not price_str:
#         return None
#     price_num = ''.join(ch for ch in price_str if ch.isdigit() or ch == '.')
#     try:
#         return float(price_num)
#     except:
#         return None

def parse_price(price_str):
    if not price_str:
        return None
    cleaned = ''.join(ch for ch in price_str if ch.isdigit())
    try:
        return float(cleaned)
    except:
        return None

def parse_rating(rating_str):
    import re
    match = re.search(r'(\d+(\.\d+)?)', str(rating_str))
    return float(match.group(1)) if match else None

def parse_colors(colors_str):
    import re
    match = re.search(r'(\d+)', str(colors_str))
    return int(match.group(1)) if match else None

def scrape_page(page_num=1):
    try:
        if page_num == 1:
            url = "https://fashion-studio.dicoding.dev/"
        else:
            url = f"https://fashion-studio.dicoding.dev/page{page_num}"

        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"❌ Failed to retrieve page {page_num}, status code: {response.status_code}")
            return []
            
        soup = BeautifulSoup(response.text, 'html.parser')
        products = []
        
        for card in soup.select('div.collection-card'):
            details = card.select_one('div.product-details')
            if not details:
                continue

            title = details.select_one('.product-title')
            price_raw = details.select_one('.price')

            product = {
                "Title": title.text.strip(),
                "Price": parse_price(price_raw.text.strip()) if price_raw else None,
                "Rating": None,
                "Colors": None,
                "Size": None,
                "Gender": None,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }

            for p in details.find_all('p'):
                text = p.text.strip()
                if "Rating" in text:
                    product['Rating'] = parse_rating(text)
                elif "Colors" in text:
                    product['Colors'] = parse_colors(text)
                elif text.startswith("Size:"):
                    product['Size'] = text.replace("Size:", "").strip()
                elif text.startswith("Gender:"):
                    product['Gender'] = text.replace("Gender:", "").strip()

            if all(product.values()):
                products.append(product)

        return products

    except Exception as e:
        print(f"❌ Error scraping page {page_num}: {e}")
        return []

def extract_all_products(max_pages=50):
    print("Scraping product data from all pages..")
    all_products = []
    
    for page in range(1, max_pages + 1):
        products = scrape_page(page)
        if not products: 
            break
        all_products.extend(products)
        print(f"Page {page}: {len(products)} products found")
    
    df = pd.DataFrame(all_products)
    print(f"✅ Total {len(df)} products extracted")
    return df