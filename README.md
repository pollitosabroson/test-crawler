# Lister and Crawler Script

This script is designed to crawl a webpage, extract product URLs, and fetch product details in parallel using multiple crawler instances. It provides options to specify the URL to be crawled and the concurrency level for parallel crawling.

## Requirements

- Python 3.x
- `requests` library
- `BeautifulSoup` library
- `concurrent.futures` module

## Usage

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/lister-crawler.git
    ```

2. Navigate to the project directory:

    ```bash
    cd lister-crawler
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the script:

    ```bash
    python crawler.py <url> [-c <concurrency>]
    ```

    Replace `<url>` with the URL of the webpage to be crawled. Optionally, you can specify the concurrency level with the `-c` or `--concurrency` flag. If not specified, the default concurrency level is 1.

5. After execution, the script will generate a `products.json` file containing the fetched product data.

## Example

```bash
python crawler.py https://example.com -c 5
```
This command will crawl the webpage at https://example.com with a concurrency level of 5.
