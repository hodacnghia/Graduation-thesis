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
import pandas as pd
import numpy as np
import networkx as nx
from operator import attrgetter
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
        r_in_period = np_r[np.logical_and(
            np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return r_in_period

    def get_trading_day_in_period(self, start_day, end_day):
        np_list_trading_day = np.array(self.list_trading_day)
        trading_day_in_period = np_list_trading_day[np.logical_and(
            np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return trading_day_in_period

    def get_close_price_in_period(self, start_day, end_day):
        np_list_trading_day = np.array(self.list_trading_day)
        np_list_close_price = np.array(self.list_close_price)
        close_price_in_period = np_list_close_price[np.logical_and(
            np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return close_price_in_period


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
        trading_day_in_period = np_list_trading_day[np.logical_and(
            np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
        return trading_day_in_period

    def get_close_price_in_period(self, start_day, end_day):
        np_list_trading_day = np.array(self.list_trading_day)
        np_list_close_price = np.array(self.list_close_price)
        close_price_in_period = np_list_close_price[np.logical_and(
            np_list_trading_day >= start_day, np_list_trading_day <= end_day)]
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
    # TODO: Read stock info from file
    data_in_file = pd.read_csv(filepath)

    stock = Stock()
    stock.set_ticker(data_in_file['<Ticker>'].values[0])
    stock.set_close_price(data_in_file['<Close>'].values)
    list_day = convert_list_numpy_to_list_datetime(
        data_in_file['<DTYYYYMMDD>'].values)
    stock.set_list_trading_day(list_day)
    r = calculate_r(stock.list_close_price)
    stock.set_r(r)
    return stock


def read_market_index_cp68(filepath):
    # TODO: Read market index from cophieu68 download file
    data_in_file = pd.read_csv(filepath)

    market_index = MarketIndex()
    market_index.set_ticker(data_in_file['<Ticker>'].values[0])
    market_index.set_list_close_price(data_in_file['<Close>'].values)
    list_day = convert_list_numpy_to_list_datetime(
        data_in_file['<DTYYYYMMDD>'].values)
    market_index.set_list_trading_day(list_day)
    return market_index


def read_market_index_yf(filepath, ticker):
    # TODO: Read market index from yahoo finance download file
    data_in_file = pd.read_csv(filepath)

    market_index = MarketIndex()
    market_index.set_ticker(ticker)
    market_index.set_list_close_price(data_in_file['Close'].values[::-1])
    list_day = convert_list_string_to_list_datetime(
        data_in_file['Date'].values[::-1])
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
        dtime = datetime.date(int(string_day[:4]), int(
            string_day[4:6]), int(string_day[6:8]))
        list_datetime.append(dtime)
    return list_datetime


def convert_list_string_to_list_datetime(list_date):
    list_datetime = []

    for d in list_date:
        split_d = d.split('-')
        dtime = datetime.date(int(split_d[0]), int(
            split_d[1]), int(split_d[2]))
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

    numerator = expected2list - \
        calculate_expected(stock1_in_st['r']) * \
        calculate_expected(stock2_in_st['r'])
    denominator = (calculate_expected(np.power(stock1_in_st['r'], 2)) - calculate_expected(stock1_in_st['r'])**2) * (
        calculate_expected(np.power(stock2_in_st['r'], 2)) - calculate_expected(stock2_in_st['r'])**2)
    return numerator / math.sqrt(denominator)


def distance_of_2_stock(correlation_coefficent):
    return math.sqrt(2 * (1 - correlation_coefficent))


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
            print(vd['vertex'].label, ' ', vd['d_to_largest'])

    else:
        # BY_DISTANCE
        # v_n_d is list dictionary contain vertex and distance to vertex have smallest mean distance
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


def total_AR_of_portfolios_in_period(portfolios, start_day, end_day):
    # TODO: calculate total average return of all stocks of portfolios in period
    # INPUT: portfolios is set of stock, start_day is the date begin invest , end_day is the date finish invest
    # OUTPUT: total average return
    total_AR = 0
    for stock in portfolios:
        price_history = stock.get_close_price_in_period(start_day, end_day)
        total_AR += calculate_average_return(price_history)
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
    number_of_investment_days = 300
    last_investment_day = day_t + \
        datetime.timedelta(days=number_of_investment_days)
    investment_mc = market_condition_in_period(
        market_index, day_t + datetime.timedelta(days=1), last_investment_day)

    total_AR_of_central = total_AR_of_portfolios_in_period(
        portfolios['central'], day_t + datetime.timedelta(days=1), last_investment_day)
    total_AR_of_peripheral = total_AR_of_portfolios_in_period(
        portfolios['peripheral'], day_t + datetime.timedelta(days=1), last_investment_day)
    total_AR_of_random = total_AR_of_portfolios_in_period(
        random_portfolios, day_t + datetime.timedelta(days=1), last_investment_day)
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

    total_profit_central = 0
    total_profit_peripheral = 0

    ff = open(market_name + '_train.txt', 'w')

    for key, value in samples_were_classified.items():
        ff.write("Combination market condition: " + str(key) + "\n")

        for v in value:
            total_profit_central += v['total_AR_of_central']
            total_profit_peripheral += v['total_AR_of_peripheral']
            ff.write('{\n')
            ff.write('day_t: ' + str(v['day_t']) + ",\n")
            ff.write('total_AR_of_central_portfolios: ' + str(v['total_AR_of_central']) + ",\n")
            ff.write('total_AR_of_peripheral_portfolios: ' + str(v['total_AR_of_peripheral']) + ",\n")
            ff.write('total_AR_of_random_portfolios: ' + str(v['total_AR_of_random']) + ",\n")
            ff.write('rd_of_MC_in_selection_horizon: ' + str(v['selection_mc'].rd) + ",\n")
            ff.write('rd_of_MC_in_investment_horizon: ' + str(v['investment_mc'].rd) + ",\n")
            ff.write('rf_of_MC_in_selection_horizon: ' + str(v['selection_mc'].rf) + ",\n")
            ff.write('rf_of_MC_in_investment_horizon: ' + str(v['investment_mc'].rf) + ",\n")
            ff.write('},\n')
        ff.write("================\n")
    ff.write('Profit of central: ' + str(total_profit_central) + '\n')
    ff.write('Profit of peripheral: ' + str(total_profit_peripheral) + '\n')
    ff.close()

    '''
    # Find optimal portfolios under combination portfolios
    for key, value in samples_were_classified.items():
        profit_of_central = 0
        profit_of_peripheral = 0
        profit_of_random = 0
        
        for v in value:
            profit_of_central += v['total_AR_of_central']
            profit_of_peripheral += v['total_AR_of_peripheral']
            profit_of_random += v['total_AR_of_random']
        
        if profit_of_central >= profit_of_peripheral:
            optimal_portfolios_in_MC[key] = 'central'
        else:
            optimal_portfolios_in_MC[key] = 'peripheral'
                
    return optimal_portfolios_in_MC
    '''


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


def invest_DPS(OPS, market_name, start_day, end_day):
    # TODO: Use dynamic portfolio strategy to invest in period between start_day and end_day
    # INPUT: stocks: all stocks in market, OPS: dictionary with key is conbination of market and value is optimal portfolio
    total_average_return = 0
    day_t = start_day

    ff = open(market_name + '_invest.txt', 'w')

    while day_t < end_day:
        ps = portfolio_strategy(day_t, [])

        combination = combination_of_MC(
            ps['selection_mc'].rd, ps['investment_mc'].rd)

        if combination in OPS.keys():
            optimal_portfolio = OPS[combination]
            average_return_of_portfolio = 0

            if (optimal_portfolio == 'central'):
                average_return_of_portfolio += ps['total_AR_of_central']
            else:
                average_return_of_portfolio += ps['total_AR_of_peripheral']

            total_average_return += average_return_of_portfolio

            ff.write('day_t: ' + str(ps['day_t']) + '\n')
            ff.write('last_investment_day: ' +
                     str(ps['last_investment_day']) + '\n')
            ff.write('optimal portfolios: ' + str(optimal_portfolio) + '\n')
            ff.write('average_return_of_portfolio: ' +
                     str(average_return_of_portfolio) + '\n')

        day_t += datetime.timedelta(days=150)

    ff.write('========================\n')
    ff.write('total_average_return: ' + str(total_average_return))
    ff.close()


#====================================================================15========#
BY_DEGREE = 1
BY_C = 2
BY_D_DEGREE = 3
BY_CORRELATION = 4
BY_DISTANCE = 5


print("Please select one of markets below:")
print("1: VNINDEX")
print("2: HNXINDEX")
print("3: NYSE")
print("4: AMEX")
print("5: OLSO BORS")
print("Default: Nasdaq")
selected_market = input("Select 1 number: ")

if selected_market == '1':
    data_dictionary = os.path.join(os.getcwd(), 'dulieuvnindex')
    market_index = read_market_index_cp68(os.path.join(os.getcwd(), 'excel_^vnindex.csv'))
    market_name = 'HOSE_CP'
elif selected_market == '2':
    data_dictionary = os.path.join(os.getcwd(), 'dulieuhnxindex')
    market_index = read_market_index_cp68(
        os.path.join(os.getcwd(), 'excel_^hastc.csv'))
    market_name = 'HNX_BY_CORRELATION10'
elif selected_market == '3':
    data_dictionary = os.path.join(os.getcwd(), 'dulieunyse')
    market_index = read_market_index_yf(
        os.path.join(os.getcwd(), '^NYA.csv'), 'NYSE')
    market_name = 'NYSE_BY_CORRELATION10'
elif selected_market == '4':
    data_dictionary = os.path.join(os.getcwd(), 'dulieuamex')
    market_index = read_market_index_yf(
        os.path.join(os.getcwd(), '^XAX.csv'), 'AMEX')
    market_name = 'AMEX_BY_CORRELATION10'
elif selected_market == '5':
    data_dictionary = os.path.join(os.getcwd(), 'dulieuolsobors')
    market_index = read_market_index_yf(
        os.path.join(os.getcwd(), '^OSEAX.csv'), 'OLSOBORS')
    market_name = 'OLSOBORS_BY_CORRELATION10'
else:
    data_dictionary = os.path.join(os.getcwd(), 'dulieunasdaq')
    market_index = read_market_index_yf(os.path.join(os.getcwd(), '^IXIC.csv'), 'NASDAQ')
    market_name = 'NASDAQ_CP'
# TODO: Read all stocks infomation from files
all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))
print("Tổng số cổ phiếu là: ", len(all_stocks_filepath))

stocks = []

for i in range(0, len(all_stocks_filepath)):
    stock = read_detail_stock(all_stocks_filepath[i])
    stocks.append(stock)
# End

# Train to find optimal portfolios under each combination of market conditions in period
start_day_train = datetime.date(2015, 6, 1)
end_day_train = datetime.date(2015, 12, 1)

# OPS is dictionary contain key is conbination of market and value is optimal portfolio
OPS = train_to_find_OPS(market_name, start_day_train, end_day_train)


'''
# Investment
start_day_invest = datetime.date(2015, 6, 1)
end_day_invest = datetime.date(2017, 6, 1)

invest_DPS(OPS, market_name, start_day_invest, end_day_invest)
'''
