from product import Product
import json
from typing import List

def make_search_response(products:list, session):

    product = products[0]

    resp_items = [
        {
            "simpleResponse": {
                "textToSpeech": make_text_to_speech(product),
                "displayText": f'{product.name} - {product.price} EUR'
            }
        }, {
            "basicCard": {
                "title": f'{product.name} - {product.price} EUR',
                "image": {
                    "url": product.image_url,
                    "accessibilityText": "keine Vorschau"
                }
            }
        }
    ]

    resp_payload = {
        "google": {
            "expectUserResponse": True,
            "richResponse": {
                "items": resp_items,
                "suggestions": [
                    {
                        "title": "nächster Treffer"
                    }
                ]
            }
        }
    }

    resp_out_contexts = [
        {
            "name": f'{session}/contexts/next_result',
            "lifespanCount": 3,
            "parameters": make_parameters(products)
        }
    ]

    response = {
        "source": "Otto Voice Search",
        "payload": resp_payload,
        "outputContexts": resp_out_contexts
    }

    return json.dumps(response, ensure_ascii=False).encode('utf8')

def make_text_to_speech(product:Product) -> str:
    return f'<speak>Gefunden auf otto DE: {product.name}. Der Artikel kostet {product.price} Euro</speak>'

def make_parameters(products:List[Product]) -> dict:
    prods = []

    for prod in products:
        prod = {
            "name": prod.name,
            "price": prod.price,
            "image": prod.image_url,
            "article-number": prod.article_nr
        }
        prods.append(prod)

    parameters = {
        "current-index" : 0,
        "products": prods
    }

    return parameters