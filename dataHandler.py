from alpaca_trade_api.rest import REST, TimeFrame
import pandas as pd
import yfinance as yf
from alpaca_trade_api.stream import Stream
import asyncio
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')



class DataHandler:
    def __init__(self, api):
        self.api = api
        self.stream=None

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

    def get_positions(self):
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
    async def on_trade_update(self, trade):
        print(f"New trade: {trade}")

    async def on_quote_update(self, quote):
        print(f"New quote: {quote}")

    async def start_streaming(self, symbols):
        if not self.is_market_open():
            logging.info('Market is closed, streaming cannot be done at this time.')
            return 'Market is closed, streaming cannot be done at this time.'

        if self.stream is None:
            self.stream = Stream(
                key_id=self.api._key_id,
                secret_key=self.api._secret_key,
                base_url=self.api._base_url,
                data_feed='iex'
            )

            for symbol in symbols:
                self.stream.subscribe_trades(self.on_trade_update, symbol)
                self.stream.subscribe_quotes(self.on_quote_update, symbol)

            logging.info(f'Subscribed to trades and quotes for: {symbols}')

            try:
                await self.stream._run_forever()
            except KeyboardInterrupt:
                logging.info("Streaming stopped manually.")
        else:
            logging.info("Stream is already running.")

    def stop_streaming(self):
        if self.stream:
            self.stream.close()
            print("Stopped streaming")
