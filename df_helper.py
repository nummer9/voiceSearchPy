from product import Product
import json


def make_card_response_from_product(session:str, product:Product, parameters:list) -> str:
    """Assembles a Dialogflow response that contains a BasicCard with
    an image of the product."""
    
    resp_items = [
        {
            "simpleResponse": {
                "textToSpeech": make_text_to_speech(product),
                "displayText": "gefunden auf otto.de"
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
    return f'<speak>Gefunden auf otto D E: {product.name}. Der Artikel kostet {product.price} Euro</speak>'