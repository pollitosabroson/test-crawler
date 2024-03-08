import requests
from bs4 import BeautifulSoup


class Lister:
    """
    A class to extract product URLs from a webpage.

    Attributes:
        url (str): The URL of the webpage to be parsed.
    """
    def __init__(self, url):
        """
        Initializes Lister with the URL to be parsed.

        Args:
            url (str): The URL of the webpage.
        """
        self.url = url

    def get_product_urls(self):
        """
        Retrieves product URLs from the webpage.

        Returns:
            list: A list containing product URLs.
        """
        product_urls = []
        page_number = 1
        while True:
            page_url = f"{self.url}page/{page_number}/"
            # Send a GET request to the page URL
            response = requests.get(page_url)
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            try:
                # Find all product links within the table body
                products = soup.find('tbody').find_all('a')
            except Exception:
                # If no products found, set products to an empty list
                products = []

            # If no products found, exit the loop
            if not products:
                break

            # Extract the URL of each product and add it to the product_urls list
            for product in products:
                product_url = product["href"]
                product_urls.append(product_url)

            # Increment the page number for the next iteration
            page_number += 1

        return product_urls
