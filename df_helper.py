from product import Product
import json


def make_card_response_from_product(session:str, product:Product, parameters:list) -> str:
    """Assembles a Dialogflow response that contains a BasicCard with
    an image of the product."""
    
    resp_items = [
        {
            "simpleResponse": {
                "textToSpeech": make_text_to_speech(product),
                "displayText": f'{product.price} EUR'
            }
        }, {
            "basicCard": {
                "title": f'{product.name} - {product.price} EUR',
                "image": {
                    "url": product.image_url,
                    "accessibilityText": "keine Vorschau"
                },
                "buttons": [
                    {
                    "title": "auf otto.de ansehen",
                    "openUrlAction": {
                        "url": product.url
                        }
                    }
                ]
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
            "parameters": parameters
        }
    ]

    response = {
        "source": "Otto Voice Search",
        "payload": resp_payload,
        "outputContexts": resp_out_contexts
    }

    return json.dumps(response, ensure_ascii=False).encode('utf8')

def make_text_to_speech(product:Product) -> str:

    # there seems to be a bug in dialogflow so that in string with an &,
    # the <speak>-tags are spoken.
    p_name = product.name.replace("&", " und ")\
    .replace("inkl.", "inklusive")\
    .replace("incl.", "inklusive")\
    .replace("einschl.", "einschließlich")\
    .replace("tlg.", "teilig")\
    .replace("-tlg.", " teilig")\
    .replace("St", "Stück")\
    .replace("St.", "Stück")\
    .replace("Stk", "Stück")\
    .replace("Stk.", "Stück")\
    .replace("U/Min", "Umdrehungen pro Minute")\
    .replace("U/min", "Umdrehungen pro Minute")\
    .replace("«", "'")\
    .replace("»", "'")\
    .replace("™", "")\
    .replace("®", "")

    return f'<speak>Gefunden auf otto D E: {p_name}. Der Artikel kostet {product.price} Euro</speak>'