# -*- coding: utf-8 -*-
"""
Created on Wed Jul  4 15:36:13 2018

@author: vttqh
"""
import numpy as np
import os, glob, datetime
import pandas as pd
import ReadFile

#==============================================================================#
def change_format_excel(filepath, save_to):
    file = pd.read_csv(filepath)
    date = file['Date'].values[::-1]
    oopen = file['Open'].values[::-1]
    high = file['High'].values[::-1]
    low = file['Low'].values[::-1]
    close = file['Close'].values[::-1]
    volume = file['Volume'].values[::-1]

    t = filepath[filepath.rfind('\\') + 1:filepath.rfind('.')]
    ticker = [t] * len(date)
    
    dtyyyymmdd = []

    for d in date:
        print(d)
        split_d = d.split('/')
        
        if int(split_d[0]) < 10:
            split_d[0] = '0' + split_d[0]
        if int(split_d[1]) < 10:
            split_d[1] = '0' + split_d[1]
            
        yyyymmdd = ''.join(split_d[::-1])
        print(yyyymmdd)
        dtyyyymmdd.append(yyyymmdd)

    dframe = list(zip(ticker, dtyyyymmdd, oopen, high, low, close, volume))

    os.remove(filepath)
    df = pd.DataFrame(data=dframe, columns=['<Ticker>', '<DTYYYYMMDD>', '<Open>', '<High>', '<Low>', '<Close>', '<Volume>'])
    df.to_csv(os.path.join(save_to, t + '.csv'), index=False, header=True)
    
    
def fill_data_to_nullcell(filepath, save_to):
    file = pd.read_csv(filepath)
    ticker = file['<Ticker>'].values
    date = file['<DTYYYYMMDD>'].values
    oopen = file['<Open>'].values
    high = file['<High>'].values
    low = file['<Low>'].values
    close = file['<Close>'].values
    volume = file['<Volume>'].values
    
    for i in range(0, len(oopen) - 1):
        if np.isnan(oopen[i]):
            
            for j in range(i + 1, len(oopen) - 1):
                if np.isnan(oopen[j]) == False:
                    oopen[i] = np.array([oopen[j]])
                    high[i] = np.array([high[j]])
                    low[i] = np.array([low[j]])
                    close[i] = np.array([close[j]])
                    volume[i] = np.array([volume[j]])
                    break
            
    dframe = list(zip(ticker, date, oopen, high, low, close, volume))
    
    os.remove(filepath)
    df = pd.DataFrame(data=dframe, columns=['<Ticker>', '<DTYYYYMMDD>', '<Open>', '<High>', '<Low>', '<Close>', '<Volume>'])
    df.to_csv(os.path.join(save_to, ticker[0] + '.csv'), index=False, header=True)

def convert_datetime_to_YYYYMMDD(dt):
    month = dt.month
    day = dt.day
        
    if (month < 10):
        month = str('0') + str(month)
    if (day < 10):
        day = str('0') + str(day)
            
    yyyymmdd = str(dt.year) + str(month) + str(day)
    return yyyymmdd
    
#==============================================================================#
change_format_excel(os.path.join(os.getcwd(), '^OSEAX.csv'), os.getcwd())
fill_data_to_nullcell(os.path.join(os.getcwd(), '^OSEAX.csv'), os.getcwd())


market_index = ReadFile.read_data_marketindex(os.path.join(os.getcwd(), '^OSEAX.csv'))

data_dictionary = os.path.join(os.getcwd(), 'dulieuolsobors')

# TODO: get all filename .csv
all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))

# Change format data
for fp in all_stocks_filepath:
    file = pd.read_csv(fp)
    ticker = file['<Ticker>'].values
    print(ticker[0])
    date = file['<DTYYYYMMDD>'].values
    oopen = file['<Open>'].values
    high = file['<High>'].values
    low = file['<Low>'].values
    close = file['<Close>'].values
    volume = file['<Volume>'].values
    
    new_date = []
    new_oopen = []
    new_high = []
    new_low = []
    new_close = []
    new_volume = []
    
    firstday_trade = str(date[-1])
    firstday = datetime.date(int(firstday_trade[:4]), int(firstday_trade[4:6]), int(firstday_trade[6:8]))
    
    reverse_list_trading = market_index.list_trading_day[::-1]
    
    try:
        pos_fd_in_market = reverse_list_trading.index(firstday)
    except ValueError:
        pos_fd_in_market = 0
            
    for i in range(pos_fd_in_market, len(reverse_list_trading)):
        current_date = reverse_list_trading[i]
        currentdate_ymd = convert_datetime_to_YYYYMMDD(current_date)
        
        pos_tradinglist_stock = np.where(date == int(currentdate_ymd))
        
        if len(pos_tradinglist_stock[0]) > 0:
            pos = pos_tradinglist_stock[0][0]
            
            new_date.append(date[pos])
            new_oopen.append(oopen[pos])
            new_high.append(high[pos])
            new_low.append(low[pos])
            new_close.append(close[pos])
            new_volume.append(volume[pos])
        else:
            if len(new_date) == 0:
                new_date.append(currentdate_ymd)
                new_oopen.append(0)
                new_high.append(0)
                new_low.append(0)
                new_close.append(0)
                new_volume.append(0)
            else:
                new_date.append(currentdate_ymd)
                new_oopen.append(new_oopen[-1])
                new_high.append(new_high[-1])
                new_low.append(new_low[-1])
                new_close.append(new_close[-1])
                new_volume.append(new_volume[-1])
            
    ticker = [ticker[0]] * len(new_date)
    
    dframe = list(zip(ticker, new_date[::-1], new_oopen[::-1], new_high[::-1], new_low[::-1], new_close[::-1], new_volume[::-1]))
    
    os.remove(fp)
    df = pd.DataFrame(data=dframe, columns=['<Ticker>', '<DTYYYYMMDD>', '<Open>', '<High>', '<Low>', '<Close>', '<Volume>'])
    df.to_csv(fp, index=False, header=True)
    