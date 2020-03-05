from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

shipment_options = [ 
    {
        'id': 1,
        'title': u"shipping option number 1",
        'description': 'free by air',
        'done': 'False'
    },
    {
        'id': 2,
        'title': u"shipping option number 2",
        'description': 'free by water',
        'done':'False'
    }
]


@app.route('/api/v1/shipping_offers/<int:shipment_id>', methods=['GET'])
def get_shipping_offers(shipment_id):
    shipping_offer = [shipment for shipment in shipment_options if shipment['id'] == shipment_id ]
    if len(shipping_offer) == 0:
        abort(404)
    return(jsonify({"shipment": shipment_options[0]}))

@app.route('/api/v1/shipping_offers', methods=['POST'])
def create_shipment():
    if not request.json or not "title" in request.json:
        abort(400)
    shipment_option = {
        'id': shipment_options[-1]['id'] + 1,
        'title': request.json['title'],
        'description': request.json.get('description', ""),
        'done': 'false'
        }
    shipment_options.append(shipment_option)
    return(jsonify({"shipment": shipment_options}), 201)



@app.errorhandler(404)
def not_found(error):
    return(make_response(jsonify({"error": "Not found"}),))


if __name__=='__main__':
    app.run(debug=True)
