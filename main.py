"""For GCP Usage"""

from scrape_search import search_products, Product

def webhook(request):
    if request.args and 'text' in request.args:
        text = request.args.get('text')
        products = search_products(text)

        answer = ''
        for p in products:
            answer += p.__str__()
        return f'articles: {answer}'

    elif request.get_json:
        return request.get_json

    else:
        return 'wrong usage: please specify a request parameter called text.'
