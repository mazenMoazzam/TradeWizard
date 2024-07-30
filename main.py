from alpaca_trade_api.rest import REST, TimeFrame
from dataHandler import DataHandler
from orderManagement import OrderManager
import pandas as pd


#apiKey = 'PKG126Z4K4SABUBFSYBG'
#secretKey = '2KdUrhkh83ZTZc24AtmU1Lc79HlcaQtERLZhwDrE' to keep for reference.
#url = 'https://paper-api.alpaca.markets'

apiKey = 'PKG126Z4K4SABUBFSYBG'
secretKey = '2KdUrhkh83ZTZc24AtmU1Lc79HlcaQtERLZhwDrE'
url = 'https://paper-api.alpaca.markets'


def main():
    alpacaApi = REST(apiKey, secretKey, url, api_version='v2')
    data = DataHandler(alpacaApi)
    order = OrderManager(alpacaApi)

    pd.set_option('display.max_columns', None)
    pd.set_option('display.expand_frame_repr', False)


    symbol = 'CI'
    start_date = '2024-07-01'
    end_date = '2024-07-10'
    historical_data = data.get_historical_data(symbol, start_date, end_date)
    port = data.get_portfolio()
    print(order.get_cash())
if __name__ == "__main__":
    main()