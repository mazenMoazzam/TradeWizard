from flask import Flask, request, jsonify
from dataHandler import DataHandler
from alpaca_trade_api.rest import REST, TimeFrame
from orderManagement import OrderManager
'

alpacaApi = REST(apiKey, secretKey, url, api_version='v2')

order = OrderManager(alpacaApi, twilio_sid, twilio_auth_token, twilio_phone_number)

app = Flask(__name__)

@app.route('/place_order', methods=['POST'])
def place_order():
    data = request.json

    symbol = data.get('symbol')
    qty = data.get('qty')
    side = data.get('side')
    orderType = data.get('order_type')
    timeInForce = data.get('time_in_force')

    orderResponse = order.place_order(symbol, qty, side, orderType, timeInForce)

    if orderResponse:
        return jsonify({'status': 'success', 'order': orderResponse}), 200
    else:
        return jsonify({'status': 'error', 'message': 'Failed to place order'}), 400

if __name__ == '__main__':
    app.run(debug=True)


