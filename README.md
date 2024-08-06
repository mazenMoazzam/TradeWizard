# TradeWizard
-This is a comprehensive stock market paper trading bot designed to automated the trading of stocks using Alpaca's API. The bot can place buy and sell orders based on technical analysis and follows its own trading logic as well as gathering real tiem data and historical data regarding specific stocks. This bot also logs trades and orders in a SQLite database, providing a comprehensive record of all trading activity done on the user's account.

# Features
-Automated Trading: Uses RSI (Relative Strength Index) to determine buy and sell signals.
-Real-Time Data Streaming: Subscribes to real-time stock updates and processes them.
-Order Management: Places, cancels, and updates orders. Keeps track and stores them in a database. 
-Database Logging: Stores order and trade information in a SQLite database.
-SMS Automation/Notifications: Sends SMS notifications for order placement, updates, and cancellations.
