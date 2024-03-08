import argparse
import json
from concurrent.futures import ThreadPoolExecutor

from larodan_parse import LarodanCrawler
from listener import Lister


def main():
    """
    Main function to execute Lister and Crawler script.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Lister and Crawler script')
    parser.add_argument('url', type=str, help='URL to crawl')
    parser.add_argument(
        '-c', '--concurrency',
        type=int, default=1,
        help='Number of parallel crawlers'
    )
    # Parse command-line arguments
    args = parser.parse_args()

    # Instantiate Lister with the provided URL
    lister = Lister(args.url)
    # Retrieve product URLs from the webpage
    product_urls = lister.get_product_urls()

    # Create ThreadPoolExecutor with specified concurrency
    with ThreadPoolExecutor(max_workers=args.concurrency) as executor:
        # Execute LarodanCrawler on each product URL in parallel
        results = list(executor.map(LarodanCrawler, product_urls))

    # Extract product data from crawler results
    product_data_list = [result.get_product_data() for result in results]

    # Write product data to a JSON file
    with open('products.json', 'w') as f:
        json.dump(product_data_list, f, indent=4)


if __name__ == "__main__":
    main()
