import re

import requests
from bs4 import BeautifulSoup


class LarodanCrawler:
    """
    A class to extract information from a webpage of Larodan.

    Attributes:
        url (str): The URL of the webpage to be parsed.
    """

    REGEX_FOR_QUANTITY = r"(?P<quantity_unit>\d+(?:\.\d+)?\s*(?:mg|g|ml|µg|µl|µmol|mmol|mg/ml|µg/ml|µmol/ml|mmol/ml|mg/g|µg/g|µmol/g|mmol/g))" # NOQA

    def __init__(self, url):
        """
        Initializes LarodanCrawler with the URL to be parsed.

        Args:
            url (str): The URL of the webpage.
        """
        self.url = url

    def extract_quantity_unit(self, text):
        """
        Extracts information from the given text.

        Args:
            text (str): The text from which information needs to be extracted.

        Returns:
            str: Extracted information.
        """
        match = re.search(self.REGEX_FOR_QUANTITY, text)
        if match:
            return match.group("quantity_unit")
        else:
            return None

    def get_cas_value(self, product_div):
        """
        Extracts the CAS value from the product_div.

        Args:
            product_div (BeautifulSoup element): The product_div containing information.

        Returns:
            str: CAS value.
        """
        cas = ""
        cas_number_span = product_div.find("span", text="CAS number: ")

        # Find the parent of the span element
        parent_element = cas_number_span.parent

        # Extract text from the parent element
        if parent_element:
            cas = parent_element.text.strip()
            patron = r'\bCAS number:\s*(\d+-\d+-\d+)\b'

            # Search the pattern in the text
            cas_regex = re.search(patron, cas)

            # If pattern found, return the result
            if cas_regex:
                cas = cas_regex.group(1)

        return cas

    def get_synonyms(self, soup_element):
        """
        Extracts synonyms from the soup_element.

        Args:
            soup_element (BeautifulSoup element): The element containing information.

        Returns:
            list: List of synonyms.
        """
        synonyms = []
        synonyms_element = soup_element.find("div", class_="product-prop product-prop-synonyms")

        # If the element is found, extract the text after the label "Synonyms:"
        if synonyms_element:
            synonyms_text = synonyms_element.text.strip().split(":")[-1]
            # Remove leading and trailing spaces from each synonym
            synonyms = [synonym.strip() for synonym in synonyms_text.split(",")]
        return synonyms

    def get_molecular(self, soup_element):
        """
        Extracts the molecular weight from the soup_element.

        Args:
            soup_element (BeautifulSoup element): The element containing information.

        Returns:
            str: Molecular weight.
        """
        molecular_weight = ""
        molecular_weight_span = soup_element.find("span", text="Molecular weight: ")

        # Find the parent of the span element
        parent_element = molecular_weight_span.parent

        # Extract text from the parent element
        if parent_element:
            molecular_weight = parent_element.text.strip()
            patron = r'\d+\.\d+'

            # Search the pattern in the text
            molecular_weight = re.search(patron, molecular_weight)

            # If pattern found, return the result
            if molecular_weight:
                molecular_weight = molecular_weight.group()

            return molecular_weight

    def get_packing(self, soup_element):
        """
        Extracts packaging information from the soup_element.

        Args:
            soup_element (BeautifulSoup element): The element containing information.

        Returns:
            dict: Packaging information.
        """
        packaging = {}

        variations_table = soup_element.find("table", class_="product-variations-table")

        if variations_table:
            # Find all the rows in the table
            rows = variations_table.find_all('tr')

            for row in rows:
                # Get the cells of the row
                cells = row.find_all('td')
                if len(cells) == 3:  # Asegura que la fila tenga las 3 celdas
                    product_description = cells[1].get_text(strip=True)
                    product_description = self.extract_quantity_unit(product_description)
                    price = cells[2].get_text(strip=True)
                    packaging[product_description] = price

        return packaging

    def get_image_product(self, soup_element):
        """
        Extracts the image link from the soup_element.

        Args:
            soup_element (BeautifulSoup element): The element containing information.

        Returns:
            str: Image link.
        """
        image_link = ""
        # Find the element with class "prod-structure"
        prod_structure = soup_element.find("div", class_="prod-structure")

        # If found, extract the image source attribute
        if prod_structure:
            image_element = prod_structure.find("img")
            if image_element:
                image_link = image_element["src"]

        return image_link

    def get_smiles(self, soup_element):
        """
        Extracts SMILES information from the soup_element.

        Args:
            soup_element (BeautifulSoup element): The element containing information.

        Returns:
            str: SMILES information.
        """
        smiles = ""
        try:
            smiles_element = soup_element.find(
                "div", class_="product-prop-wrap"
            ).find("span", class_="prop-label", text="Smiles: ")
        except Exception:
            smiles_element = ""

        # Extract SMILES
        if smiles_element:
            smiles = smiles_element.next_sibling.strip()

        return smiles

    def get_description(self, soup_element):
        """
        Extracts the description from the soup_element.

        Args:
            soup_element (BeautifulSoup element): The element containing information.

        Returns:
            str: Description text.
        """
        description = ""
        # Select the element with the class "product-description"
        description_element = soup_element.find("div", class_="product-description")

        # Extract the text of the description
        if description_element:
            description = description_element.text.strip()

        return description

    def get_msds_link(self, soup_element):
        """
        Extracts the MSDS link from the soup_element.

        Args:
            soup_element (BeautifulSoup element): The element containing information.

        Returns:
            str: MSDS download link.
        """
        download_link = ""
        # Select the 'a' element with the text "Download"
        download_element = soup_element.find("a", text="Download")

        # Extract the download link
        if download_element:
            download_link = download_element["href"]

        return download_link

    def get_product_data(self):
        """
        Retrieves product data from the URL.

        Returns:
            dict: A dictionary containing product data.
        """
        # Send a GET request to the URL
        response = requests.get(self.url)
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        # Find all product elements with class 'type-product'
        product_html_body = soup.find_all(class_='type-product')
        for product in product_html_body:
            # Extract product name
            name = product.find('h1').text
            # Extract product SKU
            sku = product.find("span", class_="sku").text.strip()

        # Construct product data dictionary
        product_data = {
            "id": sku,
            "url": self.url,
            "name": name,
            "CAS": self.get_cas_value(soup),
            "synonyms": self.get_synonyms(soup),
            "molecular_weight": self.get_molecular(soup),
            "packaging": self.get_packing(soup),
            "img": self.get_image_product(soup),
            "description": self.get_description(soup),
            "smiles": self.get_smiles(soup),
            "pdf_msds": self.get_msds_link(soup)
        }
        return product_data
