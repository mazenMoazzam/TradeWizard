import pandas as pd
import time
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream

class TradingLogic:
    def __init__(self, api, dataHandler, orderManager, portfolio, rsi_period=14, rsi_overbought=70, rsi_oversold=30, trading_interval=60):
        self.api = api
        self.dataHandler = dataHandler
        self.orderManager = orderManager
        self.portfolio = portfolio
        self.rsi_period = rsi_period
        self.rsi_overbought = rsi_overbought
        self.rsi_oversold = rsi_oversold
        self.trading_interval = trading_interval

    def calculate_rsi(self, close_prices):
        close_prices = pd.to_numeric(close_prices, errors='coerce')
        delta = close_prices.diff()
        print(f"Price Changes (delta):\n{delta.head()}")

        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()

        print(f"Average Gains:\n{gain.head()}")
        print(f"Average Losses:\n{loss.head()}")

        gain = gain.fillna(0)
        loss = loss.fillna(0)
        loss = loss.replace(0, 0.01)  # Avoid division by zero

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        print(f"RS:\n{rs.head()}")
        print(f"RSI:\n{rsi.head()}")

        return rsi

    def start_trading(self):
        while True:
            marketOpen = self.dataHandler.is_market_open()
            print(f"Market Open Status: {marketOpen}")
            if marketOpen:
                print("Market is open. Starting trading...")
                for symbol, qty in self.portfolio:
                    self.trading_logic(symbol, qty)
            else:
                print("Market is closed. Waiting for the market to open...")

            time.sleep(self.trading_interval)

    def trading_logic(self, symbol, qty):
        try:
            positions = self.api.list_positions()
            ownedStocks = {position.symbol: float(position.qty) for position in positions}

            end_date = pd.Timestamp.now(tz='America/New_York')
            start_date = end_date - pd.Timedelta(days=365)

            historical_data = self.dataHandler.get_historical_data(symbol, start_date.strftime('%Y-%m-%d'),
                                                                   end_date.strftime('%Y-%m-%d'))

            if historical_data.empty:
                print(f"No data returned for {symbol}. Skipping...")
                return

            print(f"Data Length for {symbol}: {len(historical_data)}")
            print(historical_data.head())

            if len(historical_data) < self.rsi_period:
                print(f"Not enough data to calculate RSI for {symbol}. Skipping...")
                return

            historical_data['rsi'] = self.calculate_rsi(historical_data['close'])

            if historical_data['rsi'].isnull().values.any():
                print(f"RSI could not be calculated properly for {symbol}. Skipping...")
                return

            print(f"RSI for {symbol}:")
            print(historical_data[['rsi']].tail())

            latest_rsi = historical_data['rsi'].iloc[-1]
            print(f"Latest RSI for {symbol}: {latest_rsi}")

            if latest_rsi < self.rsi_oversold:
                self.orderManager.place_order(symbol, qty, 'buy', 'market', 'gtc')
                print(f"Buy Signal for {symbol} based on RSI - Placing order for {qty} shares")
            elif latest_rsi > self.rsi_overbought:
                current_positions = self.orderManager.get_positions()
                if any(pos['symbol'] == symbol and int(pos['qty']) >= qty for pos in current_positions):
                    self.orderManager.place_order(symbol, qty, 'sell', 'market', 'gtc')
                    print(f"Sell Signal for {symbol} based on RSI - Placing order for {qty} shares")
                else:
                    print(f"Sell Signal for {symbol} but insufficient quantity to sell")

        except Exception as e:
            print(f"Error in trading logic for {symbol}: {e}")
