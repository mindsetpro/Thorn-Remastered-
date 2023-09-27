# thorn.py

import requests
from bs4 import BeautifulSoup
import json

class Thorn:
    def __init__(self):
        self.session = requests.Session()

    def scrape_html(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            # Extract and return HTML data
            return soup.prettify()
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def scrape_json(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            json_data = response.json()
            return json_data
        except (requests.exceptions.RequestException, json.JSONDecodeError) as e:
            print(f"Error: {e}")
            return None

    def scrape_css(self, url):
        try:
            response = self.session.get(url)
            response.raise_for_status()
            # Extract and return CSS content
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def scrape_python(self, code_url):
        try:
            response = self.session.get(code_url)
            response.raise_for_status()
            # Extract and return Python code content
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None

    def scrape_user_choice(self):
        url = input("Enter the URL you want to scrape: ")
        content_type = input("Enter the content type to scrape (html/json/css/python): ").lower()

        if content_type == "html":
            result = self.scrape_html(url)
        elif content_type == "json":
            result = self.scrape_json(url)
        elif content_type == "css":
            result = self.scrape_css(url)
        elif content_type == "python":
            result = self.scrape_python(url)
        else:
            print("Invalid content type. Supported types: html/json/css/python")
            return

        if result is not None:
            print(result)

# Usage example
if __name__ == "__main__":
    thorn = Thorn()
    thorn.scrape_user_choice()
