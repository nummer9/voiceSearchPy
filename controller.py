from scrape_search import search_products, Product
import json
import logging

def handle_request(request):
    req_json = request.get_json()

    if req_json:
        json_str = json.dumps(req_json)
        # logging JSON POST Body for debugging purposes
        logging.info(f'json: {json_str}')
        return handle_search_request(req_json)

    else:
        logging.error('wrong usage: the request did not contain a valid JSON body.')
        return 'wrong usage: the request did not contain a valid JSON body.'

def handle_search_request(def_req):
    product = def_req["queryResult"]["parameters"]["product"]
    color = def_req["queryResult"]["parameters"]["color"]
    brand = def_req["queryResult"]["parameters"]["brand"]

    products = search_products(f'{product} {color} {brand}')

    for p in products:
        print(p.__str__())

    return product
