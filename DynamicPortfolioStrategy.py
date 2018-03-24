# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:06:37 2018

@author: vttqh
"""

import os, glob, math
import pandas as pd
from datetime import date
import numpy as np
#============================================================================#
class Stock():
    ticker = ""
    list_close_price = []
    list_trading_day = []
    r = []
    
    
    def set_ticker(self, ticker):
        self.ticker = ticker
        
    def set_close_price(self, list_close_price):
        self.list_close_price = list_close_price
        
    def set_list_trading_day(self, list_trading_day):
        for day in list_trading_day:
            stringDay = str(day)
            datetime = date(int(stringDay[:4]), int(stringDay[4:6]), int(stringDay[6:8]))
            self.list_trading_day.append(datetime)
            
    def set_r(self, list_close_price):
        for i in range(0, len(list_close_price) - 1):
            difference = math.log(list_close_price[i], 2.718) - math.log(list_close_price[i - 1], 2.718)
            self.r.append(difference)
            
        self.r.append(0)
        
        
#============================================================================#
def read_list_stockID_from_file(filePath):
	theFile = open(filePath, 'r')
	listStockID = theFile.read().split('\n')
	return listStockID

def read_detail_stock(filename):
    data_in_file = pd.read_csv(filename)
    
    stock = Stock()
    stock.set_ticker(data_in_file['<Ticker>'].values[0])
    stock.set_close_price(data_in_file['<Close>'].values)
    stock.set_list_trading_day(data_in_file['<DTYYYYMMDD>'].values)
    stock.set_r(stock.list_close_price)
    
    return stock
        
#============================================================================#
data_dictionary = os.path.join(os.getcwd(), 'dulieucophieu')

# TODO: get all filename .csv 
all_stocks_filename = glob.glob(os.path.join(data_dictionary, "*.csv"))

aaa = read_detail_stock(all_stocks_filename[0])
print(len(aaa.list_trading_day))
print(len(aaa.r))
    