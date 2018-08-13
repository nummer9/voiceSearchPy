"""local usage"""

from flask import Flask, request
from scrape_search import search_products, Product

webhook = Flask(__name__)

@webhook.route("/")
def main():
    return "use /search?text=* to search for products."

@webhook.route("/search")
def search():
    text = request.args.get("text")
    products = search_products(text)

    answer = ""
    for p in products:
        answer += p.__str__()
    return "articles {}".format(answer)

if __name__ == "__main__":
    webhook.run(debug=True, host="0.0.0.0", port=8080)