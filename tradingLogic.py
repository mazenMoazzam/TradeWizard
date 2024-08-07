import pandas as pd
import time
import logging

import requests
from bs4 import BeautifulSoup
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from alpaca_trade_api.rest import REST, TimeFrame
from alpaca_trade_api.stream import Stream

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

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
        self.sentiment_analyzer = SentimentIntensityAnalyzer()


    def calculate_rsi(self, close_prices):
        close_prices = pd.to_numeric(close_prices, errors='coerce')
        delta = close_prices.diff()
        logging.info(f"Price Changes (delta):\n{delta.head()}")

        gain = (delta.where(delta > 0, 0)).rolling(window=self.rsi_period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.rsi_period).mean()

        logging.info(f"Average Gains:\n{gain.head()}")
        logging.info(f"Average Losses:\n{loss.head()}")

        gain = gain.fillna(0)
        loss = loss.fillna(0)
        loss = loss.replace(0, 0.01)

        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))

        logging.info(f"RS:\n{rs.head()}")
        logging.info(f"RSI:\n{rsi.head()}")

        return rsi

    def start_trading(self):
        while True:
            marketOpen = self.dataHandler.is_market_open()
            logging.info(f"Market Open Status: {marketOpen}")
            if marketOpen:
                logging.info("Market is open. Starting trading...")
                for symbol, qty in self.portfolio:
                    self.trading_logic(symbol, qty)
            else:
                logging.info("Market is closed. Waiting for the market to open...")

            time.sleep(self.trading_interval)

    def trading_logic(self, symbol, qty):
        try:
            positions = self.api.list_positions()
            ownedStocks = {position.symbol: float(position.qty) for position in positions}

            endDate = pd.Timestamp.now(tz='America/New_York')
            startDate = endDate - pd.Timedelta(days=365)

            historical_data = self.dataHandler.get_historical_data(symbol, startDate.strftime('%Y-%m-%d'),
                                                                   endDate.strftime('%Y-%m-%d'))

            if historical_data.empty:
                logging.warning(f"No data returned for {symbol}. Skipping...")
                return

            logging.info(f"Data Length for {symbol}: {len(historical_data)}")
            logging.info(historical_data.head())

            if len(historical_data) < self.rsi_period:
                logging.warning(f"Not enough data to calculate RSI for {symbol}. Skipping...")
                return

            historical_data['rsi'] = self.calculate_rsi(historical_data['close'])

            if historical_data['rsi'].isnull().values.any():
                logging.warning(f"RSI could not be calculated properly for {symbol}. Skipping...")
                return

            logging.info(f"RSI for {symbol}:")
            logging.info(historical_data[['rsi']].tail())

            latest_rsi = historical_data['rsi'].iloc[-1]
            latest_volume = historical_data['volume'].iloc[-1]
            average_volume = historical_data['volume'].rolling(window=self.rsi_period).mean().iloc[-1]

            logging.info(f"Latest RSI for {symbol}: {latest_rsi}")
            logging.info(f"Latest Volume for {symbol}: {latest_volume}")
            logging.info(f"Average Volume for {symbol}: {average_volume}")

            if latest_rsi < self.rsi_oversold and latest_volume > average_volume:
                self.orderManager.place_order(symbol, qty, 'buy', 'market', 'gtc')
                logging.info(f"Buy Signal for {symbol} based on RSI and Volume - Placing order for {qty} shares")
            elif latest_rsi > self.rsi_overbought and symbol in ownedStocks and ownedStocks[symbol] >= qty:
                self.orderManager.place_order(symbol, qty, 'sell', 'market', 'gtc')
                logging.info(f"Sell Signal for {symbol} based on RSI and Volume - Placing order for {qty} shares")
            else:
                logging.info(f"No valid trading signal for {symbol} at this time.")

        except Exception as e:
            logging.error(f"Error in trading logic for {symbol}: {e}")

    def getSentimentScore(self, symbol):
        url = f'https://finance.yahoo.com/quote/{symbol}/news/'
        response = requests.get(url)
        soupScraper = BeautifulSoup(response.text, 'html.parser')
        headLines = soupScraper.find_all('h3', class_='Mb(5px)')
        combinedText = ' '.join([headLine.get_text() for headLine in headLines])

        print(f"Extracted headlines for {symbol}:")
        for headline in headLines:
            print(headline.get_text()) #estbalished a for loop to see if web scraper actually extracts information for debugging
            #purposes.
        sentimentScore = self.sentiment_analyzer.polarity_scores(combinedText)
        logging.info(f'Sentiment Analysis for {symbol} headlines: {sentimentScore}')

        return sentimentScore['compound']