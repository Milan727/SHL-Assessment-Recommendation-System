from playwright.sync_api import sync_playwright
import time

def explore():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=["--disable-blink-features=AutomationControlled"])
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
        page = context.new_page()
        
        print("Navigating to SHL Catalog with custom UA...")
        page.goto("https://www.shl.com/solutions/products/product-catalog/", timeout=60000)
        print("Waiting for network idle...")
        time.sleep(5)
        
        content = page.content()
        with open("/tmp/shl_dump2.html", "w", encoding="utf-8") as f:
            f.write(content)
            
        print("Dumped HTML to /tmp/shl_dump2.html")
        browser.close()

if __name__ == "__main__":
    explore()
