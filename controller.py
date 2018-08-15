from scrape_search import search_products, Product
import json
import logging

def handle_request(request):
    req_json = request.get_json()

    if request.args and 'text' in request.args:
        text = request.args.get('text')
        products = search_products(text)

        answer = ''
        for p in products:
            answer += p.__str__()
        return f'articles: {answer}'

    elif req_json:
        json_str = json.dumps(req_json)
        logging.info(f'json: {json_str}')
        return f'{json_str}'

    else:
        logging.error('wrong usage: please specify a request parameter called text.')
        return 'wrong usage: please specify a request parameter called text.'