import json
import time
import logging
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from instagrapi import Client
import sys
import re
import os


logging.basicConfig(
    filename='instagram_extractor.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class ExtractInstagramPosts:
    def __init__(self, driver, client):
        self.driver = driver
        self.client = client

    @staticmethod
    def init_driver(proxy=None):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        try:
            driver = webdriver.Chrome(options=options)
        except WebDriverException as e:
            logging.error(f"Error initializing WebDriver: {e}")
            sys.exit(1)
        return driver

    def get_post_details(self, url):
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, "//meta[@name='description']"))
                )
                meta_description = self.driver.find_element(By.XPATH, "//meta[@name='description']")
                description_content = meta_description.get_attribute('content')
                if not description_content:
                    raise ValueError("Meta description content is empty")
                
                likes = self.extract_likes(description_content)
                comments = self.extract_comments(description_content)
                article = self.extract_article(description_content)
                date = self.extract_date(description_content)
                description = self.extract_description(description_content)

                return {
                    'url': url,
                    'likes': likes,
                    'comments': comments,
                    'article': article,
                    'date': date,
                    'description': description,
                    'description_content': description_content
                }

            except TimeoutException:
                logging.warning(f"Timeout on attempt {attempt + 1} for URL: {url}")
                if attempt == max_retries - 1:
                    raise Exception(f"Page load timeout for {url}")
                time.sleep(5)  
            except Exception as e:
                logging.error(f"Error fetching post details for {url}: {e}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(5)

    def extract_likes(self, content):
        match = re.search(r'([\d,]+)\s+likes', content, re.IGNORECASE)
        if match:
            return match.group(1).replace(',', '')
        return None

    def extract_comments(self, content):
        match = re.search(r'([\d,]+)\s+comments', content, re.IGNORECASE)
        if match:
            return match.group(1).replace(',', '')
        return None

    def extract_article(self, content):
        match = re.search(r'-\s*([^\s]+)\s*on', content)
        if match:
            return match.group(1).strip()
        return None

    def extract_date(self, content):
        match = re.search(r'on\s+([A-Za-z]+\s+\d{1,2},\s+\d{4})', content)
        if match:
            return match.group(1).strip()
        return None

    def extract_description(self, content):
        match = re.search(r'"([^"]+)"', content)
        if match:
            return match.group(1).strip()
        return None

    def close(self):
        self.driver.quit()


def main():
    parser = argparse.ArgumentParser(description='Instagram Post Extractor')
    subparsers = parser.add_subparsers(dest='command', help='Sub-command help')

    login_parser = subparsers.add_parser('login', help='Login to Instagram')
    login_parser.add_argument('--username', required=True, help='Instagram username')
    login_parser.add_argument('--password', required=True, help='Instagram password')

    proxy_parser = subparsers.add_parser('proxy', help='Use proxy with WebDriver')
    proxy_parser.add_argument('--proxy', required=True, help='Proxy address (e.g., http://proxyserver:port)')

    parser.add_argument('--links', default='links.txt', help='Path to links file')
    parser.add_argument('--output', default='instagram_posts.json', help='Output JSON file')

    args = parser.parse_args()

    cl = Client()
    if args.command == 'login':
        try:
            cl.login(args.username, args.password)
            logging.info("Successfully logged in to Instagram!")
        except Exception as e:
            logging.error(f"Failed to login: {e}")
            sys.exit(1)

    proxy_value = None
    if args.command == 'proxy':
        proxy_value = args.proxy

    driver = ExtractInstagramPosts.init_driver(proxy=proxy_value)

    extractor = ExtractInstagramPosts(driver, cl)

    try:
        with open(args.links, 'r', encoding='utf-8') as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        logging.error(f"Links file not found: {args.links}")
        sys.exit(1)

    results = []

    for url in urls:
        logging.info(f'Processing: {url}')
        try:
            details = extractor.get_post_details(url)
            results.append(details)
        except Exception as e:
            logging.error(f"Error processing {url}: {e}")

    extractor.close()

    try:
    
        if os.path.exists(args.output):
            with open(args.output, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
        else:
            existing_data = []

        existing_data.extend(results)
        
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(existing_data, f, ensure_ascii=False, indent=4)

        logging.info(f'Data saved to {args.output}')

    except Exception as e:
        logging.error(f"Failed to save data: {e}")

if __name__ == '__main__':
    main()
