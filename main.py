from alpaca_trade_api.rest import REST, TimeFrame
from dataHandler import DataHandler
from orderManagement import OrderManager
from tradingLogic import TradingLogic
from dotenv  import load_dotenv
from tradingBot import TradingBot
import os
import asyncio


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
    portfolio = [('TSLA', 1), ('AMZN', 1)]
    trading = TradingLogic(alpacaApi, data, order, portfolio)
    portfolio = []
    bot = TradingBot(alpacaApi, twilio_sid, twilio_auth_token, twilio_phone_number, portfolio)
    symbols = ['AAPL', 'GOOG']

    async def run():
        result = await data.start_streaming(symbols)
        print(result)

    asyncio.run(run())



if __name__ == "__main__":
    main()
