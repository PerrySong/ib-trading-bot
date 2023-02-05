import threading
import time

import pandas as pd

from lib.trade_app import TradeApp
from lib.helper import *

import sys


def main(tickers):
    ticker_list = tickers.split(',')
    """Function that run the entire trading app """
    app = TradeApp()
    app.connect(host='127.0.0.1', port=7497,
                clientId=23)  # port 4002 for ib gateway paper trading/7497 for TWS paper trading
    con_thread = threading.Thread(target=app.run, daemon=True)
    con_thread.start()
    time.sleep(5)

    for ticker in ticker_list:
        print("starting passthrough for.....", ticker)
        app.req_hist_data(tickers.index(ticker), contract(ticker), '2 Y', '30 mins')
        time.sleep(35)
        df = app.get_stock_df(ticker_list, ticker)
        df.to_csv("./hist_data/{}_30mins_2y.csv".format(ticker))
    time.sleep(35)
    print("Complete")

if __name__ == '__main__':
    tickers = sys.argv[1]
    main(tickers)
