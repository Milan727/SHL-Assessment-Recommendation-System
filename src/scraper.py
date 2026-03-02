import os
import json
import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
from playwright_stealth import Stealth

BASE_URL = "https://www.shl.com"
CATALOG_PATH = "/solutions/products/product-catalog/"

# The specific test types identified during exploration
TYPE_MAPPING = {
    1: "Knowledge & Skills (K) / Technical",
    2: "Personality & Behavior (P) / Soft Skills"
}

def fetch_page_html(url, timeout=60000):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        Stealth().apply_stealth_sync(page)
        print(f"Fetching: {url}")
        
        try:
            page.goto(url, timeout=timeout)
            page.wait_for_timeout(3000) # Let React/Vue render
            html = page.content()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            html = ""
        finally:
            browser.close()
            
        return html

def parse_products(html, test_type_label):
    soup = BeautifulSoup(html, 'html.parser')
    products = []
    
    # SHL catalog items are typically anchors linking to their view pages
    for a in soup.find_all('a'):
        href = a.get('href', '')
        if '/product-catalog/view/' in href and not href.endswith('/view/'):
            title = a.text.strip()
            if title and not any(p['title'] == title for p in products):
                products.append({
                    "title": title,
                    "url": BASE_URL + href if href.startswith('/') else href,
                    "test_type": test_type_label
                })
                
    return products

def scrape_catalog(test_mode=False):
    all_products = []
    
    for category_id, test_type_label in TYPE_MAPPING.items():
        start = 0
        limit = 60 if test_mode else 120 # fetch 5-10 pages max for time constraints
        
        while start <= limit:
            url = f"{BASE_URL}{CATALOG_PATH}?start={start}&type={category_id}"
            html = fetch_page_html(url)
            
            if not html:
                break
                
            page_products = parse_products(html, test_type_label)
            if not page_products:
                print(f"No products found on start={start}. Moving to next category.")
                break
                
            all_products.extend(page_products)
            print(f"Found {len(page_products)} products. Total so far: {len(all_products)}")
            
            if test_mode:
                break
                
            start += 12
            
    # Deduplicate and combine test types
    unique_products_dict = {}
    for p in all_products:
        url = p['url']
        if url in unique_products_dict:
            # If it already exists, combine the test_type strings if not already in there
            if p['test_type'] not in unique_products_dict[url]['test_type']:
                unique_products_dict[url]['test_type'] += f", {p['test_type']}"
        else:
            unique_products_dict[url] = p
            
    unique_products = list(unique_products_dict.values())
    
    os.makedirs('data', exist_ok=True)
    with open('data/shl_catalog.json', 'w') as f:
        json.dump(list(unique_products), f, indent=2)
        
    print(f"Successfully saved {len(unique_products)} unique assessments to data/shl_catalog.json")
    return unique_products

if __name__ == "__main__":
    scrape_catalog(test_mode=False)
