# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 00:57:46 2018

@author: vttqh
"""
import math, ReadFile, os, glob, datetime
from CLASS import Stock
from sklearn.linear_model import LinearRegression
from matplotlib import pyplot
import numpy as np
import networkx as nx
import planarity
#============================================================================#
class DCCA_Stock(Stock):
    integrated_ts = []
    
    def __init__(self, stock):
        self.ticker = stock.ticker
        self.list_close_price = stock.list_close_price
        self.list_trading_day = stock.list_trading_day
        
    def set_integrated_ts(self, integrated_ts):
        self.integrated_ts = integrated_ts
        
class Segment():
    s1_variance = 0
    s2_variance = 0
    covariance = 0
        
    def set_s1_variance(self, s1_variance):
        self.s1_variance = s1_variance
        
    def set_s2_variance(self, s2_variance):
        self.s2_variance = s2_variance
        
    def set_covariance(self, covariance):
        self.covariance = covariance
#============================================================================#
def calculate_r(time_series):
    r = []
    for i in range(0, len(time_series) - 2):
        difference = math.log(time_series[i], 2.718) - math.log(time_series[i + 1], 2.718)
        r.append(difference)
        
    r.append(0)
    return r

def integrated_timeseries(time_series):
    expected = calculate_expected(time_series)
    integrated = [x - expected for x in time_series]
    return integrated

def calculate_expected(l):
    # INPUT:  l is a list
    # TODO:   Calculate expected
    # OUTPUT: epected value
    total = 0
    for item in l:
        total += item
        
    return total / len(l)

def qdependent_cc_coefficient(dcca_stock_1, dcca_stock_2, Q, S):
    lenght_integrated_ts = min(len(dcca_stock_1.integrated_ts),len(dcca_stock_2.integrated_ts))
    
    #Divide time series into segments of lenght S
    segment_count = int(lenght_integrated_ts / S)
    segments = [Segment()] * segment_count
    for i in range(0, segment_count):
        # Get integrated ts in segment
        s1_integrated = dcca_stock_1.integrated_ts[i * S : i * S + S]
        s2_integrated = dcca_stock_2.integrated_ts[i * S : i * S + S]
    
        s1_rs = calculate_residual_signals(s1_integrated)
        s2_rs = calculate_residual_signals(s2_integrated)
        
        # calculate variance and covariance
        s1_variance = calculate_variance(s1_rs)
        s2_variance = calculate_variance(s2_rs)
        covariance  = (1 / S) * sum(s1_rs[i] * s2_rs[i] for i in range(0, S))
        
        segments[i].set_s1_variance(s1_variance)
        segments[i].set_s2_variance(s2_variance)
        segments[i].set_covariance(covariance)
        
    #Defined the fluctuation functions
    F_covariance  = (1 / segment_count) * sum(np.sign(s.covariance) * abs(s.covariance)**(Q/2) for s in segments)
    F_s1_variance = (1 / segment_count) * sum(s.s1_variance**(Q/2) for s in segments)
    F_s2_variance = (1 / segment_count) * sum(s.s2_variance**(Q/2) for s in segments)
    
    # Retyrn the q-dependent cross-correlation coefficient between stock_1 and stock_2
    return F_covariance / (F_s1_variance * F_s2_variance)**(1/2.0)

def build_crosscorelation_matrix(dcca_stocks, Q, S):
    matrix = np.empty([len(dcca_stocks), len(dcca_stocks)], dtype=np.float)
    for i in range(0, len(dcca_stocks)):
        for j in range(i, len(dcca_stocks)):
            p = qdependent_cc_coefficient(dcca_stocks[i], dcca_stocks[j], Q, S)
            matrix[i][j] = round(p, 6)
            matrix[j][i] = round(p, 5)
            
    return matrix
    
def calculate_trend(time_series):
    numerical_order = [i for i in range(0, len(time_series))]
    numerical_order = np.reshape(numerical_order, (len(numerical_order), 1))
    
    model = LinearRegression()
    model.fit(numerical_order, time_series)
    
    trend = model.predict(numerical_order)
    return trend

def calculate_residual_signals(integrated_ts):
    trend = calculate_trend(integrated_ts)
    residual_signals = [integrated_ts[i] - trend[i] for i in range(0, len(integrated_ts))]
    return residual_signals

def calculate_variance(residual_signals):
    total = sum(i * i for i in residual_signals)
    return (1 / S) * total
    
def sort_graph_edges(G):
    sorted_edges = []
    for source, dest, data in sorted(G.edges(data=True), 
                                     key=lambda x: x[2]['weight'],
                                     reverse=True):
        sorted_edges.append({'source': source, 
                             'dest': dest,
                             'weight': data['weight']})
        print(data['weight'])
    
    return sorted_edges

def compute_PMFG(sorted_edges, nb_nodes):
    PMFG = nx.Graph()
    for edge in sorted_edges:
        PMFG.add_edge(edge['source'], edge['dest'])
        if not planarity.is_planar(PMFG):
            PMFG.remove_edge(edge['source'], edge['dest'])
            
        if len(PMFG.edges()) == 3*(nb_nodes-2):
            break
        
    return PMFG

#============================================================================#
Q = 2
S = 100
begin_day = datetime.date(2009, 6, 1)
end_day = datetime.date(2017, 7, 1)

data_dictionary = os.path.join(os.getcwd(), 'dulieuvnindex')
market_datapath = os.path.join(os.getcwd(), 'excel_^vnindex.csv')

all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))
print("Tong so co phieu la: ", len(all_stocks_filepath))

dcca_stocks = []

for filePath in all_stocks_filepath:
    stock = ReadFile.read_data_stock(filePath)
    
    dcca_stock = DCCA_Stock(stock)
    #Get list_close_price to use
    lcp_to_use = dcca_stock.get_close_price_in_period(begin_day, end_day)
    
    r = calculate_r(lcp_to_use)
    dcca_stock.set_r(r)
    
    integrated_ts = integrated_timeseries(dcca_stock.r)
    dcca_stock.set_integrated_ts(integrated_ts)
    
    dcca_stocks.append(dcca_stock)

nb_nodes = len(dcca_stocks)

c_matrix = build_crosscorelation_matrix(dcca_stocks, Q, S)

complete_graph = nx.Graph()
for i in range(0, nb_nodes):
    for j in range(i+1, nb_nodes):
        complete_graph.add_edge(dcca_stocks[i].ticker, dcca_stocks[j].ticker, weight=c_matrix[i,j])
        
sorted_edges = sort_graph_edges(complete_graph)

PMFG = compute_PMFG(sorted_edges, len(complete_graph.nodes))
print(len(PMFG.edges))
nx.draw(PMFG, with_labels=True)




