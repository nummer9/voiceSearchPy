from scrape_search import search_products, Product
import json
import logging

def handle_request(request):
    req_json = request.get_json()

    intent = ""

    if req_json:
        intent = req_json["queryResult"]["intent"]["displayName"]
    else:
        logging.error('wrong usage: the request did not contain a valid JSON body.')
        return 'wrong usage: the request did not contain a valid JSON body.'

    if intent == "search_product_intent":
        json_str = json.dumps(req_json)
        # logging JSON POST Body for debugging purposes
        logging.info(f'json: {json_str}')
        return handle_search_product_intent(req_json)
    else:
        logging.error(f'the intent "{intent}" is not supported')
        return f'the intent "{intent}" is not supported'

def handle_search_product_intent(def_req):
    product = def_req["queryResult"]["parameters"]["product"]
    color = def_req["queryResult"]["parameters"]["color"]
    brand = def_req["queryResult"]["parameters"]["brand"]
    session = def_req["session"]

    products = search_products(f'{product} {color} {brand}')

    if len(products) == 0:
        text = def_req["queryResult"]["queryText"]
        logging.error(f'no products found for text: "{text}"')
        return f'no products found for text: "{text}"'

    return make_search_response(products[0], session)

def make_search_response(product, session):

    resp_items = [
        {
            "simpleResponse": {
                "textToSpeech": f'<speak>Ich habe den folgenden Artikel für dich gefunden: {product.name}</speak>',
                "displayText": product.name
            }
        }, {
            "basicCard": {
                "title": product.name,
                "image": {
                    "url": product.image_url,
                    "accessibilityText": "keine Vorschau"
                }
            }
        }, {
            "suggestions": [
                {
                    "title": "nächster Treffer"
                }
            ]
        }
    ]

    resp_payload = {
        "google": {
            "expectUserResponse": True,
            "richResponse": {
                "items": resp_items
            }
        }
    }

    resp_out_contexts = [
        {
            "name": f'{session}/contexts/next_result',
            "lifespanCount": 3
        }
    ]

    response = {
        "source": "Otto Voice Search",
        "payload": resp_payload,
        "outputContexts": resp_out_contexts
    }

    return json.dumps(response, ensure_ascii=False).encode('utf8')
