from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
import yfinance as yf


class DataHandler:
    def __init__(self, api):
        self.api = api

    def get_historical_data(self, symbol, startDate, endDate):
        data = yf.download(symbol, start=startDate, end=endDate)
        print(f'Downloaded data for {symbol}:\n{data.head()}')

        data.columns = [col.lower() for col in data.columns]
        data.reset_index(inplace=True)
        return data

    def get_real_time_quote(self, symbol):
        return self.api.get_latest_trade(symbol)  # gets recent real time quote with the inputted symbol from user.

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
        data = [{
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
            return clock.is_open
        except Exception as e:
            print(f'Error checking market status: {e}')
            return False

    def get_portfolio(self):
        ''' #intial code to retrieve user's portfolio (output was a bit unreadable)
        try:
            positions = self.api.list_positions()
            return positions
        except Exception as e:
            print(f'Error fetching the portfolios: {e}')
            return None
        '''
        positions = self.api.list_positions()
        portfolioData = []

        for position in positions:
            portfolioData.append({
                'Ticker Symbol': position.symbol,
                'Shares': position.qty,
                'Avg Entry Price': position.avg_entry_price,
                'Current Price': position.current_price,
                'Market Value': position.market_value,
                'Unrealized P/L': position.unrealized_pl,
                'Unrealized P/L %': position.unrealized_plpc
            })
        return pd.DataFrame(portfolioData)

    def calculate_portfolio_value(self):
        try:
            positions = self.api.list_positions()
            totalValue = sum(float(position.market_value) for position in positions)
            return totalValue
        except Exception as e:
            print(f'Error calculating portfolio value: {e}')
            return None
