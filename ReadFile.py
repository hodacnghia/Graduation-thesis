# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:34:58 2018

@author: vttqh
"""

import datetime
import pandas as pd

from CLASS import Stock, MarketIndex

def read_data_stock(filepath):
    # TODO: Read stock info from file
    data_in_file = pd.read_csv(filepath)

    stock = Stock()
    stock.set_ticker(data_in_file['<Ticker>'].values[0])
    stock.set_close_price(data_in_file['<Close>'].values)
    list_day = convert_list_numpy_to_list_datetime(data_in_file['<DTYYYYMMDD>'].values)
    stock.set_list_trading_day(list_day)
    #r = calculate_r(stock.list_close_price)
    #stock.set_r(r)
    return stock

def read_data_marketindex(filepath):
    data_in_file = pd.read_csv(filepath)

    market_index = MarketIndex()
    market_index.set_ticker(data_in_file['<Ticker>'].values[0])
    market_index.set_list_close_price(data_in_file['<Close>'].values)
    list_day = convert_list_numpy_to_list_datetime(data_in_file['<DTYYYYMMDD>'].values)
    market_index.set_list_trading_day(list_day)
    return market_index

def convert_list_numpy_to_list_datetime(list):
    list_datetime = []

    for day in list:
        string_day = str(day)
        dtime = datetime.date(int(string_day[:4]), int(string_day[4:6]), int(string_day[6:8]))
        list_datetime.append(dtime)
    return list_datetime