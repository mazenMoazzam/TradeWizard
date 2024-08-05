from alpaca_trade_api.rest import REST, TimeFrame
from twilio.rest import Client
from models import Order, session


class OrderManager:
    def __init__(self, api, twilio_sid, twilio_auth_token, twilio_phone_number):
        self.api = api
        self.twilio_client = Client(twilio_sid, twilio_auth_token)
        self.twilio_phone_number = twilio_phone_number
        self.notifyNumber = '+14043885784'

    def send_sms_notification(self, number, message):
        try:
            message = self.twilio_client.messages.create(
                body=message,
                from_=self.twilio_phone_number,
                to=number
            )
            return message.sid
        except Exception as e:
            print(f'Error sending SMS notification: {e}')
            return None

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
            if self.notifyNumber:
                message = f'Order placed: {"Bought" if side == "buy" else "Sold"} {qty} {symbol} shares at {order_type}'
                self.send_sms_notification(self.notifyNumber, message)

            db_order = Order(
                id=order.id,
                symbol=order.symbol,
                qty=order.qty,
                side=order.side,
                order_type=order.type,
                status=order.status,
                created_at=order.created_at,
                filled_at=None
            )
            session.add(db_order)
            session.commit()
            return {
                'order_id': order.id,
                'symbol': order.symbol,
                'qty': order.qty,
                'side': order.side,
                'order_type': order.type,
                'status': order.status,
                'created_at': order.created_at
            }
        except Exception as e:
            print(f"Error placing order: {e}")
            return None

    def cancel_order(self, order_id):
        try:
            self.api.cancel_order(order_id)
            message = f'Order {order_id} has successfully been cancelled'
            self.send_sms_notification(self.notifyNumber, message)
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

    def get_positions(self):
        try:
            positions = self.api.list_positions()
            return positions
        except Exception as e:
            print(f'Error getting positions: {e}')
            return None

    def update_order(self, order_id, qty=None, time_in_force=None):
        try:
            order = self.api.replace_order(
                    order_id=order_id,
                    qty=qty,
                    time_in_force=time_in_force
            )
            message = f'Order: {order_id} has been updated successfully!'
            self.send_sms_notification(self.notifyNumber, message)
        except Exception as e:
            print(f'Error updating order: {e}')
            return None

    def retrieve_order_by_id(self,order_id):
        try:
            order = self.api.get_order(order_id)
            return {
                'id': order.id,
                'symbol': order.symbol,
                'qty': order.qty,
                'side': order.side,
                'type': order.type,
                'status': order.status,
                'created at': order.created_at,
                'filled_at': order.filled_at
            }
        except Exception as e:
            print(f'Error retrieving order by ID: {e}')
            return None

    def list_order_history(self, status='all'):
        try:
            orders = self.api.list_orders(status=status)
            order_details = [
                {
                    'id': order.id,
                    'symbol': order.symbol,
                    'qty': order.qty,
                    'side': order.side,
                    'type': order.type,
                    'status': order.status,
                    'created_at': order.created_at,
                    'filled at': order.filled_at
                }
                for order in orders
            ]
            return order_details
        except Exception as e:
            print(f'Error getting order details: {e}')
            return None

    def fetch_orders_from_db(self):
        try:
            orders = session.query(Order).all()
            for order in orders:
                print(f'Order ID: {order.id}, Symbol: {order.symbol}, Quantity: {order.qty}, Side: {order.side}, Type: {order.type}')
        except Exception as e:
            print(f'Error fetching orders: {e}')


