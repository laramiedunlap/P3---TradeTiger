import os
from pathlib import Path
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi

load_dotenv()

class alpaca:
    API_KEY = "<Your API Key>"
    API_SECRET = "<Your Secret Key>"
    BASE_URL = "https://paper-api.alpaca.markets"
    alpaca_trader:tradeapi = None
    account = None
    def __init__(self):
        self.API_KEY = os.getenv("APCA_API_KEY_ID")
        self.API_SECRET = os.getenv("APCA_API_SECRET_KEY")
        self.BASE_URL = os.getenv("APCA_API_BASE_URL")
        self.alpaca_trader = tradeapi.REST(self.API_KEY, self.API_SECRET, self.BASE_URL)
    def submit_order(
        self,
        symbol: str,
        qty: float = None,
        side: str = "buy",
        type: str = "market",
        time_in_force: str = "day",
        limit_price: str = None,
        stop_price: str = None,
        client_order_id: str = None,
        extended_hours: bool = None,
        order_class: str = None,
        take_profit: dict = None,
        stop_loss: dict = None,
        trail_price: str = None,
        trail_percent: str = None,
        notional: float = None
    ):
        """
        @ https://github.com/alpacahq/alpaca-trade-api-python/blob/master/alpaca_trade_api/rest.py
        :param symbol: symbol or asset ID
        :param qty: float. Mutually exclusive with "notional".
        :param side: buy or sell
        :param type: market, limit, stop, stop_limit or trailing_stop
        :param time_in_force: day, gtc, opg, cls, ioc, fok
        :param limit_price: str of float
        :param stop_price: str of float
        :param client_order_id:
        :param extended_hours: bool. If true, order will be eligible to execute
               in premarket/afterhours.
        :param order_class: simple, bracket, oco or oto
        :param take_profit: dict with field "limit_price" e.g
               {"limit_price": "298.95"}
        :param stop_loss: dict with fields "stop_price" and "limit_price" e.g
               {"stop_price": "297.95", "limit_price": "298.95"}
        :param trail_price: str of float
        :param trail_percent: str of float
        :param notional: float. Mutually exclusive with "qty".
        """
        return self.alpaca_trader.submit_order(
            symbol,qty,side,type,time_in_force,limit_price,stop_price,
            client_order_id,extended_hours,order_class,take_profit,stop_loss,
            trail_price,trail_percent,notional
        )
    def list_posistions(self):
        return self.alpaca_trader.list_posistions()
    
    def current_price(self,symbol):
        return self.alpaca_trader.get_bars(symbol,'1Min',limit=1).df['close'][0]
    

"""  
OrderExample({
    'asset_class': 'crypto',
    'asset_id': '64bbff51-59d6-4b3c-9351-13ad85e3c752',
    'canceled_at': None,
    'client_order_id': '4bb3ad77-6f62-4cfb-9cac-001f1458e39c',
    'commission': '60.264',
    'created_at': '2022-06-29T19:20:20.809126584Z',
    'expired_at': None,
    'extended_hours': False,
    'failed_at': None,
    'filled_at': None,
    'filled_avg_price': None,
    'filled_qty': '0',
    'hwm': None,
    'id': 'c1ec6bc9-a346-4c29-9e7e-054a86c1b9f9',
    'legs': None,
    'limit_price': None,
    'notional': None,
    'order_class': '',
    'order_type': 'market',
    'qty': '1',
    'replaced_at': None,
    'replaced_by': None,
    'replaces': None,
    'side': 'buy',
    'source': None,
    'status': 'pending_new',
    'stop_price': None,
    'submitted_at': '2022-06-29T19:20:20.808309584Z',
    'subtag': None,
    'symbol': 'BTC/USD',
    'time_in_force': 'day',
    'trail_percent': None,
    'trail_price': None,
    'type': 'market',
    'updated_at': '2022-06-29T19:20:20.809254364Z'
})
Account({
    'account_blocked': False,
    'account_number': 'PA3717PJAYWN',
    'accrued_fees': '0',
    'buying_power': '1645434.1767681126',
    'cash': '742009.3924890563',
    'created_at': '2022-04-19T17:46:03.68585Z',
    'crypto_status': 'ACTIVE',
    'currency': 'USD',
    'daytrade_count': 1,
    'daytrading_buying_power': '0',
    'equity': '903424.7842790563',
    'id': 'ee302827-4ced-4321-b5fb-71080392d828',
    'initial_margin': '80707.695895',
    'last_equity': '916328.80490268234',
    'last_maintenance_margin': '3317.19',
    'long_market_value': '161415.39179',
    'maintenance_margin': '161415.39179',
    'multiplier': '2',
    'non_marginable_buying_power': '742009.39',
    'pattern_day_trader': False,
    'pending_transfer_in': '0',
    'portfolio_value': '903424.7842790563',
    'regt_buying_power': '1645434.1767681126',
    'short_market_value': '0',
    'shorting_enabled': True,
    'sma': '818449.81',
    'status': 'ACTIVE',
    'trade_suspended_by_user': False,
    'trading_blocked': False,
    'transfers_blocked': False
})
"""