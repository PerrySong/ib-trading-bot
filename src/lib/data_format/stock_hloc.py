import datetime
import backtrader.feeds as btfeed


class StockHLOC(btfeed.GenericCSVData):
    params = (
        ('fromdate', datetime.datetime(1900, 12, 31)),
        ('todate', datetime.datetime(2100, 12, 31)),
        ('nullvalue', 0.0),
        ('dtformat', ('%Y%m%d')),
        ('tmformat', ('%H:%M:%S')),

        ('datetime', 0),
        ('time', 1),
        ('high', 2),
        ('low', 3),
        ('open', 4),
        ('close', 5),
        ('volume', 6),
        ('openinterest', -1)
    )
