import logging
from product import Product
from df_helper import make_card_response_from_product
import json

def make_show_next_response(df_req:dict) -> str:
    """Makes a Dialogflow Response for the intent in wicht the
    user wants to see the next article."""
    
    session = df_req["session"]
    ctx = get_context(df_req["queryResult"]["outputContexts"],
        f'{session}/contexts/next_result')
    
    # first increment the index of the current product
    ctx = increment_current_idx(ctx)

    # get the product with the right index
    product = get_product(ctx)

    if product.article_nr == -1:
        return make_no_more_article_response()

    return make_card_response_from_product(session, product, ctx["parameters"])

def get_context(contexts:list, desired_ctx:str) -> dict:
    
    for c in contexts:
        if c["name"] == desired_ctx:
            return c

    logging.error(f'context: {desired_ctx} not found')
    return {}

def get_product(ctx:dict) -> Product:
    idx = int(ctx["parameters"]["current-index"])
    products = ctx["parameters"]["products"]
    
    if idx < len(products):
        prd_dict = products[idx]

        return Product(
            prd_dict["article-number"],
            prd_dict["name"],
            prd_dict["price"],
            prd_dict["image"],
            prd_dict["url"]
        )
    else:
        return Product(-1, "", "", "", "")

def increment_current_idx(ctx:dict) -> dict:
    ctx["parameters"]["current-index"] += 1
    return ctx

def make_no_more_article_response():
    resp_items = [
        {
            "simpleResponse": {
                "textToSpeech": "Keine weiteren Artikel. Versuche eine neue Suche oder lass dich direkt auf otto D E inspirieren!",
                "displayText": "Keine weiteren Artikel"
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

