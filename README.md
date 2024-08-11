# TradeWizard
-This is a comprehensive stock market paper trading bot designed to automated the trading of stocks using Alpaca's API. The bot can place buy and sell orders based on technical analysis and follows its own trading logic as well as gathering real tiem data and historical data regarding specific stocks. This bot also logs trades and orders in a SQLite database, providing a comprehensive record of all trading activity done on the user's account. Implementing sentiment analysis at this moment. 

# Features
-Automated Trading: Uses RSI (Relative Strength Index) trading strategy to determine buy and sell signals.


-Real-Time Data Streaming/Trading: Subscribes to real-time stock updates and processes them. Trades stocks in real-time.


-Order Management: Places, cancels, and updates orders. Keeps track and stores them in a database. 


-Database Logging: Stores order and trade information in a SQLite database.


-SMS Automation/Notifications: Sends SMS notifications for order placement, updates, and cancellations.


-Sentiment Analysis: Returns a sentiment score regarding any stock via ticker symbol. Achieved using News API and BeautifulSoup to fetch social media articles/news regarding a stock, and returns a sentiment score using VADER. 

