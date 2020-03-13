import json
import os

from dotenv import load_dotenv
from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPTokenAuth

# load_dotenv()

app = Flask(__name__)
# app.secret_key = os.getenv("FLASK_SECRET_KEY")

''' Test '''

shipment_options = [
    {
        'request_id': '1111.111',
        'sender_address': {
            'first_name': 'Decathlon USA LLC',
            'last_name': '',
            'country_code': 'US',
            'city': 'San Francisco',
            'zip_code': '94107',
            'state': 'CA',
            'address_line_1': '2415 3rd Street',
            'address_line_2': '',
            'phone': '555 5555 555'
            },
        'shipping_address': {
            'country_code': 'US',
            'zip_code': '94124',
            'address_line_1': '5880 3rd St',
            'city': 'San Francisco',
            'state': 'CA',
            'phone': '5555555555'
            },
        'fulfillment_node_id': 'WHOA002',
        'ready_by': '2020-03-12T23:32:16.125862',
        'service_level': 'UPS_SECOND_DAY_AIR',
        'provider_rate': 'UPS Second Day Air',
        'deliverables': [
            {
                'item': {
                    'weight': {
                        'amount': 184.0,
                        'unit': 'g'
                        },
                    'dimensions': {
                        'height': 3.15,
                        'length': 9.84,
                        'width': 5.12,
                        'unit': 'in'
                        },
                    'price': {
                        'amount': 9.99,
                        'currency': 'USD'
                        }},
                'quantity': 1
                }
            ]
        }
    ]

shipments = [
    {
        'request_id': '2111.111',
        'rate': 'FEDEX_GROUND',
        'demand_location_id': 'US01',
        'fulfillment_node_id': 'US02',
        'carrier_code': 'FEDEX',
        'external_order_id': '981475723',
        'booking_method': 'shipping_and_return',
        'sender_address': {
            'first_name': 'John',
            'last_name': 'Doe',
            'phone': '202-555-0186',
            'country_code': 'US',
            'city': 'New York',
            'zip_code': '10001',
            'address_line_1': '2635 Simons Hollow Road',
            'state': 'New York'
            },
        'shipping_address': {
            'first_name': 'James',
            'last_name': 'Navarrete',
            'phone': '520-466-2640',
            'country_code': 'US',
            'city': 'Arizona City',
            'zip_code': '85223',
            'address_line_1': '2035 Parkway Drive',
            'state': 'AZ'
            },
        'items': [
                        {
                            'identifier': {
                                'EPC': '32WE4335'
                                }
                            },
                        {
                            'identifier': {
                                'EPC': '473UC75279'
                                },
                            'price': {
                                'amount': 15.4
                                },
                            'weight': {
                                'amount': 350,
                                'unit': 'g'
                                }
                            }
                        ],
        'package_option': {
                        'weight': {
                            'amount': 2.5,
                            'unit': 'lb'
                            }
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
        'request_id': str(float(shipment_options[-1]['request_id']) + 0.001),
        'sender_address': request.json.get('sender_address', ''),
        'shipping_address': request.json.get('shipping_address', ''),
        'fulfillment_node_id': request.json.get('fulfillment_node_id', ''),
        'ready_by': request.json.get('ready_by', ''),
        'service_level': request.json.get('service_level', ''),
        'provider_rate': request.json.get('provider_rate', ''),
        'deliverables': request.json.get('deliverables', '')
        }

#    with open("POST_request.json") as f:
#        shipment_option = json.load(f)
    shipment_options.append(shipment_option)
    print(f"POST SHIPMENT OPTION {shipment_option}")
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
    shipment = {
        'request_id': str(float(shipments[-1]['request_id']) + 0.001),
        'shipping_address': request.json.get('shipping_address', ''),
        'rate': request.json.get('rate', ''),
        'demand_location_id': request.json.get('demand_location_id', ''),
        'fulfillment_node_id': request.json.get('fulfillment_node_id', ''),
        'carrier_code': request.json.get('carrier_code', ''),
        'external_order_id': request.json.get('external_order_id', ''),
        'booking_method': request.json.get('booking_method', ''),
        'sender_address': request.json.get('sender_address', ''),
        'items': request.json.get('items', ''),
        'package_option': request.json.get('package_option', '')
        }

#    with open("POST_request.json") as f:
#        shipment_option = json.load(f)
    shipment_options.append(shipment)
    print(f"POST SHIPMENT OPTION {shipment}")
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
