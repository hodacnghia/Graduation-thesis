# -*- coding: utf-8 -*-
"""
Created on Sat Mar 24 11:06:37 2018

@author: vttqh
"""

import os
import glob
import math
import datetime
import sys
import random
import ReadFile
import pandas as pd
import numpy as np
import networkx as nx
from operator import attrgetter
from CLASS import Stock, MarketIndex
#============================================================================#


class Vertex():
    label = ""
    degree = 0
    c = 0
    distance = 0
    correlation = 0

    def set_label(self, label):
        self.label = label

    def set_degree(self, degree):
        self.degree = degree

    def set_c(self, c):
        self.c = c

    def set_distance(self, distance):
        self.distance = distance

    def set_correlation(self, correlation):
        self.correlation = correlation


class MarketCondition():
    rd = 0
    rf = 0

    def set_rd(self, rd):
        self.rd = rd

    def set_rf(self, rf):
        self.rf = rf

#============================================================================#


def calculate_r(list):
    r = []
    for i in range(0, len(list) - 1):
        difference = math.log(list[i] + 0.01, 2.718) - math.log(list[i + 1] + 0.01, 2.718)
        r.append(difference)
    r.append(0)
    return r


def calculate_expected(l):
    # INPUT: list is logarithmic return of stock
    # TODO: Calculate expected of stock
    expected = 0

    for item in l:
        expected += item
    return expected / len(l)


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

    numerator = expected2list - \
        calculate_expected(stock1_in_st['r']) * \
        calculate_expected(stock2_in_st['r'])
    denominator = (calculate_expected(np.power(stock1_in_st['r'], 2)) - calculate_expected(stock1_in_st['r'])**2) * (
        calculate_expected(np.power(stock2_in_st['r'], 2)) - calculate_expected(stock2_in_st['r'])**2)
    return numerator / math.sqrt(denominator)


def distance_of_2_stock(correlation_coefficent):
    return math.sqrt(2 * abs(1 - correlation_coefficent))


def calculate_correlation_cofficent_by_distance(distance):
    return (2 - distance * distance) / 2


def build_distance_matrix(stocks, selection_horizon):
    # TODO: calculate distance matrix depend on time of selection horizon

    distance_matrix = np.empty([len(stocks), len(stocks)], dtype=np.float)

    for i in range(0, len(stocks)):
        for j in range(i, len(stocks)):
            if i == j:
                distance_matrix[i][j] = 999
            else:
                #selection_horizon = {'trading_days':trading_days, 'close_prices':close_prices}
                start_day = selection_horizon['trading_days'][len(
                    selection_horizon['trading_days']) - 1]
                end_day = selection_horizon['trading_days'][0]

                r_of_stock_i = stocks[i].get_r_in_period(start_day, end_day)
                trading_day_of_stock_i = stocks[i].get_trading_day_in_period(
                    start_day, end_day)
                stock_i_in_period = {
                    'trading_days': trading_day_of_stock_i, 'r': r_of_stock_i}

                r_of_stock_j = stocks[j].get_r_in_period(start_day, end_day)
                trading_day_of_stock_j = stocks[j].get_trading_day_in_period(
                    start_day, end_day)
                stock_j_in_period = {
                    'trading_days': trading_day_of_stock_j, 'r': r_of_stock_j}

                cc = correlation_coefficent(
                    stock_i_in_period, stock_j_in_period)
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


def prim(distance_matrix, start=0):
    global key, free, parent
    number_of_vertices = len(stocks)
    key = number_of_vertices * [sys.maxsize]
    free = number_of_vertices * [True]
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

    u = 0

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
            shortest_path = nx.shortest_path(
                graph, nodes[pos_node_i], nodes[pos_node_j])

            for pos_node_k in range(0, len(nodes)):
                if nodes[pos_node_k] != nodes[pos_node_i] and nodes[pos_node_k] != nodes[pos_node_j]:
                    if nodes[pos_node_k] in shortest_path:
                        list_bc[pos_node_k] += 1 / len(shortest_path)
    return list_bc


def calculate_correlation(graph):
    nodes = list(graph.node)
    list_correlation = [0] * len(nodes)

    for pos_node in range(0, len(nodes)):
        label_of_node = nodes[pos_node]
        neighbors = list(graph.neighbors(label_of_node))

        for label_of_neighbor in neighbors:
            distance = graph[label_of_node][label_of_neighbor]['weight']
            list_correlation[pos_node] += calculate_correlation_cofficent_by_distance(
                distance)

    return list_correlation


def calculate_distance(graph):
    nodes = list(graph.node)
    list_distance = [0] * len(nodes)

    for pos_node in range(0, len(nodes)):
        label_of_node = nodes[pos_node]
        neighbors = list(graph.neighbors(label_of_node))

        for label_of_neighbor in neighbors:
            distance = graph[label_of_node][label_of_neighbor]['weight']
            list_distance[pos_node] += distance
        list_distance[pos_node] /= len(neighbors)

    return list_distance


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


def sort_vertices(graph, vertices, sort_by):
    # TODO: Sort vertices by properties
    # INPUT: vertices: list vertex, sort_by: attribute want to sort by
    # OUTPUT: vertices after sort
    if sort_by == BY_DEGREE:
        vertices = sorted(vertices, key=lambda v: (v.degree))

    elif sort_by == BY_C:
        vertices = sorted(vertices, key=lambda v: (v.c))

    elif sort_by == BY_D_DEGREE:
        # v_n_d is list dictionary contain vertex and distance to vertex have largest degree
        v_n_d = []
        v_largest = max(vertices, key=attrgetter('degree'))
        spl = dict(nx.all_pairs_dijkstra_path_length(graph))

        for v in vertices:
            distance = spl[v.label][v_largest.label]
            v_n_d.append({'vertex': v, 'd_to_largest': distance})
        v_n_d = sorted(v_n_d, key=lambda v: (v['d_to_largest']), reverse=True)

        vertices = []
        for vd in v_n_d:
            vertices.append(vd['vertex'])

    elif sort_by == BY_CORRELATION:
        # v_n_d is list dictionary contain vertex and distance to vertex have largest total correlation
        v_n_d = []
        v_largest = max(vertices, key=attrgetter('correlation'))
        spl = dict(nx.all_pairs_dijkstra_path_length(graph))

        for v in vertices:
            distance = spl[v.label][v_largest.label]
            v_n_d.append({'vertex': v, 'd_to_largest': distance})
        v_n_d = sorted(v_n_d, key=lambda v: (v['d_to_largest']), reverse=True)

        vertices = []
        for vd in v_n_d:
            vertices.append(vd['vertex'])
        v_n_d = []
        v_smallest = min(vertices, key=attrgetter('distance'))
        spl = dict(nx.all_pairs_dijkstra_path_length(graph))

        for v in vertices:
            distance = spl[v.label][v_smallest.label]
            v_n_d.append({'vertex': v, 'd_to_smallest': distance})
        v_n_d = sorted(v_n_d, key=lambda v: (v['d_to_smallest']), reverse=True)

        vertices = []
        for vd in v_n_d:
            vertices.append(vd['vertex'])

    return vertices


def portfolio_selection(stocks, index_selection_horizon):
    distance_matrix = build_distance_matrix(stocks, index_selection_horizon)
    G = build_MST(distance_matrix)

    vertices = []
    nodes = list(G.nodes)

    list_bc = calculate_betweenness_centrality(G)
    list_correlation = calculate_correlation(G)
    list_distance = calculate_distance(G)

    for i in range(0, len(nodes)):
        v = Vertex()
        v.set_label(nodes[i])
        v.set_degree(G.degree(nodes[i]))
        v.set_c(list_bc[i])
        v.set_correlation(list_correlation[i])
        v.set_distance(list_distance[i])
        vertices.append(v)

    vertices = sort_vertices(G, vertices, BY_C)

    ten_percent = int(len(vertices) / 10)
    peripheral_vertices = vertices[:ten_percent]
    central_vertices = vertices[-ten_percent:]

    central_portfolios = []
    peripheral_portfolios = []

    for v in central_vertices:
        stock = next((s for s in stocks if s.ticker == v.label), None)
        central_portfolios.append(stock)

    for v in peripheral_vertices:
        stock = next((s for s in stocks if s.ticker == v.label), None)
        peripheral_portfolios.append(stock)

    return {'peripheral': peripheral_portfolios, 'central': central_portfolios}


def get_selection_horizon(market_index, day_t):
    # TODO: get trading days and close prices of market index in period
    # OUTPUT: A dictionary contains list trading days and close prices in period from day_t - 10 month to day_t
    np_list_trading_day = np.array(market_index.list_trading_day)

    days_of_10month = 300
    first_day = day_t - datetime.timedelta(days=days_of_10month)

    trading_days = np_list_trading_day[np.logical_and(
        np_list_trading_day >= first_day, np_list_trading_day < day_t)]
    close_prices = market_index.list_close_price[np.logical_and(
        np_list_trading_day >= first_day, np_list_trading_day < day_t)]

    selection_horizon = {'trading_days': trading_days,
                         'close_prices': close_prices}
    return selection_horizon


def calculate_average_return(price_history):
    # TODO: Calculate profit of stock
    # INPUT: Price history is a list of price
    #OUTPUT: Profit
    total_profit = 0

    for i in range(0, len(price_history) - 1):
        total_profit = price_history[i + 1] - price_history[i]

    return total_profit / (len(price_history) - 1)


def total_AR_of_portfolios_in_period(portfolios, amount_per_share, start_day, end_day):
    # TODO: calculate total average return of all stocks of portfolios in period
    # INPUT: portfolios is set of stock, start_day is the date begin invest , end_day is the date finish invest
    # OUTPUT: total average return
    total_AR = 0
    for stock in portfolios:
        price_history = stock.get_close_price_in_period(start_day, end_day)
        
        stock_price = price_history[0]
        shares_purchased = amount_per_share / stock_price
        
        total_AR += calculate_average_return(price_history) * shares_purchased
        
    return total_AR

def market_condition_in_period(market_index, begin_day, end_day):
    list_price = market_index.get_close_price_in_period(begin_day, end_day)

    mc = MarketCondition()
    mc.set_rd(calculate_trading_day_criterion(list_price))
    mc.set_rf(calculate_amplitude_criterion(list_price))
    return mc


def portfolio_strategy(day_t, random_portfolios):
    # TODO: Get central and periperal in selection horizol [day_t - 10mond, day_t]
    days_of_10month = 300
    selection_mc = market_condition_in_period(
        market_index, day_t - datetime.timedelta(days=days_of_10month), day_t)
    index_selection_horizon = get_selection_horizon(market_index, day_t)
    portfolios = portfolio_selection(stocks, index_selection_horizon)
    # End

    # Calculate profit in investment horizol
    number_of_investment_days = 90
    last_investment_day = day_t + \
        datetime.timedelta(days=number_of_investment_days)
    investment_mc = market_condition_in_period(
        market_index, day_t + datetime.timedelta(days=1), last_investment_day)

    total_AR_of_central = total_AR_of_portfolios_in_period(
        portfolios['central'], AMOUNT_PER_SHARE, day_t + datetime.timedelta(days=1), last_investment_day)
    total_AR_of_peripheral = total_AR_of_portfolios_in_period(
        portfolios['peripheral'], AMOUNT_PER_SHARE, day_t + datetime.timedelta(days=1), last_investment_day)
    total_AR_of_random = total_AR_of_portfolios_in_period(
        random_portfolios, AMOUNT_PER_SHARE, day_t + datetime.timedelta(days=1), last_investment_day)
    # End

    return {'selection_mc': selection_mc, 'investment_mc': investment_mc, 'day_t': day_t, 'last_investment_day': last_investment_day,
            'central_portfolios': portfolios['central'], 'total_AR_of_central': total_AR_of_central,
            'peripheral_portfolios': portfolios['peripheral'], 'total_AR_of_peripheral': total_AR_of_peripheral,
            'random_portfolios': random_portfolios, 'total_AR_of_random': total_AR_of_random}


def classify_to_combinations_of_MC(list_result):
    # INPUT:  The list of dictionary contains the information and the results of the investment
    # TODO:   Classify the samples of returns of selected portfolios to the 9 combinations of market conditions
    # OUTPUT: Dictionary contains classified samples
    samples_were_classified = {}

    for d in list_result:
        combination = combination_of_MC(
            d['selection_mc'].rd, d['investment_mc'].rd)

        if combination == 'DD':
            samples_were_classified['DD'] = samples_were_classified.get('DD', [
            ])
            samples_were_classified['DD'].append(d)
        if combination == 'DS':
            samples_were_classified['DS'] = samples_were_classified.get('DS', [
            ])
            samples_were_classified['DS'].append(d)
        if combination == 'DU':
            samples_were_classified['DU'] = samples_were_classified.get('DU', [
            ])
            samples_were_classified['DU'].append(d)
        if combination == 'SD':
            samples_were_classified['SD'] = samples_were_classified.get('SD', [
            ])
            samples_were_classified['SD'].append(d)
        if combination == 'SS':
            samples_were_classified['SS'] = samples_were_classified.get('SS', [
            ])
            samples_were_classified['SS'].append(d)
        if combination == 'SU':
            samples_were_classified['SU'] = samples_were_classified.get('SU', [
            ])
            samples_were_classified['SU'].append(d)
        if combination == 'UD':
            samples_were_classified['UD'] = samples_were_classified.get('UD', [
            ])
            samples_were_classified['UD'].append(d)
        if combination == 'US':
            samples_were_classified['US'] = samples_were_classified.get('US', [
            ])
            samples_were_classified['US'].append(d)
        if combination == 'UU':
            samples_were_classified['UU'] = samples_were_classified.get('UU', [
            ])
            samples_were_classified['UU'].append(d)

    return samples_were_classified


def train_to_find_OPS(market_name, start_day, end_day):
    # TODO: Training to find the optimal portfolio strategy in each combination of market conditions between start_day and end_day
    # INPUT: Stocks: information of all stocks, start_day: the date begin traing, end_day: the date complete traning
    # OUTPUT: The dictionary contains key is ombination of market conditions and value is optimal portfolio

    optimal_portfolios_in_MC = {}
    random_portfolios = random.sample(stocks, int(len(stocks) / 10))

    DPS = []
    day_t = start_day

    while(day_t <= end_day):
        print(day_t)
        infomation_ps = portfolio_strategy(day_t, random_portfolios)
        DPS.append(infomation_ps)
        day_t += datetime.timedelta(days=30)

    samples_were_classified = classify_to_combinations_of_MC(DPS)

    total_profit_optimal = 0
    total_profit_central = 0
    total_profit_peripheral = 0
    total_profit_random = 0

    savepath = os.path.join(os.getcwd(), 'resultDPS',
                            market_name + '_train.txt')
    ff = open(savepath, 'w')

    for key, value in samples_were_classified.items():
        combination_mc = str(key)
        ff.write("Combination market condition: " + combination_mc + "\n")

        for v in value:
            if str(key) == 'DS' or str(key) == 'SU':
                total_profit_optimal += v['total_AR_of_central']
            else:
                total_profit_optimal += v['total_AR_of_peripheral']

            total_profit_central += v['total_AR_of_central']
            total_profit_peripheral += v['total_AR_of_peripheral']
            total_profit_random += v['total_AR_of_random']

            ff.write('{\n')
            ff.write('day_t: \'' + str(v['day_t']) + "\',\n")
            ff.write('total_AR_of_central_portfolios: ' +
                     str(v['total_AR_of_central']) + ",\n")
            ff.write('total_AR_of_peripheral_portfolios: ' +
                     str(v['total_AR_of_peripheral']) + ",\n")
            ff.write('total_AR_of_random_portfolios: ' +
                     str(v['total_AR_of_random']) + ",\n")
            ff.write('rd_of_MC_in_selection_horizon: ' +
                     str(v['selection_mc'].rd) + ",\n")
            ff.write('rd_of_MC_in_investment_horizon: ' +
                     str(v['investment_mc'].rd) + ",\n")
            ff.write('rf_of_MC_in_selection_horizon: ' +
                     str(v['selection_mc'].rf) + ",\n")
            ff.write('rf_of_MC_in_investment_horizon: ' +
                     str(v['investment_mc'].rf) + ",\n")
            ff.write('},\n')
        ff.write("================\n")

    ff.write('Profit of optimal: ' + str(total_profit_optimal) + '\n')
    ff.write('Profit of central: ' + str(total_profit_central) + '\n')
    ff.write('Profit of peripheral: ' + str(total_profit_peripheral) + '\n')
    ff.write('Profit of random: ' + str(total_profit_random) + '\n')
    ff.close()

def combination_of_MC(selection_mc, investment_mc):
    # TODO: compare to return combination of market condition
    # INPUT: mc_in_selection, mc_in_investment is float number
    # OUTPUT: combination of market condition

    if selection_mc < 0.45:
        if investment_mc < 0.45:
            return 'DD'
        elif investment_mc < 0.55:
            return 'DS'
        else:
            return 'DU'
    elif selection_mc < 0.55:
        if investment_mc < 0.45:
            return 'SD'
        elif investment_mc < 0.55:
            return 'SS'
        else:
            return 'SU'
    else:
        if investment_mc < 0.45:
            return 'UD'
        elif investment_mc < 0.55:
            return 'US'
        else:
            return 'UU'


#============================================================================#
os.makedirs('resultDPS', exist_ok=True)
BY_DEGREE = 1
BY_C = 2
BY_D_DEGREE = 3
BY_CORRELATION = 4
BY_DISTANCE = 5

#số tiền đầu tư cho mỗi cổ phiếu
AMOUNT_PER_SHARE = 1000

'''
print("Please select one of markets below:")
print("1: VNINDEX")
print("2: HNXINDEX")
print("3: NYSE")
print("4: AMEX")
print("5: OLSO BORS")
print("6: Nasdaq")
print("7: AEX")
print("8: CAC40")
print("9: EURO100")
print("10: IBEX35")
print("11: NIKKEI225")
print("12: TSX")
print("13: XU100")
print("14: IPC")
print("15: BOVESPA")
print("16: AustraliaS&P200")
print("17: NZX50")
print("18: Shanghai")
print("19: KOSPI")
print("20: SSEC50")'''


for selected_market in range(1, 13):
    if selected_market == 1:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuvnindex')
        market_datapath = os.path.join(os.getcwd(), 'excel_^vnindex.csv')
        save_result_to = 'BY_CORRELATION_HOSE_10m'
    elif selected_market == 2:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuhnxindex')
        market_datapath = os.path.join(os.getcwd(), 'excel_^hastc.csv')
        save_result_to = 'BY_CORRELATION_HNX_10m'
    elif selected_market == 3:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunyse')
        market_datapath = os.path.join(os.getcwd(), '^NYA.csv')
        save_result_to = 'BY_CORRELATION_NYSE_10m'
    elif selected_market == 4:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuamex')
        market_datapath = os.path.join(os.getcwd(), '^XAX.csv')
        save_result_to = 'BY_CORRELATION_AMEX_10m'
    elif selected_market == 5:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuolsobors')
        market_datapath = os.path.join(os.getcwd(), '^OSEAX.csv')
        save_result_to = 'BY_CORRELATION_OLSOBORS_10m'
    elif selected_market == 6:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunasdaq')
        market_datapath = os.path.join(os.getcwd(), '^IXIC.csv')
        save_result_to = 'BY_CORRELATION_NASDAQ_10m'
    elif selected_market == 7:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunikkei225')
        market_datapath = os.path.join(os.getcwd(), '^N225.csv')
        save_result_to = 'BY_CORRELATION_NIKKEI225_10m'
    elif selected_market == 8:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuTSX')
        market_datapath = os.path.join(os.getcwd(), '^GSPTSE.csv')
        save_result_to = 'BY_CORRELATION_TSX_10m'
    elif selected_market == 9:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuturkey')
        market_datapath = os.path.join(os.getcwd(), '^XU100.csv')
        save_result_to = 'BY_CORRELATION_XU100_10m'
    elif selected_market == 10:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuAustraliaS&P200')
        market_datapath = os.path.join(os.getcwd(), '^AXJO.csv')
        save_result_to = 'BY_CORRELATION_AustraliaS&P200_10m'
    elif selected_market == 11:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuShanghai')
        market_datapath = os.path.join(os.getcwd(), '^SSEC.csv')
        save_result_to = 'BY_CORRELATION_Shanghai_10m'
    elif selected_market == 12:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuKOSPI')
        market_datapath = os.path.join(os.getcwd(), '^KS11.csv')
        save_result_to = 'BY_CORRELATION_KOSPI_10m'
    else:
        print("...")

    # TODO: Read all stocks infomation from files
    all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))
    print("Tong so co phieu la: ", len(all_stocks_filepath))

    stocks = []

    for i in range(0, len(all_stocks_filepath)):
        stock = ReadFile.read_data_stock(all_stocks_filepath[i])
        r = calculate_r(stock.list_close_price)
        stock.set_r(r)

        stocks.append(stock)

    market_index = ReadFile.read_data_marketindex(market_datapath)
    # End

    # Train to find optimal portfolios under each combination of market conditions in period
    start_day_train = datetime.date(2014, 6, 1)
    end_day_train = datetime.date(2017, 6, 1)

    # OPS is dictionary contain key is conbination of market and value is optimal portfolio
    train_to_find_OPS(save_result_to, start_day_train, end_day_train)
