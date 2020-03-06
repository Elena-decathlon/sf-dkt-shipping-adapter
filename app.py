from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

''' Test '''
shipment_options = [ 
 #   {
 #       'id': 1,
 #       'title': u"shipping option number 1",
 #       'description': 'free by air',
 #       'done': 'False'
 #   },
 #   {
 #       'id': 2,
 #       'title': u"shipping option number 2",
 #       'description': 'free by water',
 #       'done':'False'
 #   }
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

''' POST method '''


@app.route('/api/v1/shipping_offers', methods=['POST'])
def create_shipment():
#    if not request.json or not "title" in request.json:
    if not request.json or not "shipping_address" in request.json:
        abort(400)
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
#{
#                'address_line_1': '',
#                'address_line_2': '',
#                'city': '',
#                'country_code': '',
#                'zip_code': 0
#            'shipping_address': request.json['shipping_address'],
#        'description': request.json.get('description', ""),
#        'bag': request.json.get('bag', ""),
#            }
        }
    shipment_options.append(shipment_option)
    print("LOOK DOWN HERE")
    print(shipment_options)
    return(jsonify({"shipment": shipment_options}), 201)


''' Error handler '''


@app.errorhandler(404)
def not_found(error):
    return(make_response(jsonify({"error": "Not found"}),))


if __name__=='__main__':
    app.run(debug=True)
