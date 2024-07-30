from alpaca_trade_api.rest import REST, TimeFrame

class OrderManager:
    def __init__(self, api):
        self.api = api

    def place_order(self, symbol, qty, side, order_type, time_in_force):
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

