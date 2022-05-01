import requests
from bs4 import BeautifulSoup

url_best_sellers_main = "https://www.amazon.com/bestsellers"
html_sidebar_class_name = '_p13n-zg-nav-tree-all_style_zg-browse-item__1rdKf _p13n-zg-nav-tree-all_style_zg-browse-height-small__nleKL'


html = requests.get(url_best_sellers_main).content
soup = BeautifulSoup(html, 'html5lib')
best_seller_categories = soup.find_all('div', class_=html_sidebar_class_name)
for category in best_seller_categories:
    for _ in category.findAll('a', href=True):
        print(_['href'])


bsdict =pull_all_bestseller_categories(True)
list_bsnames=list(bsdict.keys())
list_bsnames = [x.replace(' ','') for x in list_bsnames]
list_bsnames = [x.replace(',','') for x in list_bsnames]
list_bsnames = [x.replace('&','_') for x in list_bsnames]
list_bsnames = [x.upper() for x in list_bsnames]