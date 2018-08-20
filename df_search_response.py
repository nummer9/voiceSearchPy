from product import Product
import json
from typing import List
from df_helper import make_card_response_from_product
import logging

def make_search_response(products:list, session):
    """Makes a Dialogflow Response for search intents."""

    if len(products) == 0:
        logging.warning('no products found')

        # TODO: no article found response!
        return make_no_products_response()
    else:
        product = products[0]
        parameters = make_parameters(products)

    return make_card_response_from_product(session, product, parameters)  

def make_parameters(products:List[Product]) -> dict:
    prods = []

    for prod in products:
        prod = {
            "name": prod.name,
            "price": prod.price,
            "image": prod.image_url,
            "article-number": prod.article_nr,
            "url": prod.url
        }
        prods.append(prod)

    parameters = {
        "current-index" : 0,
        "products": prods
    }

    return parameters

def make_no_products_response():
    resp_items = [
        {
            "simpleResponse": {
                "textToSpeech": "Dieses Produkt konnte ich nicht auf otto D E finden!",
                "displayText": "Keine Produkte gefunden"
            }
        }
    ]

    resp_payload = {
        "google": {
            "expectUserResponse": True,
            "richResponse": {
                "items": resp_items,
            }
        }
    }

    response = {
        "source": "Otto Voice Search",
        "payload": resp_payload,
    }

    return json.dumps(response, ensure_ascii=False).encode('utf8')