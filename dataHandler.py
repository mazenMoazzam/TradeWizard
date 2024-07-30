from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd

class DataHandler:
    def __init__(self, api):
        self.api = api

    def get_historical_data(self, symbol, startDate, endDate):
        bars = self.api.get_bars(
            symbol,
            TimeFrame.Day,
            start=startDate,
            end=endDate
        )

        data = [{
            'time': bar.t,
            'open': bar.o,
            'high': bar.h,
            'low': bar.l,
            'close': bar.c,
            'volume': bar.v,
            'vwap': bar.vw
        }for bar in bars]
        return pd.DataFrame(data)

    def get_real_time_quote(self, symbol):
        return self.api.get_latest_trade(symbol) #gets latest real time quote with the inputted symbol from user.

    def get_current_price(self, symbol: str):
        try:
            quote = self.api.get_latest_quote(symbol)
            return quote.ask_price if quote.ask_price else quote.bid_price
        except Exception as e:
            print(f"Error getting current price of {symbol}: {e}")
            return None

    def get_intraday_data(self, symbol, startDate, endDate, timeFrame=TimeFrame.Hour):
        bars = self.api.get.bars(
            symbol,
            timeFrame,
            start=startDate,
            end=endDate
        )
        data= [{
            'time': bar.t,
            'open': bar.o,
            'high': bar.h,
            'low': bar.l,
            'close': bar.c,
            'volume': bar.v,
            'vwap': bar.vw
        } for bar in bars]
        return pd.DataFrame(data)

    def is_market_open(self):
        try:
            clock = self.api.get_clock()
            if clock.is_open:
                return 'Market is currently open.'
            else:
                return 'Market is currently closed, will open at 9:30 A.M'
        except Exception as e:
            print(f'Error checking market status: {e}')
            return False
