from dataHandler import DataHandler
from orderManagement import OrderManager
from tradingLogic import TradingLogic


class TradingBot:
    def __init__(self, api, twilio_sid, twilio_auth_token, twilio_phone_number, portfolio, rsi_period=14, rsi_overbought=70, rsi_oversold=30, trading_interval=60):
        self.data_handler = DataHandler(api)
        self.order_manager = OrderManager(api, twilio_sid, twilio_auth_token, twilio_phone_number)
        self.trading_logic = TradingLogic(api, self.data_handler, self.order_manager, portfolio, rsi_period, rsi_overbought, rsi_oversold, trading_interval)

    def update_portfolio(self):
        """Refresh the portfolio data."""
        self.portfolio = self.data_handler.get_positions()

    def execute_trading_strategy(self):
        """Execute trading strategy based on the current portfolio."""
        self.update_portfolio()
        self.trading_logic.start_trading()


    def monitor_portfolio(self):
        """Log the current portfolio."""
        portfolio = self.data_handler.get_positions()
        print(f"Current portfolio:\n{portfolio}")

    def manage_orders(self):
        """Log and manage all orders."""
        orders = self.order_manager.list_all_orders(status='all')
        print(f"Current orders:\n{orders}")

    def fetch_account_info(self):
        """Log account information."""
        account_info = self.order_manager.get_account_info()
        print(f"Account info:\n{account_info}")

    def fetch_cash_balance(self):
        """Log cash balance."""
        cash_balance = self.order_manager.get_cash()
        print(f"Cash balance:\n{cash_balance}")

    def place_order(self, symbol, qty, side, order_type='market', time_in_force='gtc'):
        """Place an order using OrderManager."""
        try:
            self.order_manager.place_order(symbol, qty, side, order_type, time_in_force)
            print(
                f"Order placed: {side} {qty} shares of {symbol} with {order_type} order and {time_in_force} time in force.")
        except Exception as e:
            print(f"Error placing order: {e}")