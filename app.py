from flask import Flask, request, jsonify
from dataHandler import DataHandler
from alpaca_trade_api.rest import REST, TimeFrame
from orderManagement import OrderManager

apiKey = 'PKG126Z4K4SABUBFSYBG'
secretKey = '2KdUrhkh83ZTZc24AtmU1Lc79HlcaQtERLZhwDrE'
url = 'https://paper-api.alpaca.markets'

twilio_sid = 'ACd08d4a99a3a12582ad7d30f50c3dd575'
twilio_auth_token = '7084ed704ff6dcc47d2d9e87330324d4'
twilio_phone_number = '+18772741628'

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


