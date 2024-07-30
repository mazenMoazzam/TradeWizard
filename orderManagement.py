from alpaca_trade_api.rest import REST, TimeFrame

class OrderManager:
    def __init__(self, api):
        self.api = api



    def place_order(self, symbol, qty, side, order_type, time_in_force):
        ''' Function used to place orders (buy or sell) on stocks
            Symbol is the ticker symbol of the stock, qty is simply the amount of shares,
            side (whether you want to buy or sell)
        '''
        try:
            order = self.api.submit_order(
                symbol=symbol,
                qty=qty,
                side=side,
                type=order_type,
                time_in_force=time_in_force
            )
            return order
        except Exception as e:
            print(f"Error placing order: {e}")
            return None

    def cancel_order(self,order_id):
        try:
            self.api.cancel_order(order_id)
            return f'Order {order_id} has successfully been cancelled'
        except Exception as e:
            print(f'Error cancelling order: {e}')

    def list_all_orders(self, status='all'):
        try:
            orders = self.api.list_orders(status=status)
            return orders
        except Exception as e:
            print(f'Error listing the orders: {e}')
            return None

    def get_account_info(self):
        try:
            account = self.api.get_account()
            return account
        except Exception as e:
            print(f'Error getting account information: {e}')

    def get_cash(self):
        try:
            accountInformation = self.get_account_info()
            if accountInformation:
                formattedAmount = "$"+str(accountInformation.cash)
                return formattedAmount
            else:
                print("Unable to retrieve account information")
                return None
        except Exception as e:
            print(f'Error getting cash amount: {e}')
            return None



