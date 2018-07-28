# -*- coding: utf-8 -*-
"""
Created on Tue Jul 10 00:57:46 2018

@author: vttqh
"""
import math
import ReadFile
import os
import glob
import datetime
import PMFG
import random
from CLASS import Stock
from sklearn.linear_model import LinearRegression
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


class Vertex():
    label = ''
    centrality_score = 0

    def __init__(self, label, centrality_score):
        self.label = label
        self.centrality_score = centrality_score

    def set_label(self, label):
        self.label = label

    def set_centrality_score(self, centrality_score):
        self.centrality_score = centrality_score

#============================================================================#


def calculate_r(time_series):
    r = []
    for i in range(0, len(time_series) - 1):
        difference = math.log(
            time_series[i] + 0.01, 2.718) - math.log(time_series[i + 1] + 0.01, 2.718)
        r.append(difference)

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
    lenght_integrated_ts = min(
        len(dcca_stock_1.integrated_ts), len(dcca_stock_2.integrated_ts))

    # Divide time series into segments of lenght S
    segment_count = int(lenght_integrated_ts / S)
    segments = [Segment()] * segment_count
    for i in range(0, segment_count):
        # Get integrated ts in segment
        s1_integrated = dcca_stock_1.integrated_ts[i * S: i * S + S]
        s2_integrated = dcca_stock_2.integrated_ts[i * S: i * S + S]

        s1_rs = calculate_residual_signals(s1_integrated)
        s2_rs = calculate_residual_signals(s2_integrated)

        # calculate variance and covariance
        s1_variance = calculate_variance(s1_rs, S)
        s2_variance = calculate_variance(s2_rs, S)
        covariance = (1 / S) * sum(s1_rs[i] * s2_rs[i] for i in range(0, S))

        segments[i].set_s1_variance(s1_variance)
        segments[i].set_s2_variance(s2_variance)
        segments[i].set_covariance(covariance)

    # Defined the fluctuation functions
    F_covariance = (1 / segment_count) * sum(np.sign(s.covariance)
                                             * abs(s.covariance)**(Q/2) for s in segments)
    F_s1_variance = (1 / segment_count) * sum(s.s1_variance**(Q/2)
                                              for s in segments)
    F_s2_variance = (1 / segment_count) * sum(s.s2_variance**(Q/2)
                                              for s in segments)

    # Retyrn the q-dependent cross-correlation coefficient between stock_1 and stock_2
    return F_covariance / (F_s1_variance * F_s2_variance)**(1/2.0)


def build_crosscorelation_matrix(dcca_stocks, Q, S):
    matrix = np.empty([len(dcca_stocks), len(dcca_stocks)], dtype=np.float)
    for i in range(0, len(dcca_stocks)):
        for j in range(i, len(dcca_stocks)):
            if i == j:
                matrix[i][i] = 0
                continue

            p = qdependent_cc_coefficient(dcca_stocks[i], dcca_stocks[j], Q, S)
            matrix[i][j] = round(p, 6)
            matrix[j][i] = round(p, 6)

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
    residual_signals = [integrated_ts[i] - trend[i]
                        for i in range(0, len(integrated_ts))]
    return residual_signals


def calculate_variance(residual_signals, S):
    total = sum(i * i for i in residual_signals)
    return (1 / S) * total


def invest(stocks, portfolios, begin_date, end_date):
    total_average_profit = 0
    for ticker in portfolios:
        stock = next((s for s in stocks if s.ticker == ticker), None)

        # Get list_close_price to use, note: decrease date
        lcp_to_use = stock.get_close_price_in_period(begin_date, end_date)

        average_profit = (1 / len(lcp_to_use)) * sum(
            lcp_to_use[i] - lcp_to_use[i + 1] for i in range(0, len(lcp_to_use) - 1))
        total_average_profit += average_profit

    return total_average_profit


def choose_stocks_to_invest(stocks, day_choose_stocks, Q, S):
    dcca_stocks = stocks.copy()

    # The first day of the period is selected to select the stock that needs to be invested
    first_day = day_choose_stocks - datetime.timedelta(days=1500)
    print(first_day)
    for dcca_stock in dcca_stocks:
        # Get list_close_price to use
        lcp_to_use = dcca_stock.get_close_price_in_period(
            first_day, day_choose_stocks)

        r = calculate_r(lcp_to_use)
        dcca_stock.set_r(r)

        integrated_ts = integrated_timeseries(dcca_stock.r)
        dcca_stock.set_integrated_ts(integrated_ts)

    c_matrix = build_crosscorelation_matrix(dcca_stocks, Q, S)

    nb_nodes = len(dcca_stocks)
    complete_graph = nx.Graph()
    for i in range(0, nb_nodes):
        for j in range(i+1, nb_nodes):
            complete_graph.add_edge(
                dcca_stocks[i].ticker, dcca_stocks[j].ticker, weight=c_matrix[i, j])

    PMFG_graph = PMFG.build_PMFG(complete_graph)

    ten_percent = int(nb_nodes * 0.1)
    portfolios = PMFG.choose_central_peripheral(
        PMFG_graph, ten_percent, ten_percent)

    return portfolios


def qdependent_DCCA(stocks, investment_start_date, investment_stop_date, market_name):
    Q = 1
    S = 50

    while Q <= 4:

        while S <= 150:

            filename = market_name + '_Q=' + str(Q) + '_S=' + str(S)
            save_result_to = os.path.join(
                os.getcwd(), 'result_qdependent_dcca', filename + '.txt')

            ff = open(save_result_to, 'w')

            total_profit_of_central = 0
            total_profit_of_peripheral = 0
            total_profit_of_random = 0

            day_choose_stocks = investment_start_date
            while day_choose_stocks < investment_stop_date:
                print(day_choose_stocks, Q, S)

                portfolios = choose_stocks_to_invest(
                    stocks, day_choose_stocks, Q, S)

                central_portfolio = [x.label for x in portfolios['central']]
                peripheral_portfolio = [
                    x.label for x in portfolios['peripheral']]

                random_portfolio = random.sample(
                    stocks, len(central_portfolio))
                random_portfolio = [s.ticker for s in random_portfolio]

                lastday_of_invesment = day_choose_stocks + \
                    datetime.timedelta(days=90)

                central_AP = invest(stocks, central_portfolio,
                                    day_choose_stocks, lastday_of_invesment)
                peripheral_AP = invest(
                    stocks, peripheral_portfolio, day_choose_stocks, lastday_of_invesment)
                random_AP = invest(stocks, random_portfolio,
                                   day_choose_stocks, lastday_of_invesment)

                total_profit_of_central += central_AP
                total_profit_of_peripheral += peripheral_AP
                total_profit_of_random += random_AP

                ff.write('{\n')
                ff.write('Ngay chon co phieu de dau tu: \'' +
                         str(day_choose_stocks) + "\',\n")
                ff.write('total_AR_of_central_portfolios: ' +
                         str(central_AP) + ",\n")
                ff.write('total_AR_of_peripheral_portfolios: ' +
                         str(peripheral_AP) + ",\n")
                ff.write('total_AR_of_random_portfolios: ' +
                         str(random_AP) + ",\n")
                ff.write('},\n')

                day_choose_stocks += datetime.timedelta(days=30)

            ff.write("================\n")
            ff.write('Profit of central: ' +
                     str(total_profit_of_central) + '\n')
            ff.write('Profit of peripheral: ' +
                     str(total_profit_of_peripheral) + '\n')
            ff.write('Profit of random: ' + str(total_profit_of_random) + '\n')
            ff.close()

            S += 50

        S = 50
        Q = 1



#============================================================================#
os.makedirs('result_qdependent_dcca', exist_ok=True)

for selected_market in range(10, 21):
    if selected_market == 1:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuvnindex')
        market_datapath = os.path.join(os.getcwd(), 'excel_^vnindex.csv')
        market_name = 'HOSE'
    elif selected_market == 2:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuhnxindex')
        market_datapath = os.path.join(os.getcwd(), 'excel_^hastc.csv')
        market_name = 'HNX'
    elif selected_market == 3:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunyse')
        market_datapath = os.path.join(os.getcwd(), '^NYA.csv')
        market_name = 'NYSE'
    elif selected_market == 4:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuamex')
        market_datapath = os.path.join(os.getcwd(), '^XAX.csv')
        market_name = 'AMEX'
    elif selected_market == 5:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuolsobors')
        market_datapath = os.path.join(os.getcwd(), '^OSEAX.csv')
        market_name = 'OLSOBORS'
    elif selected_market == 6:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunasdaq')
        market_datapath = os.path.join(os.getcwd(), '^IXIC.csv')
        market_name = 'NASDAQ'
    elif selected_market == 7:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuAEX')
        market_datapath = os.path.join(os.getcwd(), '^AEX.csv')
        market_name = 'AEX'
    elif selected_market == 8:
        data_dictionary = os.path.join(os.getcwd(), 'dulieucac40')
        market_datapath = os.path.join(os.getcwd(), '^FCHI.csv')
        market_name = 'CAC40'
    elif selected_market == 9:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuEuronext100')
        market_datapath = os.path.join(os.getcwd(), '^N100.csv')
        market_name = 'EURO100'
    elif selected_market == 10:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuIBEX35')
        market_datapath = os.path.join(os.getcwd(), '^IBEX.csv')
        market_name = 'IBEX35'
    elif selected_market == 11:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunikkei225')
        market_datapath = os.path.join(os.getcwd(), '^N225.csv')
        market_name = 'NIKKEI225'
    elif selected_market == 12:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuTSX')
        market_datapath = os.path.join(os.getcwd(), '^GSPTSE.csv')
        market_name = 'TSX'
    elif selected_market == 13:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuturkey')
        market_datapath = os.path.join(os.getcwd(), '^XU100.csv')
        market_name = 'XU100'
    elif selected_market == 14:
        #data_dictionary = os.path.join(os.getcwd(), 'dulieuIPC')
       # market_datapath = os.path.join(os.getcwd(), '^MXX.csv')
        # save_result_to = 'IPC
        continue
    elif selected_market == 15:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuBOVESPA')
        market_datapath = os.path.join(os.getcwd(), '^BVSP.csv')
        market_name = 'BOVESPA'
    elif selected_market == 16:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuAustraliaS&P200')
        market_datapath = os.path.join(os.getcwd(), '^AXJO.csv')
        market_name = 'AustraliaS&P200'
    elif selected_market == 17:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuNZX50')
        market_datapath = os.path.join(os.getcwd(), '^NZ50.csv')
        market_name = 'NZX50'
    elif selected_market == 18:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuShanghai')
        market_datapath = os.path.join(os.getcwd(), '^SSEC.csv')
        market_name = 'Shanghai'
    elif selected_market == 19:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuKOSPI')
        market_datapath = os.path.join(os.getcwd(), '^KS11.csv')
        market_name = 'KOSPI'
    elif selected_market == 20:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuSSEC50')
        market_datapath = os.path.join(os.getcwd(), '^SSE50.csv')
        market_name = 'SSEC50'
    else:
        print("...")

    print(market_name)

    all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))
    print("Tong so co phieu la: ", len(all_stocks_filepath))

    dcca_stocks = []

    for filePath in all_stocks_filepath:
        stock = ReadFile.read_data_stock(filePath)
        dcca_stock = DCCA_Stock(stock)
        dcca_stocks.append(dcca_stock)

    investment_start_date = datetime.date(2014, 6, 1)
    investment_stop_date = datetime.date(2017, 6, 1)

    qdependent_DCCA(dcca_stocks, investment_start_date,
                    investment_stop_date, market_name)
