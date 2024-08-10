from alpaca_trade_api.rest import REST, TimeFrame
from dataHandler import DataHandler
from orderManagement import OrderManager
from tradingLogic import TradingLogic
from dotenv  import load_dotenv
import os

load_dotenv()

apiKey = os.getenv('API_KEY')
secretKey = os.getenv('SECRET_KEY')
url = os.getenv('URL')

twilio_sid = os.getenv('TWILIO_SID')
twilio_auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_phone_number = os.getenv('TWILIO_PHONE_NUMBER')


def main():
    alpacaApi = REST(apiKey, secretKey, url, api_version='v2')
    data = DataHandler(alpacaApi)
    order = OrderManager(alpacaApi, twilio_sid, twilio_auth_token, twilio_phone_number)
    portfolio = [('LMT', 1)]
    trading = TradingLogic(alpacaApi, data, order, portfolio)
    print(trading.getSentimentScore('PENN'))

if __name__ == "__main__":
    main()
