# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:06:37 2018

@author: vttqh
"""

import os, glob
import pandas as pd
#============================================================================#
class Stock():
    ticker = ""
    close_price_history = []
    
    def set_ticker(self, ticker):
        self.ticker = ticker
        
    def set_price_history(self, close_price_history):
        self.close_price_history = close_price_history
        
#============================================================================#
def read_list_stockID_from_file(filePath):
	theFile = open(filePath, 'r')
	listStockID = theFile.read().split('\n')
	return listStockID

def read_detail_stock(filename):
    data_in_file = pd.read_csv(filename)
    
    stock = Stock()
    stock.set_ticker(data_in_file['<Ticker>'].values[0])
    stock.set_price_history(data_in_file['<Close>'].values)
    
    return stock
        
#============================================================================#
data_dictionary = os.path.join(os.getcwd(), 'dulieucophieu')

# TODO: get all filename .csv 
all_stocks_filename = glob.glob(os.path.join(data_dictionary, "*.csv"))

aaa = read_detail_stock(all_stocks_filename[0])
print(aaa.close_price_history)
    