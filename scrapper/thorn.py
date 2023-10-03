#thorn.py


import requests
from bs4 import BeautifulSoup
import json
import os
from concurrent.futures import ThreadPoolExecutor
from cachetools import TTLCache
import sqlite3
from selenium import webdriver
from selenium.webdriver.common.by import By
import pdfplumber
from PIL import Image
import pytesseract
import cv2
import numpy as np

# Config
CACHE_TTL = 60 # 1 minute
MAX_THREADS = 10
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148'
]  

class Scraper:

    def __init__(self):
        self.session = requests.Session()
        self.cache = TTLCache(maxsize=100, ttl=CACHE_TTL)
        self.user_agents = USER_AGENTS

    def scrape(self, url):
        try:
            response = self.session.get(url, headers={
                'User-Agent': random.choice(self.user_agents)
            })
            content = response.text
        except Exception as e:
            print(e)
            return
        
        key = hashlib.sha1(url.encode('utf8')).hexdigest()
        self.cache[key] = content
        return content

    def scrape_html(self, url):
        html = self.scrape(url)
        if html:
            return BeautifulSoup(html, 'html.parser')

    def scrape_json(self, url):
        json_text = self.scrape(url)
        if json_text:
            return json.loads(json_text)

    def scrape_images(self, url, dest_folder):
        soup = self.scrape_html(url)
        img_tags = soup.find_all('img')

        os.makedirs(dest_folder, exist_ok=True)

        for tag in img_tags:
            img_url = tag['src']
            img_data = self.scrape(img_url)

            filename = os.path.join(dest_folder, os.path.basename(img_url))

            with open(filename, 'wb') as f:
                f.write(img_data)

        print(f"Images saved to {dest_folder}")

    def scrape_json_api(self, url, params=None):
        response = requests.get(url, params=params)
        data = response.json()

        if 'next' in response.links:
            next_url = response.links['next']['url']
            data.extend(self.scrape_json_api(next_url))

        return data
    
    def scrape_javascript(self, url):
        driver = webdriver.Chrome()
        driver.get(url)

        html = driver.page_source
        driver.close()

        return html

    def scrape_pdf(self, url):
        pdf_data = self.scrape(url)
        
        with pdfplumber.open(io.BytesIO(pdf_data)) as pdf:
            full_text = ''
            for page in pdf.pages:
                full_text += page.extract_text()
            return full_text

def scrape_graph(self, url):

  img_data = self.scrape(url)

  img = Image.open(io.BytesIO(img_data))  
  img = np.array(img)
  
  # Convert to grayscale
  img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
  
  # Apply threshold to make points white and background black
  ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV) 

  # Find contours in image
  contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

  data_points = []

  for c in contours:
    # Extract coordinate of centroid of each contour
    M = cv2.moments(c)
    if M["m00"] != 0:
      cX = int(M["m10"] / M["m00"])
      cY = int(M["m01"] / M["m00"])
      data_points.append((cX, cY))

  # Sort data points by x coordinate  
  data_points = sorted(data_points, key=lambda x: x[0]) 

  return data_points

scraper = Scraper()

# Scrape a normal HTML page
soup = scraper.scrape_html('http://example.com')

# Scrape a JSON API
data = scraper.scrape_json('http://api.example.com/data')

# Scrape and download images 
scraper.scrape_images('http://example.com/gallery', 'scraped_images')

# Scrape JavaScript rendered page
html = scraper.scrape_javascript('http://example.com')

# Extract text from a PDF file
text = scraper.scrape_pdf('http://example.com/doc.pdf')

# Extract data points from a chart image
data = scraper.scrape_graph('http://example.com/chart.png')
