import threading
import time

import pandas as pd

import sys

filepath = sys.argv[1]


def main():
    df = pd.read_csv(filepath)
    df['Date'] = df.apply(lambda x: '{}-{}-{} {}'.format(str(x['Date'])[:4], str(x['Date'])[4:6], str(x['Date'])[6:8], x['Time']), axis=1)
    df.dropna(how='all')
    df.to_csv(filepath.split('.')[-2] + "_parsed.csv", index=False)


if __name__ == '__main__':
    main()
