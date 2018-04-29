# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:06:37 2018

@author: vttqh
"""

import os, glob, math, datetime, sys, random
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
        
    def get_r_in_period(self, start_day, end_day):
        np_list_trading_day = np.array(self.list_trading_day)
        np_r = np.array(self.r)
        r_in_period = np_r[np.logical_and(np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return r_in_period

    def get_trading_day_in_period(self, start_day, end_day):
        np_list_trading_day = np.array(self.list_trading_day)
        trading_day_in_period = np_list_trading_day[np.logical_and(np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return trading_day_in_period

    def get_close_price_in_period(self, start_day, end_day):
        np_list_trading_day = np.array(self.list_trading_day)
        np_list_close_price = np.array(self.list_close_price)
        close_price_in_period = np_list_close_price[np.logical_and(np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return close_price_in_period

class Vertex():
    label = ""
    degree = 0
    c = 0
    d_distance = 0
    d_correlation = 0
    
    def set_label(self, label):
        self.label = label
        
    def set_degree(self, degree):
        self.degree = degree
    
    def set_c(self, c):
        self.c = c
        
    def set_d_distance(self, d_distance):
        self.d_distance = d_distance
        
    def set_d_correlation(self, d_correlation):
        self.d_correlation = d_correlation
    
class MarketIndex():
    ticker = ""
    list_trading_day = []
    list_close_price = []
    
    def set_ticker(self, ticker):
        self.ticker = ticker
        
    def set_list_trading_day(self, list_trading_day):
        self.list_trading_day = list_trading_day
        
    def set_list_close_price(self, list_close_price):
        self.list_close_price = list_close_price
        
    def get_trading_day_in_period(self, start_day, end_day):
        np_list_trading_day = np.array(self.list_trading_day)
        trading_day_in_period = np_list_trading_day[np.logical_and(np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return trading_day_in_period

    def get_close_price_in_period(self, start_day, end_day):
        np_list_trading_day = np.array(self.list_trading_day)
        np_list_close_price = np.array(self.list_close_price)
        close_price_in_period = np_list_close_price[np.logical_and(np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return close_price_in_period
    
class MarketCondition():
    rd = 0
    rf = 0
    
    def set_rd(self, rd):
        self.rd = rd
        
    def set_rf(self, rf):
        self.rf = rf
    
#============================================================================#
def read_detail_stock(filepath):
    #TODO: Read stock info from file
    data_in_file = pd.read_csv(filepath)
    
    #if len(data_in_file) < 1000:
        #return None
    
    stock = Stock()
    stock.set_ticker(data_in_file['<Ticker>'].values[0])
    stock.set_close_price(data_in_file['<Close>'].values)
    list_day = convert_list_numpy_to_list_datetime(data_in_file['<DTYYYYMMDD>'].values)
    stock.set_list_trading_day(list_day)
    r = calculate_r(stock.list_close_price)
    stock.set_r(r)
    return stock

def read_market_index(filepath):
    #TODO: Read market index from file
    data_in_file = pd.read_csv(filepath)
    
    market_index = MarketIndex()
    market_index.set_ticker(data_in_file['<Ticker>'].values[0])
    market_index.set_list_close_price(data_in_file['<Close>'].values)
    list_day = convert_list_numpy_to_list_datetime(data_in_file['<DTYYYYMMDD>'].values)
    market_index.set_list_trading_day(list_day)
    return market_index

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
    # INPUT: list is logarithmic return of stock
    # TODO: Calculate expected of stock
    expected = 0
    
    for item in list:
        expected += item
    return expected / len(list)
    
def expected_between2list(stock1_in_st, stock2_in_st):
    # INPUT: list1, list2 are logarithmic return of stock 1 and stock 2
    # TODO: Calculate expected of 2 stocks
    list_multi_r_of_2stock = []
    
    if len(stock1_in_st['r']) > len(stock2_in_st['r']):
        longer_list = np.array(stock1_in_st['r'])
        shorter_list = np.array(stock2_in_st['r'])
    else:
        longer_list = np.array(stock2_in_st['r'])
        shorter_list = np.array(stock1_in_st['r'])
    list_multi_r_of_2stock = shorter_list * longer_list[:len(shorter_list)]
    
    for i in range(len(shorter_list), len(longer_list)):
        np.append(list_multi_r_of_2stock, 0)
    
    return calculate_expected(list_multi_r_of_2stock)
        
    
def correlation_coefficent(stock1_in_st, stock2_in_st):
    expected2list = expected_between2list(stock1_in_st, stock2_in_st)
    
    numerator = expected2list - calculate_expected(stock1_in_st['r']) * calculate_expected(stock2_in_st['r'])
    denominator = (calculate_expected(np.power(stock1_in_st['r'], 2)) - calculate_expected(stock1_in_st['r'])**2) * (calculate_expected(np.power(stock2_in_st['r'], 2)) - calculate_expected(stock2_in_st['r'])**2)
    return numerator / math.sqrt(denominator)

def distance_of_2_stock(correlation_coefficent):
    return math.sqrt(2 * (1 - correlation_coefficent))

def calculate_correlation_cofficent_by_distance(distance):
    return (2 - distance * distance) / 2

def valid_stock(stock, period_condition):
    if datetime.date.today() - datetime.timedelta(days=period_condition) > stock.list_trading_day[0]:
        return False
    
    for i in range(0, len(stock.list_trading_day) - 1):
        days_after_sub = stock.list_trading_day[i] - datetime.timedelta(days=20)
        
        if days_after_sub > stock.list_trading_day[i+1]:
            return False
    return True

def build_distance_matrix(stocks, selection_horizon):
    #TODO: calculate distance matrix depend on time of selection horizon  
    
    distance_matrix = np.empty([len(stocks), len(stocks)], dtype=np.float)

    for i in range(0, len(stocks)):
        for j in range(i, len(stocks)):
            if i == j:
                distance_matrix[i][j] = 999
            else:
                #selection_horizon = {'trading_days':trading_days, 'close_prices':close_prices}
                start_day = selection_horizon['trading_days'][len(selection_horizon['trading_days']) - 1]
                end_day   = selection_horizon['trading_days'][0]
                
                r_of_stock_i = stocks[i].get_r_in_period(start_day, end_day)
                trading_day_of_stock_i = stocks[i].get_trading_day_in_period(start_day, end_day)
                stock_i_in_period = {'trading_days':trading_day_of_stock_i, 'r':r_of_stock_i}
                
                r_of_stock_j = stocks[j].get_r_in_period(start_day, end_day)
                trading_day_of_stock_j = stocks[j].get_trading_day_in_period(start_day, end_day)
                stock_j_in_period = {'trading_days':trading_day_of_stock_j, 'r':r_of_stock_j}
                
                cc = correlation_coefficent(stock_i_in_period, stock_j_in_period)
                distance = distance_of_2_stock(cc)
                distance_matrix[i][j] = distance
                distance_matrix[j][i] = distance
    return distance_matrix
 
def build_MST(distance_matrix):
    G = nx.Graph()
    
    for stock in stocks:
        G.add_node(stock.ticker)
    
    prim(distance_matrix)
    
    for i in range(1, len(parent)):
        G.add_edge(stocks[parent[i]].ticker, stocks[i].ticker, weight=key[i])
        
    return G

def prim(distance_matrix, start = 0):
    global key, free, parent
    number_of_vertices = len(stocks)
    key    = number_of_vertices * [sys.maxsize]
    free   = number_of_vertices * [True]
    parent = number_of_vertices * [-1]
    
    key[start] = 0
    
    for i in range(0, number_of_vertices - 1):
        u = extract_min()
        free[u] = False
        
        for v in range(0, number_of_vertices):
            if free[v] and distance_matrix[u][v] < key[v]:
                key[v] = distance_matrix[u][v]
                parent[v] = u
    
def extract_min():
    min = sys.maxsize
    
    for i in range(0, len(stocks)):
        if free[i] == True and key[i] < min:
            min = key[i]
            u = i
            
    return u

def calculate_betweenness_centrality(graph):
    # TODO: calculate betweenness centrality of all node in graph
    nodes = list(graph.node)
    list_bc = [0] * len(nodes)
    
    for pos_node_i in range(0, len(nodes) - 1):
        for pos_node_j in range(pos_node_i + 1, len(nodes)):
            shortest_path = nx.shortest_path(graph, nodes[pos_node_i], nodes[pos_node_j])
            
            for pos_node_k in range(0, len(nodes)):
                if nodes[pos_node_k] != nodes[pos_node_i] and nodes[pos_node_k] != nodes[pos_node_j]:
                    if nodes[pos_node_k] in shortest_path:
                        list_bc[pos_node_k] += 1 / len(shortest_path)
    
    return list_bc

def calculate_d_correlation(graph):
    nodes = list(graph.node)
    list_d_correlation = [0] * len(nodes)
    
    for pos_node in range(0, len(nodes)):
        label_of_node = nodes[pos_node]
        neighbors = list(graph.neighbors(label_of_node))
        
        for label_of_neighbor in neighbors:
            distance = graph[label_of_node][label_of_neighbor]['weight']
            list_d_correlation[pos_node] += calculate_correlation_cofficent_by_distance(distance)
            
    return list_d_correlation
        
def calculate_d_distance(graph):
    nodes = list(graph.node)
    list_d_distance = [0] * len(nodes)
    
    for pos_node in range(0, len(nodes)):
        label_of_node = nodes[pos_node]
        neighbors = list(graph.neighbors(label_of_node))
        
        for label_of_neighbor in neighbors:
            distance = graph[label_of_node][label_of_neighbor]['weight']
            list_d_distance[pos_node] += distance
        list_d_distance[pos_node] /= len(neighbors)
        
    return list_d_distance

def calculate_trading_day_criterion(list_close_price):
    count = 0
    
    for i in range(0, len(list_close_price) - 1):
        if list_close_price[i] > list_close_price[i + 1]:
            count += 1
    return count / len(list_close_price)

def calculate_amplitude_criterion(list_close_price):
    numerator = 0
    denominator = 0
    
    for i in range(0, len(list_close_price) - 1):
        if list_close_price[i] > list_close_price[i + 1]:
            numerator += list_close_price[i] - list_close_price[i + 1]
        denominator += abs(list_close_price[i] - list_close_price[i + 1])
    return numerator / denominator

def portfolio_selection(stocks, index_selection_horizon):
    distance_matrix = build_distance_matrix(stocks, index_selection_horizon)
    G = build_MST(distance_matrix)
    #nx.draw(G, with_labels = True)
    
    vertices = []
    nodes = list(G.nodes)

    list_bc            = calculate_betweenness_centrality(G)
    list_d_correlation = calculate_d_correlation(G)
    list_d_distance    = calculate_d_distance(G)

    for i in range(0, len(nodes)):
        v = Vertex()
        v.set_label(nodes[i])
        v.set_degree(G.degree(nodes[i]))
        v.set_c(list_bc[i])
        v.set_d_correlation(list_d_correlation[i])
        v.set_d_distance(list_d_distance[i])
        vertices.append(v)

    vertices = sorted(vertices, key = lambda v: (v.degree))

    ten_percent = int(len(vertices) / 10)
    peripheral_portfolios = vertices[:ten_percent]
    central_portfolios = vertices[-ten_percent:]
    return {'peripheral': peripheral_portfolios, 'central': central_portfolios}

def get_selection_horizon(market_index, day_t):
    #TODO: get trading days and close prices of market index in period
    #OUTPUT: A dictionary contains list trading days and close prices in period from day_t - 10 month to day_t
    np_list_trading_day = np.array(market_index.list_trading_day)
    
    days_of_10month = 300
    first_day = day_t - datetime.timedelta(days=days_of_10month)
    
    trading_days = np_list_trading_day[np.logical_and(np_list_trading_day >= first_day, np_list_trading_day < day_t)]
    close_prices = market_index.list_close_price[np.logical_and(np_list_trading_day >= first_day, np_list_trading_day < day_t)]
    
    selection_horizon = {'trading_days':trading_days, 'close_prices':close_prices}
    return selection_horizon

def get_investment_horizon(market_index, day_t):
    #TODO: get trading days and close prices of market index in period
    #OUTPUT: A dictionary contains list trading days and close prices in period from day_t to day_t + 10 month
    np_list_trading_day = np.array(market_index.list_trading_day)
    
    days_of_10month = 300
    last_day = day_t + datetime.timedelta(days=days_of_10month)
    
    trading_days = np_list_trading_day[np.logical_and(np_list_trading_day > day_t, np_list_trading_day <= last_day)]
    close_prices = market_index.list_close_price[np.logical_and(np_list_trading_day > day_t, np_list_trading_day <= last_day)]
    
    investment_horizon = {'trading_days':trading_days, 'close_prices':close_prices}
    return investment_horizon

def calculate_profit(price_history):
    #TODO: Calculate profit of stock
    #INPUT: Price history is a list of price
    #OUTPUT: Profit
    
    return price_history[1] - price_history[-1]

def market_condition_in_period(market_index, begin_day, end_day):
    list_price = market_index.get_close_price_in_period(begin_day, end_day)
    
    mc = MarketCondition()
    mc.set_rd(calculate_trading_day_criterion(list_price))
    mc.set_rf(calculate_amplitude_criterion(list_price))
    return mc

def portfolio_strategy(day_t):
    # TODO: Get central and periperal in selection horizol [day_t - 10mond, day_t]
    days_of_10month = 300
    selection_mc = market_condition_in_period(market_index, day_t - datetime.timedelta(days=days_of_10month), day_t)
    index_selection_horizon = get_selection_horizon(market_index, day_t)
    portfolios = portfolio_selection(stocks, index_selection_horizon)
    # End
    
    # Calculate profit in investment horizol
    profit_of_central = 0
    profit_of_peripheral = 0
    profit_of_random = 0
    
    central_portfolios = []
    peripheral_portfolios = []
    
    last_investment_day = day_t + datetime.timedelta(days=days_of_10month)
    investment_mc= market_condition_in_period(market_index, day_t + datetime.timedelta(days=1), last_investment_day)
    
    for v in portfolios['central']:
        stock = next((s for s in stocks if s.ticker == v.label), None)
        price_history = stock.get_close_price_in_period(day_t + datetime.timedelta(days=1), last_investment_day)
        profit_of_central += calculate_profit(price_history)
        
        central_portfolios.append(stock)
        
    for v in portfolios['peripheral']:
        stock = next((s for s in stocks if s.ticker == v.label), None)
        price_history = stock.get_close_price_in_period(day_t + datetime.timedelta(days=1), last_investment_day)
        profit_of_peripheral += calculate_profit(price_history)
        
        peripheral_portfolios.append(stock)
    # End
    
    # TODO: Get 10% of total stocks and calculate profit of them
    random_portfolios = random.sample(stocks, int(len(stocks)/10))
    
    for stock in random_portfolios:
        price_history = stock.get_close_price_in_period(day_t + datetime.timedelta(days=1), last_investment_day)
        profit_of_random += calculate_profit(price_history)
    # End
    
    # calculate average profit
    central_ap = profit_of_central / len(portfolios['central'])
    peripheral_ap = profit_of_peripheral / len(portfolios['peripheral'])
    random_ap = profit_of_random / len(random_portfolios)
    
    return {'selection_mc':selection_mc, 'investment_mc':investment_mc, 'day_t':day_t, \
            'central_portfolios':central_portfolios, 'central_ap': central_ap, \
            'peripheral_portfolios':peripheral_portfolios, 'peripheral_ap': peripheral_ap, \
            'random_portfolios':random_portfolios, 'random_ap': random_ap}
        
#============================================================================#

data_dictionary = os.path.join(os.getcwd(), 'dulieuhnxindex')

# TODO: Read all stocks infomation from files and read market index
all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))
print("Tổng số cổ phiếu của sàn HOSE: ", len(all_stocks_filepath))

stocks = []

for i in range(0, len(all_stocks_filepath)):
    stock = read_detail_stock(all_stocks_filepath[i])
    stocks.append(stock)

market_index = read_market_index(os.path.join(os.getcwd(), 'excel_^hastc.csv'))
# End

day_t = datetime.date(2011, 1, 1)
DPS = []

while(day_t + datetime.timedelta(days=150) < market_index.list_trading_day[0] ):
    infomation_ps = portfolio_strategy(day_t)
    DPS.append(infomation_ps)
    day_t += datetime.timedelta(days=30)

ff = open('resulthnx.txt', 'w')

for infomation_ps in DPS:
    ff.write("================")
    ff.write("\n")
    ff.write('day_t: ' + str(infomation_ps['day_t']))
    ff.write("\n")
    ff.write('average profit of central portfolios: ' + str(infomation_ps['central_ap']))
    ff.write("\n")
    ff.write('average profit of peripheral portfolios: ' + str(infomation_ps['peripheral_ap']))
    ff.write("\n")
    ff.write('average profit of random portfolios: ' + str(infomation_ps['random_ap']))
    ff.write("\n")
    ff.write('rd of market condition in selection horizon: ' + str(infomation_ps['selection_mc'].rd))
    ff.write("\n")
    ff.write('rd of market condition in investment horizon: ' + str(infomation_ps['investment_mc'].rd))
    ff.write("\n")
    ff.write("================")
    ff.write("\n")

ff.close()