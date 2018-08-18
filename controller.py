from scrape_search import search_products
from df_search_response import make_search_response
from df_show_next_response import make_show_next_response
import json
import logging
from product import Product

def handle_request(request) -> str:
    req_json = request.get_json()

    intent = ""

    # check if request has an intent
    if req_json:
        intent = req_json["queryResult"]["intent"]["displayName"]
        logging.info(f'intent found: {intent}')
    else:
        logging.error('wrong usage: the request did not contain a valid JSON body.')
        return 'wrong usage: the request did not contain a valid JSON body.'

    # logging JSON POST Body for debugging purposes
    json_str = json.dumps(req_json)
    logging.info(f'json: {json_str}')

    # chose handler for intent
    if intent == "search_product_intent":
        return handle_search_product_intent(req_json)
    elif intent == "show_next_result":
        return handle_show_next_result(req_json)
    else:
        logging.error(f'the intent "{intent}" is not supported')
        return f'the intent "{intent}" is not supported'

def handle_search_product_intent(df_req:dict) -> str:
    product = df_req["queryResult"]["parameters"]["product"]
    color = df_req["queryResult"]["parameters"]["color"]
    brand = df_req["queryResult"]["parameters"]["brand"]
    session = df_req["session"]

    products = search_products(f'{product} {color} {brand}')

    return make_search_response(products, session)

def handle_show_next_result(df_req:dict) -> str:
    return make_show_next_response(df_req)