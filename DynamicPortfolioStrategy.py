# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:06:37 2018

@author: vttqh
"""

import os, glob, math, datetime
import pandas as pd
import numpy as np
import networkx as nx
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
        self.list_trading_day = list_trading_day
    
    def set_r(self, r):
        self.r = r
        
        
#============================================================================#
def read_detail_stock(filename):
    #TODO: Read stock info from file
    data_in_file = pd.read_csv(filename)
    if len(data_in_file) < 2:
        return None
    
    stock = Stock()
    stock.set_ticker(data_in_file['<Ticker>'].values[0])
    stock.set_close_price(data_in_file['<Close>'].values)
    
    list_day = convert_list_numpy_to_list_datetime(data_in_file['<DTYYYYMMDD>'].values)
    stock.set_list_trading_day(list_day)
    
    r = calculate_r(stock.list_close_price)
    stock.set_r(r)
    return stock

def calculate_r(list):
    r = []
    for i in range(0, len(list) - 1):
        difference = math.log(list[i], 2.718) - math.log(list[i - 1], 2.718)
        r.append(difference)
    r.append(0)
    return r

def convert_list_numpy_to_list_datetime(list):
    list_datetime = []
    
    for day in list:
        string_day = str(day)
        dtime = datetime.date(int(string_day[:4]), int(string_day[4:6]), int(string_day[6:8]))
        list_datetime.append(dtime)
    return list_datetime

def calculate_expected(list):
    expected = 0
    numpy_list = np.array(list, dtype = np.float)
    
    numpy_list *= 1/len(numpy_list)
    
    for item in numpy_list:
        expected += item
    return expected
    
def expected_between2list(list1, list2):
    numpy_list1 = np.array(list1, dtype = np.float)
    numpy_list2 = np.array(list2, dtype = np.float)
    result_list = numpy_list1 * numpy_list2
    return calculate_expected(result_list)
    
def correlation_coefficent(r_stock1, r_stock2):
    expected2list = expected_between2list(r_stock1, r_stock2)
    
    numerator = expected2list - calculate_expected(r_stock1) * calculate_expected(r_stock2)
    denominator = (calculate_expected(np.power(r_stock1, 2)) - calculate_expected(r_stock1)**2) * (calculate_expected(np.power(r_stock2, 2)) - calculate_expected(r_stock2)**2)
    return numerator / math.sqrt(denominator)

def distance_of_2_stock(correlation_coefficent):
    return math.sqrt(2 * (1 - correlation_coefficent))
#============================================================================#
data_dictionary = os.path.join(os.getcwd(), 'dulieucophieu')

# TODO: get all filename .csv
stocks = []
G = nx.Graph()
all_stocks_filename = glob.glob(os.path.join(data_dictionary, "*.csv"))

for i in range(0, 100):
    stock = read_detail_stock(all_stocks_filename[i])
    
    if stock != None and len(stock.list_trading_day) >= 100:
        stocks.append(stock)
        
distance_matrix = np.empty([len(stocks), len(stocks)], dtype=np.float)

for i in range(0, len(stocks)):
    for j in range(i, len(stocks)):
        if i == j:
            distance_matrix[i][j] = 999
        else:
            cc = correlation_coefficent(stocks[i].r[:100], stocks[j].r[:100])
            distance = distance_of_2_stock(cc)
            distance_matrix[i][j] = distance
            distance_matrix[j][i] = distance

for stock in stocks:
    G.add_node(stock.ticker)

test = []

# Build network
for i in range(0, len(distance_matrix)):
    pos_of_min_distance = np.argmin(distance_matrix[i])
    test.append(pos_of_min_distance)
    G.add_edge(stocks[i].ticker, stocks[pos_of_min_distance].ticker, weight=distance_matrix[i][pos_of_min_distance])
    print(stocks[i].ticker," " , stocks[pos_of_min_distance].ticker, " ", distance_matrix[i][pos_of_min_distance], " ", len(G.edges))
    
nx.draw(G)