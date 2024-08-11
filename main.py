from alpaca_trade_api.rest import REST, TimeFrame
from dataHandler import DataHandler
from orderManagement import OrderManager
from tradingLogic import TradingLogic


def main():
    alpacaApi = REST(apiKey, secretKey, url, api_version='v2')
    data = DataHandler(alpacaApi)
    order = OrderManager(alpacaApi, twilio_sid, twilio_auth_token, twilio_phone_number)
    portfolio = [('LMT', 1)]
    trading = TradingLogic(alpacaApi, data, order, portfolio)
    print(trading.getSentimentScore('PENN'))

if __name__ == "__main__":
    main()
