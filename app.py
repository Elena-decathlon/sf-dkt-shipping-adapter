import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPTokenAuth

#load_dotenv()

app = Flask(__name__)
#app.secret_key = os.getenv("FLASK_SECRET_KEY")

''' Test '''
shipment_options = [
    {
        "request_id": "1111.111",
        "bag": {
            "products": [
                {
                    "product_id": "200121",
                    "quantity": 1,
                    "price": {
                        "amount": 1.2,
                        "currency": "USD"
                        },
                    "weight": {
                        "value": 1,
                        "unit": "lb"
                        },
                    "dimensions": {
                        "length": 5,
                        "width": 5,
                        "height": 5,
                        "unit": "in"
                        }
                    }
                ]
            },
        "shipping_address": {
            "address_line_1": "999 Yawkey Way",
            "address_line_2": "999nd floor",
            "city": "Boston",
            "country_code": "US",
            "zip_code": "20038"
            }
        }
    ]

''' Logging headers and body before request'''


@app.before_request
def log_request_info():
    app.logger.debug('Header: %s', request.headers)
    app.logger.debug('Body: %s', request.get_data())

''' GET method '''


@app.route('/api/v1/shipping_offers/<request_id>', methods=['GET'])
def get_shipping_offers(request_id):
    float(request_id)
    shipping_offer = [shipment for shipment in shipment_options if shipment['request_id'] == str(request_id)]
    if len(shipping_offer) == 0:
        abort(404)
    return(jsonify({"shipment": shipping_offer[0]}))

''' POST method / shipping offers'''


@app.route('/api/v1/shipping_offers', methods=['POST'])
def post_shipping_offers():
    print(f"REQUEST SHIPPING_OFFERS: {request.json}")
    if not request.json or not "shipping_address" in request.json:
#       abort(400)
        with open("shipping_offers_400.json") as f:
            data = json.load(f)
        return(jsonify(data), 400)
    shipment_option = {
            'bag': {
                'products': [
                    {
                        'dimentions': {
                            'height': 0,
                            'lenght': 0,
                            'unit': '',
                            'width': 0
                            },
                        "price": {
                            "amount": 0.0,
                            "currency": ''
                            },
                        'product_id': 0,
                        'quantity': 0,
                        'weight': {
                            'unit': '',
                            'value': 0
                            }
                        }
                    ]
                },
            'request_id': str(float(shipment_options[-1]['request_id']) + 0.001),
            'shipping_address': request.json.get('shipping_address', '')
        }
#    with open("POST_request.json") as f:
#        shipment_option = json.load(f)
    shipment_options.append(shipment_option)
    print(shipment_option)
#    with open("shipping_offers_201.json") as f:
#        data = json.load(f)
    with open("shipping_offers_free_shipping.json") as f:
        data = json.load(f)
    return(jsonify(data), 201)

''' POST method / shipments'''


@app.route('/api/v1/shipments', methods=['POST'])
def post_shipments():
    print(f"REQUEST SHIPMENTS: {request.json}")
    if not request.json or not "shipping_address" in request.json:
#       abort(400)
        with open("shipment_400.json") as f:
            data = json.load(f)
        return(jsonify(data), 400)
    shipment_option = {
            'bag': {
                'products': [
                    {
                        'dimentions': {
                            'height': 0,
                            'lenght': 0,
                            'unit': '',
                            'width': 0
                            },
                        "price": {
                            "amount": 0.0,
                            "currency": ''
                            },
                        'product_id': 0,
                        'quantity': 0,
                        'weight': {
                            'unit': '',
                            'value': 0
                            }
                        }

                    ]
                },
            'request_id': str(float(shipment_options[-1]['request_id']) + 0.001),
            'shipping_address': request.json.get('shipping_address', '')
        }
#    with open("POST_request.json") as f:
#        shipment_option = json.load(f)
    shipment_options.append(shipment_option)
    print(shipment_option)
    with open("shipment_201.json") as f:
        data = json.load(f)
    return(jsonify(data), 201)

''' DELETE method '''


@app.route('/api/v1/shipping_offers/<request_id>', methods=['DELETE'])
def delete_shipment(request_id):
    shipping_offer = [shipment for shipment in shipment_options if shipment['request_id'] == str(request_id)]
    if len(shipping_offer) == 0:
        abort(404)
    shipment_options.remove(shipping_offer[0])
    return(jsonify({'result': True}))

''' Error handler '''


@app.errorhandler(404)
def not_found(error):
    return(make_response(jsonify({"error": "Not found"}),))


if __name__ == '__main__':
    app.run(debug=True)
