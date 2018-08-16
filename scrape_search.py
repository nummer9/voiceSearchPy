from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib import parse 
import json
import argparse

class Product:
    def __init__(self, article_nr, name, price, image_url):
        self.article_nr = article_nr
        self.name = name
        self.price = price
        self.image_url = image_url

    def __str__(self):
        return "[article-number: {}, name: {}]".format(
            self.article_nr, self.name)

def fetch_html(text):
    search_url = "https://www.otto.de/suche/" + parse.quote_plus(text)
    uClient = uReq(search_url)
    html = uClient.read()
    uClient.close()
    return html

def parse_html_to_json(html):
    page_soup = soup(html, "html.parser")
    article_containers = page_soup.find_all("article", {"class":"product"})

    json_array = "["
    i = 0

    for container in article_containers:
        try:
            json_str = container.script.encode_contents().decode("utf-8").strip()
        except:
            pass
        else:
            json_array = append_json_to_array(i, json_array, json_str)
            i += 1
    
    return json_array + "]"

def append_json_to_array(i, json_array, json_str):
    if i == 0:
        json_array += json_str
    else:
        json_array = json_array + "," + json_str
    return json_array

def search_products(text):
    """performs a search of the prodived text and returns a maximum of 4 produts of type Product."""
    html = fetch_html(text)
    json_array = parse_html_to_json(html)
    products_json = json.loads(json_array)

    products = []

    for product_json in products_json:
        variations = product_json['product']['variationMap'].values()
        data = list(variations)[0]

        product = Product(
            data['articleNumber'], 
            data['name'], 
            data['formattedRetailPrice'],
            data['imageUrl']
            )
        products.append(product)

    return products

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("search", help='search for a string, encapsulate multiple words in quotation marks')
    args = parser.parse_args()

    products = search_products(args.search)
    for p in products:
        print(p)