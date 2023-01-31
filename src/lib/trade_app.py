from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.contract import Contract
from ibapi.order import Order
import pandas as pd


class TradeApp(EWrapper, EClient):
    def __init__(self):
        EClient.__init__(self, self)
        self.data = {}
        self.pos_df = pd.DataFrame(columns=['Account', 'Symbol', 'SecType',
                                            'Currency', 'Position', 'Avg cost'])

        self.order_df = pd.DataFrame(columns=['PermId', 'ClientId', 'OrderId',
                                              'Account', 'Symbol', 'SecType',
                                              'Exchange', 'Action', 'OrderType',
                                              'TotalQty', 'CashQty', 'LmtPrice',
                                              'AuxPrice', 'Status'])

    def historicalData(self, req_id, bar):
        # print(f'Time: {bar.date}, Open: {bar.open}, Close: {bar.close}')
        if req_id not in self.data:
            self.data[req_id] = [
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume}]
        else:
            self.data[req_id].append(
                {"Date": bar.date, "Open": bar.open, "High": bar.high, "Low": bar.low, "Close": bar.close,
                 "Volume": bar.volume})

    def nextValidId(self, order_id):
        super().nextValidId(order_id)
        self.nextValidOrderId = order_id
        print("NextValidId:", order_id)

    def position(self, account, contract, position, avg_cost):
        super().position(account, contract, position, avg_cost)
        dictionary = {"Account": account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Currency": contract.currency, "Position": position, "Avg cost": avg_cost}
        self.pos_df = self.pos_df.append(dictionary, ignore_index=True)

    def positionEnd(self):
        print("Latest position data extracted")

    def openOrder(self, order_id, contract, order, order_state):
        super().openOrder(order_id, contract, order, order_state)
        dictionary = {"PermId": order.permId, "ClientId": order.clientId, "OrderId": order_id,
                      "Account": order.account, "Symbol": contract.symbol, "SecType": contract.secType,
                      "Exchange": contract.exchange, "Action": order.action, "OrderType": order.orderType,
                      "TotalQty": order.totalQuantity, "CashQty": order.cashQty,
                      "LmtPrice": order.lmtPrice, "AuxPrice": order.auxPrice, "Status": order_state.status}
        self.order_df = self.order_df.append(dictionary, ignore_index=True)

    def hist_data(self, req_num: str, contract: Contract, duration: str, candle_size):
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
