import argparse
from scraper import scrape_catalog

def main():
    parser = argparse.ArgumentParser(description="Run SHL Web Scraper")
    parser.add_argument("--test-mode", action="store_true", help="Run in test mode (scrapes fewer pages for speed)")
    args = parser.parse_args()
    
    print("=== Starting SHL Product Catalog Scraper ===")
    print(f"Mode: {'Test (Fast)' if args.test_mode else 'Full Extraction'}")
    scrape_catalog(test_mode=args.test_mode)
    print("=== Scraping Complete ===")

if __name__ == "__main__":
    main()
