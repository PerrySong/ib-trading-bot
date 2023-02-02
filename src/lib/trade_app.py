from ibapi.client import EClient
from ibapi.common import BarData
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import pandas as pd
from decimal import *


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        # { reqId : [{"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
        #                  "Volume": bar.volume}] }
        #
        self.hist_data = {}
        self.pos_df = pd.DataFrame(columns=['Account', 'Symbol', 'SecType',
                                            'Currency', 'Position', 'Avg cost'])

        self.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                              'Account', 'Symbol', 'SecType',
                                              'Exchange', 'Action', 'OrderType',
                                              'TotalQty', 'CashQty', 'LmtPrice',
                                              'AuxPrice', 'Status'])

    def historicalData(self, req_id: int, bar: BarData):
        # print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')
        print("historicalData for reqId: ", req_id)
        if req_id not in self.hist_data:
            self.hist_data[req_id] = [
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume}]
        else:
            self.hist_data[req_id].append(
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume})

    def historicalDataEnd(self, req_id: int, start: str, end: str):
        print("historicalDataEnd for reqId: ", req_id)

    def historicalDataUpdate(self, req_id: int, bar: BarData):
        print("historicalDataUpdate for reqId: ", req_id)

    def nextValidId(self, order_id):
        super().nextValidId(order_id)
        self.nextValidOrderId = order_id
        print("NextValidId:", order_id)

    def position(self, account: str, contract: Contract, position: Decimal, avg_cost: float):
        """_summary_
                After invoking reqPositions, the positions will then be received through the
                IBApi.EWrapper.position callback

                Args:
                    account (_type_): _description_
                    contract (_type_): _description_
                    position (_type_): _description_
                    avg_cost (_type_): _description_
                """
        super().position(account, contract, position, avg_cost)

        dictionary = {"Account": account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Currency": contract.currency, "Position": position, "Avg cost": avg_cost}
        print("position: ", dictionary)
        self.pos_df = self.pos_df.append(dictionary, ignore_index=True)

    def positionEnd(self):
        print("Latest position data extracted 2")

    def openOrder(self, order_id, contract, order, order_state):
        super().openOrder(order_id, contract, order, order_state)
        dictionary = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": order_id,
                      "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty,
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": order_state.status}
        print("openOrder: ", dictionary)
        self.order_df = self.order_df.append(dictionary, ignore_index=True)

    def openOrderEnd(self):
        print("openOrderEnd.")

    def get_stock_df(self, symbols, symbol):
        """returns extracted historical data in dataframe format"""
        df = pd.DataFrame(self.hist_data[symbols.index(symbol)])
        df.set_index("Date", inplace=True)
        return df

    def req_hist_data(self, req_num: str, contract: Contract, duration: str, candle_size):
        """extracts historical data"""
        self.reqHistoricalData(reqId=req_num,
                               contract=contract,
                               endDateTime='',
                               durationStr=duration,
                               barSizeSetting=candle_size,
                               whatToShow='ADJUSTED_LAST',
                               useRTH=1,
                               formatDate=1,
                               keepUpToDate=0,
                               chartOptions=[])  # EClient function to request contract details
