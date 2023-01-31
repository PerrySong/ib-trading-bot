from .trade_app import TradeApp
import pandas as pd
from ibapi.contract import Contract
from ibapi.order import Order


def get_data_in_df(trade_app: TradeApp, symbols: str, symbol: str) -> pd.DataFrame:
    """returns extracted historical data in dataframe format"""

    df = pd.DataFrame(trade_app.data[symbols.index(symbol)])
    df.set_index("Date", inplace=True)
    return df


def contract(symbol: str, sec_type: str = "STK", currency: str = "USD", exchange: str = "ISLAND") -> Contract:
    contract = Contract()
    contract.symbol = symbol
    contract.secType = sec_type
    contract.currency = currency
    contract.exchange = exchange
    return contract


def market_order(direction, quantity):
    order = Order()
    order.action = direction
    order.orderType = "MKT"
    order.totalQuantity = quantity
    order.tif = "IOC"
    return order


def stop_order(direction: str, quantity: int, st_price: float) -> Order:
    order = Order()
    order.action = direction
    order.orderType = "STP"
    order.totalQuantity = quantity
    order.auxPrice = st_price
    return order
