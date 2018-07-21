# -*- coding: utf-8 -*-
"""
Created on Sun Jul 15 12:34:40 2018

@author: vttqh
"""
import math, ReadFile, os, glob, datetime, PMFG, random
from CLASS import Stock
from matplotlib import pyplot
import numpy as np
import networkx as nx
from scipy.stats.stats import pearsonr
#==============================================================================#
class SORA_stock(Stock):
    # ratio = expected / standard deviation
    ratio = 0
    
    def __init__(self, stock):
        self.ticker = stock.ticker
        self.list_close_price = stock.list_close_price
        self.list_trading_day = stock.list_trading_day
        
    def set_ratio(self, ratio):
        self.ratio = ratio
#==============================================================================#
def choose_stocks_to_invest(sora_stocks, day_choose_stocks):
    stocks = sora_stocks.copy()
    
    # The first day of the period is selected to select the stock that needs to be invested
    first_day = day_choose_stocks - datetime.timedelta(days=125)
    for s in stocks:
        lcp_to_use = s.get_close_price_in_period(first_day, day_choose_stocks)
        r = calculate_r(lcp_to_use)
        s.set_r(r)
        
        ratio = np.mean(r) / np.std(r)
        s.set_ratio(ratio)
        
    # Get half of stocks have largest ratio (expected / standard deviation)
    stocks = sorted(stocks, key=lambda s: (s.ratio), reverse=True)
    half_length = int(len(stocks) / 2)
    stocks = stocks[:half_length]
    
    pearson_cor_matrix = build_peason_correlation_matrix(stocks)
    
    nb_nodes = len(stocks)
    complete_graph = nx.Graph()
    for i in range(0, nb_nodes):
        for j in range(i+1, nb_nodes):
            complete_graph.add_edge(stocks[i].ticker, stocks[j].ticker, weight=pearson_cor_matrix[i,j])
            
    PMFG_graph = PMFG.build_PMFG(complete_graph)
    
    twenty_percent = int(nb_nodes * 0.2)
    portfolios = PMFG.choose_central_peripheral(PMFG_graph, twenty_percent, twenty_percent)
    
    return portfolios

        
def calculate_r(stock_returns):
    r = []
    price_in_first_day = stock_returns[0]
    for i in range(1, len(stock_returns)):
        difference = (stock_returns[i] - price_in_first_day) / price_in_first_day
        r.append(difference)
        
    return r
        
def build_peason_correlation_matrix(stocks):
    matrix = np.empty([len(stocks), len(stocks)], dtype=np.float)
    for i in range(0, len(stocks)):
        for j in range(i, len(stocks)):
            if i == j:
                matrix[i][i] = 0
                continue
            print(stocks[i].ticker, stocks[j].ticker)
            p = pearsonr(stocks[i].r, stocks[j].r)[0]
            matrix[i][j] = round(p, 6)
            matrix[j][i] = round(p, 6)
            
    return matrix

def invest(stocks, portfolios, begin_date, end_date):
    total_average_profit = 0
    print(begin_date, end_date)
    for ticker in portfolios:
        stock = next((s for s in stocks if s.ticker == ticker), None)
        
        #Get list_close_price to use, note: decrease date
        lcp_to_use = stock.get_close_price_in_period(begin_date, end_date)
        
        average_profit = (1 / len(lcp_to_use)) * sum(lcp_to_use[i] - lcp_to_use[i + 1] for i in range(0, len(lcp_to_use) - 1))
        print(stock.ticker, average_profit)
        total_average_profit += average_profit
    
    return total_average_profit

def SORA(sora_stocks, investment_start_date, investment_stop_date, save_result_to):
    ff = open(save_result_to, 'w')
    total_profit_of_central    = 0
    total_profit_of_peripheral = 0
    total_profit_of_random     = 0
    
    day_choose_stocks = investment_start_date
    while(day_choose_stocks < investment_stop_date):
        portfolios = choose_stocks_to_invest(sora_stocks, day_choose_stocks)
    
        central_portfolio    = [x.label for x in portfolios['central']]
        peripheral_portfolio = [x.label for x in portfolios['peripheral']]
    
        random_portfolio     = random.sample(sora_stocks, len(central_portfolio))
        random_portfolio     = [s.ticker for s in random_portfolio]

        lastday_of_invesment = day_choose_stocks + datetime.timedelta(days=90)

        central_AP    = invest(sora_stocks, central_portfolio, day_choose_stocks, lastday_of_invesment)
        peripheral_AP = invest(sora_stocks, peripheral_portfolio, day_choose_stocks, lastday_of_invesment)
        random_AP     = invest(sora_stocks, random_portfolio, day_choose_stocks, lastday_of_invesment)
        
        total_profit_of_central    += central_AP
        total_profit_of_peripheral += peripheral_AP
        total_profit_of_random     += random_AP
        
    
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
    ff.write('Profit of central: '    + str(total_profit_of_central) + '\n')
    ff.write('Profit of peripheral: ' + str(total_profit_of_peripheral) + '\n')
    ff.write('Profit of random: '     + str(total_profit_of_random) + '\n')
    ff.close()
        
        

#==============================================================================#
os.makedirs('resultSORA', exist_ok=True)

for selected_market in range(1, 21):
    if selected_market == 1:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuvnindex')
        market_datapath = os.path.join(os.getcwd(), 'excel_^vnindex.csv')
        save_result_to = 'HOSE'
    elif selected_market == 2:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuhnxindex')
        market_datapath = os.path.join(os.getcwd(), 'excel_^hastc.csv')
        save_result_to = 'HNX'
    elif selected_market == 3:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunyse')
        market_datapath = os.path.join(os.getcwd(), '^NYA.csv')
        save_result_to = 'NYSE'
    elif selected_market == 4:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuamex')
        market_datapath = os.path.join(os.getcwd(), '^XAX.csv')
        save_result_to = 'AMEX'
    elif selected_market == 5:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuolsobors')
        market_datapath = os.path.join(os.getcwd(), '^OSEAX.csv')
        save_result_to = 'OLSOBORS'
    elif selected_market == 6:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunasdaq')
        market_datapath = os.path.join(os.getcwd(), '^IXIC.csv')
        save_result_to = 'NASDAQ'
    elif selected_market == 7:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuAEX')
        market_datapath = os.path.join(os.getcwd(), '^AEX.csv')
        save_result_to = 'AEX'
    elif selected_market == 8:
        data_dictionary = os.path.join(os.getcwd(), 'dulieucac40')
        market_datapath = os.path.join(os.getcwd(), '^FCHI.csv')
        save_result_to = 'CAC40'
    elif selected_market == 9:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuEuronext100')
        market_datapath = os.path.join(os.getcwd(), '^N100.csv')
        save_result_to = 'EURO100'
    elif selected_market == 10:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuIBEX35')
        market_datapath = os.path.join(os.getcwd(), '^IBEX.csv')
        save_result_to = 'IBEX35'
    elif selected_market == 11:
        data_dictionary = os.path.join(os.getcwd(), 'dulieunikkei225')
        market_datapath = os.path.join(os.getcwd(), '^N225.csv')
        save_result_to = 'NIKKEI225'
    elif selected_market == 12:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuTSX')
        market_datapath = os.path.join(os.getcwd(), '^GSPTSE.csv')
        save_result_to = 'TSX'
    elif selected_market == 13:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuturkey')
        market_datapath = os.path.join(os.getcwd(), '^XU100.csv')
        save_result_to = 'XU100'
    elif selected_market == 14:
        #data_dictionary = os.path.join(os.getcwd(), 'dulieuIPC')
       # market_datapath = os.path.join(os.getcwd(), '^MXX.csv')
        #save_result_to = 'IPC
        continue
    elif selected_market == 15:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuBOVESPA')
        market_datapath = os.path.join(os.getcwd(), '^BVSP.csv')
        save_result_to = 'BOVESPA'
    elif selected_market == 16:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuAustraliaS&P200')
        market_datapath = os.path.join(os.getcwd(), '^AXJO.csv')
        save_result_to = 'AustraliaS&P200'
    elif selected_market == 17:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuNZX50')
        market_datapath = os.path.join(os.getcwd(), '^NZ50.csv')
        save_result_to = 'NZX50'
    elif selected_market == 18:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuShanghai')
        market_datapath = os.path.join(os.getcwd(), '^SSEC.csv')
        save_result_to = 'Shanghai'
    elif selected_market == 19:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuKOSPI')
        market_datapath = os.path.join(os.getcwd(), '^KS11.csv')
        save_result_to = 'KOSPI'
    elif selected_market == 20:
        data_dictionary = os.path.join(os.getcwd(), 'dulieuSSEC50')
        market_datapath = os.path.join(os.getcwd(), '^SSE50.csv')
        save_result_to = 'SSEC50'
    else:
        print("...")
    print(save_result_to)
    
    all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))
    print("Tong so co phieu la: ", len(all_stocks_filepath))

    sora_stocks = []
    for filePath in all_stocks_filepath:
        stock = ReadFile.read_data_stock(filePath)
        sora_stock = SORA_stock(stock)
        sora_stocks.append(sora_stock)

    investment_start_date = datetime.date(2014, 6, 1)
    investment_stop_date  = datetime.date(2017, 6, 1)

    save_result_path = os.path.join(os.getcwd(), 'resultSORA', save_result_to + '.txt')
    SORA(sora_stocks, investment_start_date, investment_stop_date, save_result_path)






