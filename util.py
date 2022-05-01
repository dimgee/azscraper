from selectorlib import Extractor
import requests
from typing import List
from pathlib import Path
import json
from bs4 import BeautifulSoup, Tag
from enum import Enum
from typing import NamedTuple
from Common import CONFIG
from Common.Data.categories_map import CATEGORIES2URLMAP
# from scrapy.selector import Selector
# from scrapy.http import HtmlResponse
import requests
from bs4 import BeautifulSoup

from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium import webdriver
from selenium.webdriver.common.by import By

from Input import PATH_INPUT
from Output import PATH_OUTPUT
from Common.Product import PATH_PRODUCT
from Common.Listing import PATH_LISTING


class BlockedByServerError(BaseException):
    """ Raised if expected Input not received from server """

    def __init__(self):
        pass


class SelectorTypeENUM(Enum):
    SELECTOR_LISTING = PATH_LISTING / "filter_listing.yml"
    SELECTOR_PRODUCT =  PATH_PRODUCT / "filter_product.yml"

    @property
    def filter(self):
        return str(self.value)

HEADER = {
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-user': '?1',
    'sec-fetch-dest': 'document',
    'referer': 'https://www.amazon.com/',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}

# Data Section -- Queries amazon for information to be used in other functions
def _pull_all_bestseller_categories(full_url=True):
    """
    Iterates through all bestseller categories on main Best Seller page; returns a dictionary containing the category
    name and URL.
    :param full_url: If true (default), dictionary returns absolute URL to category's web page
    :return: dictionary of {category_name: category_link}
    """

    html = requests.get(CONFIG['amazon_web']["url_best_sellers"]).content
    soup = BeautifulSoup(html, 'html5lib')
    best_seller_categories: List[Tag] = soup.find_all('div', class_=CONFIG['amazon_web']['html_class_sidebar_categories'])

    bestseller_dict = {}
    for category in best_seller_categories:
        for match in category.findAll('a', href=True):
            category_name = category.getText()
            category_link = (match['href'])

            if full_url:
                category_link = get_absolute_amazon_url(category_link)

            bestseller_dict.update({category_name: category_link})
    return bestseller_dict

def pull_urls_from_category_frontpage(url_category_page):
    driver = configure_firefox_driver()
    driver.get(url_category_page)
    wp = BeautifulSoup(driver.page_source, features="lxml")

    filter_ahrefs = wp.find_all('a', href=True)
    html_blocks = [_.span for _ in filter_ahrefs if ("$" in str(_))]
    url_list = list()
    for block in html_blocks:
        try:
            relative_url = block.parent.get('href')
            print(relative_url)
            url_list.append(relative_url)
        except AttributeError:
            pass
    return url_list


# Configuration Section -- Sets up program to run based on configuration setup
def from_config_categories_to_scrape() -> list:
    valid_categories = CONFIG['valid_categories']._options()
    to_scrape = [x for x in valid_categories if CONFIG['valid_categories'][x] == 'True']
    print(f"Scraping Categories: {to_scrape}")
    return to_scrape

def get_link_to_category(valid_category):
    return CATEGORIES2URLMAP.get(valid_category)

# configure Firefox Driver
def configure_firefox_driver() -> webdriver.Firefox:
    firefox_options = FirefoxOptions()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    return driver

# Parsing Section -- Parses html data retrieved from amazon

def get_absolute_amazon_url(relative_url:str, base_url="https://www.amazon.com") -> str:
    return ''.join([base_url, relative_url])

def scrape_product(product_url, selector=SelectorTypeENUM.SELECTOR_PRODUCT):
    Extractor.from_yaml_file(selector.filter)
    rsp = requests.get(product_url, headers=HEADER)
    status_code = rsp.status_code

    if status_code >= 500:
        raise BlockedByServerError

def scrape(url, extractor):
    # Download the page using requests
    e = Extractor
    d = configure_firefox_driver()

    print("Downloading %s"%url)
    try:
        d.get(url)
        return e.extract(d.page_source)
    except:
        print('Error')

    # Simple check to check if page was blocked (Usually 503)
        # Pass the HTML of the page and create
