import util
from selectorlib import Extractor
from Common import Product
from Common.Product.product import dump_to_json
import json
import time


TESTABLE_LINKS = list()
valid_categories = util.from_config_categories_to_scrape()
url_valid_categories = [util.get_link_to_category(x) for x in valid_categories]

selector_file = util.SelectorTypeENUM.SELECTOR_PRODUCT.filter
e = Extractor.from_yaml_file(selector_file)


for category in valid_categories:
    url_category = util.get_link_to_category(category)
    urls_products = util.pull_urls_from_category_frontpage(url_category)
    urls_products = [x.split('/ref')[0] for x in urls_products]
    urls_products = [util.get_absolute_amazon_url(url) for url in urls_products]

    t_start = time.time()
    try:
        dump_to_json(category,urls_products)
    except Exception as e:
        print(f'Failed Category: {category}')
        print(e)
        raise e
            
        if (time.time() - t_start) > 30:
            break
"""
# 1. Prepartion: Read configuration file to determine which bestseller categories should be looked at

# 2. Retrieve URLs: Pull all Product links from the front page listings
# 3. Pull Product Data: For each of the urls, retrieve the product data
"""

