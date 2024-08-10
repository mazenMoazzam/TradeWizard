from alpaca_trade_api.rest import REST, TimeFrame
from dataHandler import DataHandler
from orderManagement import OrderManager
from tradingLogic import TradingLogic

# apiKey = 'PKG126Z4K4SABUBFSYBG'
# secretKey = '2KdUrhkh83ZTZc24AtmU1Lc79HlcaQtERLZhwDrE' to keep for reference.
# url = 'https://paper-api.alpaca.markets'

apiKey = 'PKG126Z4K4SABUBFSYBG'
secretKey = '2KdUrhkh83ZTZc24AtmU1Lc79HlcaQtERLZhwDrE'
url = 'https://paper-api.alpaca.markets'

twilio_sid = 'AC8be78dea1f6134d36b5682bdf46e176e'
twilio_auth_token = '19aa62b8a83555641e5f70a42e031b80'
twilio_phone_number = '+18888713828'


def main():
    alpacaApi = REST(apiKey, secretKey, url, api_version='v2')
    data = DataHandler(alpacaApi)
    order = OrderManager(alpacaApi, twilio_sid, twilio_auth_token, twilio_phone_number)
    portfolio = [('LMT', 1)]
    trading = TradingLogic(alpacaApi, data, order, portfolio)


if __name__ == "__main__":
    main()
