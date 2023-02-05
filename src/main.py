import threading
import time

import pandas as pd

from lib.trade_app import TradeApp
from lib.helper import *


def main():
    """Function that run the entire trading app """
    app = TradeApp()
    app.connect(host='127.0.0.1', port=7497,
                clientId=23)  # port 4002 for ib gateway paper trading/7497 for TWS paper trading
    con_thread = threading.Thread(target=app.run, daemon=True)
    con_thread.start()
    time.sleep(5)

    tickers = ["FB", "AMZN", "INTC", "MSFT", "AAPL", "GOOG", "CSCO", "CMCSA", "ADBE", "NVDA",
               "NFLX", "PYPL", "AMGN", "AVGO", "TXN", "CHTR", "QCOM", "GILD", "FISV", "BKNG",
               "INTU", "ADP", "CME", "TMUS", "MU"]

    capital = 1000

    app.reqPositions()
    time.sleep(2)
    pos_df = app.pos_df
    pos_df.drop_duplicates(inplace=True, ignore_index=True)  # position callback tends to give duplicate values
    app.reqOpenOrders()
    time.sleep(2)

    for ticker in tickers:
        print("starting passthrough for.....", ticker)
        app.req_hist_data(tickers.index(ticker), contract(ticker), '1 M', '15 mins')
        time.sleep(5)
        # df = app.get_stock_df(tickers, ticker)




if __name__ == '__main__':
    main()
