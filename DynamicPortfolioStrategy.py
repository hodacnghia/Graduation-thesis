# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:06:37 2018

@author: vttqh
"""

import os, glob, math, datetime, sys
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
    
#============================================================================#
def read_detail_stock(filename):
    #TODO: Read stock info from file
    data_in_file = pd.read_csv(filename)
    
    if len(data_in_file) < 2000:
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
    # INPUT: list is logarithmic return of stock
    # TODO: Calculate expected of stock
    
    expected = 0
    numpy_list = np.array(list, dtype = np.float)
    
    numpy_list *= 1/len(numpy_list)
    
    for item in numpy_list:
        expected += item
    return expected
    
def expected_between2list(list1, list2):
    # INPUT: list1, list2 are logarithmic return of stock 1 and stock 2
    # TODO: Calculate expected of 2 stocks
    
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

def calculate_correlation_cofficent_by_distance(distance):
    return (2 - distance*distance)/2

def valid_stock(stock, period_condition):
    if datetime.date.today() - datetime.timedelta(days=period_condition) > stock.list_trading_day[0]:
        return False
    
    for i in range(0, len(stock.list_trading_day) - 1):
        days_after_sub = stock.list_trading_day[i] - datetime.timedelta(days=20)
        
        if days_after_sub > stock.list_trading_day[i+1]:
            return False
    return True

def build_distance_matrix(stocks):
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
            shortest_path = nx.shortest_path(G, nodes[pos_node_i], nodes[pos_node_j])
            
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
        neighbors = list(G.neighbors(label_of_node))
        
        for label_of_neighbor in neighbors:
            distance = G[label_of_node][label_of_neighbor]['weight']
            list_d_correlation[pos_node] += calculate_correlation_cofficent_by_distance(distance)
            
    return list_d_correlation
        
def calculate_d_distance(graph):
    nodes = list(graph.node)
    list_d_distance = [0] * len(nodes)
    
    for pos_node in range(0, len(nodes)):
        label_of_node = nodes[pos_node]
        neighbors = list(G.neighbors(label_of_node))
        
        for label_of_neighbor in neighbors:
            distance = G[label_of_node][label_of_neighbor]['weight']
            list_d_distance[pos_node] += distance
    
    return list_d_distance

#============================================================================#
data_dictionary = os.path.join(os.getcwd(), 'dulieucophieu')

# TODO: get all filename .csv
all_stocks_filename = glob.glob(os.path.join(data_dictionary, "*.csv"))

# TODO: Read all of stocks from files
stocks = []

for i in range(0, len(all_stocks_filename)):
    stock = read_detail_stock(all_stocks_filename[i])
    
    if stock != None:
        if valid_stock(stock, 30):
            stocks.append(stock)

# Build distance matrix
distance_matrix = build_distance_matrix(stocks)

# TODO: Build MST
G = build_MST(distance_matrix)
nx.draw(G, with_labels=True)

list_bc            = calculate_betweenness_centrality(G)
list_d_distance    = calculate_d_distance(G)
list_d_correlation = calculate_d_correlation(G)

vertices = []
nodes = list(G.nodes)

for i in range(0, len(nodes)):
    v = Vertex()
    v.set_label(nodes[i])
    v.set_degree(G.degree(nodes[i]))
    v.set_c(list_bc[i])
    v.set_d_distance(list_d_distance[i])
    v.set_d_correlation(list_d_correlation[i])
    
    vertices.append(v)
    
for v in vertices:
    print(v.label, " ", v.degree, " ", v.c, " ", v.d_correlation, " ", v.d_distance)


