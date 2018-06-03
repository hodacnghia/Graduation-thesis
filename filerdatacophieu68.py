# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 11:56:19 2018

@author: vttqh
"""
import os
import glob
import datetime
import pandas as pd


class Stock():
    ticker = ""
    list_close_price = []
    list_trading_day = []
    r = []
    average_volumn = 0

    def set_ticker(self, ticker):
        self.ticker = ticker

    def set_close_price(self, list_close_price):
        self.list_close_price = list_close_price

    def set_list_trading_day(self, list_trading_day):
        self.list_trading_day = list_trading_day

    def set_r(self, r):
        self.r = r

    def average_volumn(self, average_volumn):
        self.average_volumn = average_volumn
# =====================================================================================================


def valid_stock(stock, period_condition):
    if datetime.date.today() - datetime.timedelta(days=period_condition) > stock.list_trading_day[0]:
        return False

    for i in range(0, len(stock.list_trading_day) - 1):
        days_after_sub = stock.list_trading_day[i] - \
            datetime.timedelta(days=30)

        if days_after_sub > stock.list_trading_day[i+1]:
            print(stock.ticker)
            return False
    return True


def read_detail_stock(filepath):
    # TODO: Read stock info from file
    data_in_file = pd.read_csv(filepath)

    stock = Stock()
    stock.set_ticker(data_in_file['<Ticker>'].values[0])
    list_day = convert_list_numpy_to_list_datetime(
        data_in_file['<DTYYYYMMDD>'].values)

    if list_day[-1] > datetime.date(2014, 6, 1):
        os.remove(filepath)
        return None
    stock.set_list_trading_day(list_day)

    total_volumn = 0
    volumns = data_in_file['<DTYYYYMMDD>'].values[:30]
    for v in volumns:
        total_volumn += v
    stock.average_volumn(total_volumn / len(volumns))

    return stock


def read_detail_stock_yf(filepath, ticker):
    # TODO: Read market index from yahoo finance download file
    data_in_file = pd.read_csv(filepath)

    stock = Stock()
    stock.set_ticker(ticker)
    stock.set_list_close_price(data_in_file['Close'].values[::-1])
    list_day = convert_list_string_to_list_datetime(
        data_in_file['Date'].values[::-1])

    if list_day[-1] > datetime.date(2014, 1, 1):
        os.remove(filepath)
        return None

    stock.set_list_trading_day(list_day)
    return stock


def convert_list_string_to_list_datetime(list_date):
    list_datetime = []

    for d in list_date:
        split_d = d.split('-')
        dtime = datetime.date(int(split_d[0]), int(
            split_d[1]), int(split_d[2]))
        list_datetime.append(dtime)
    return list_datetime


def save_list_stockID_to_file(listStockID, fileName):
    theFile = open(fileName, 'w')
    theFile.write('\n'.join(listStockID))
    theFile.close()


def convert_list_numpy_to_list_datetime(list):
    list_datetime = []

    for day in list:
        string_day = str(day)
        dtime = datetime.date(int(string_day[:4]), int(
            string_day[4:6]), int(string_day[6:8]))
        list_datetime.append(dtime)
    return list_datetime


def change_format_excel(filepath, save_to):
    file = pd.read_csv(filepath)
    date = file['Date'].values[::-1]
    open = file['Open'].values[::-1]
    high = file['High'].values[::-1]
    low = file['Low'].values[::-1]
    close = file['Close'].values[::-1]
    volume = file['Volume'].values[::-1]

    t = filepath[filepath.rfind('\\') + 1:filepath.rfind('.')]
    ticker = [t] * len(date)

    dtyyyymmdd = []

    for d in date:
        split_d = d.split('-')
        yyyymmdd = ''.join(split_d)
        dtyyyymmdd.append(yyyymmdd)

    dframe = list(zip(ticker, dtyyyymmdd, open, high, low, close, volume))

    os.remove(filepath)
    df = pd.DataFrame(data=dframe, columns=[
                      '<Ticker>', '<DTYYYYMMDD>', '<Open>', 'High', '<Low>', '<Close>', '<Volume>'])
    df.to_csv(os.path.join(save_to, t + '.csv'), index=False, header=True)


# ====================================================================================================
data_dictionary = os.path.join(os.getcwd(), 'dulieuShanghai')

# TODO: get all filename .csv
all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))
print("Tổng số cổ phiếu của sàn: ", len(all_stocks_filepath))


# Change format data
for fp in all_stocks_filepath:
    change_format_excel(fp, os.path.join(os.getcwd(), 'dulieuShanghai'))


# TODO: Read all of stocks from files download in cophieu68
stocks = []
for i in range(0, len(all_stocks_filepath)):
    stock = read_detail_stock(all_stocks_filepath[i])

    if stock != None:
        if valid_stock(stock, 30):
            stocks.append(stock.ticker)

save_list_stockID_to_file(stocks, 'stockID_Shanghai.txt')
print(len(stocks))


'''
# TODO: Read all of stocks from files download in netfond
stocks = []
for i in range(0, len(all_stocks_filepath)):
    stock = read_detail_stock(all_stocks_filepath[i])
    
    if stock != None:
        if valid_stock(stock, 30):
            stocks.append(stock)
         
stocks = sorted(stocks, key = lambda s: (s.average_volumn))

if (len(stocks) > 200):
    stocks = stocks[:200]

stocks_ticker = []

for s in stocks:
    stocks_ticker.append(s.ticker)
    
save_list_stockID_to_file(stocks_ticker, 'stockID_nyse.txt')
print(len(stocks_ticker))



# TODO: Read all of stocks from files download in yahoo finance
'''
