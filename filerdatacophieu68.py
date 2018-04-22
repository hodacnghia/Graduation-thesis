# -*- coding: utf-8 -*-
"""
Created on Wed Apr 11 11:56:19 2018

@author: vttqh
"""
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
#=====================================================================================================
        
def valid_stock(stock, period_condition):
    if datetime.date.today() - datetime.timedelta(days=period_condition) > stock.list_trading_day[0]:
        return False
    
    for i in range(0, len(stock.list_trading_day) - 1):
        days_after_sub = stock.list_trading_day[i] - datetime.timedelta(days=20)
        
        if days_after_sub > stock.list_trading_day[i+1]:
            return False
    return True

def read_detail_stock(filepath):
    #TODO: Read stock info from file
    data_in_file = pd.read_csv(filepath)
    
    if len(data_in_file) < 1000:
        return None
    
    stock = Stock()
    stock.set_ticker(data_in_file['<Ticker>'].values[0])
    stock.set_close_price(data_in_file['<Close>'].values)
    list_day = convert_list_numpy_to_list_datetime(data_in_file['<DTYYYYMMDD>'].values)
    stock.set_list_trading_day(list_day)
    r = calculate_r(stock.list_close_price)
    stock.set_r(r)
    return stock

def save_list_stockID_to_file(listStockID, fileName):
    theFile = open(fileName, 'w')
    theFile.write('\n'.join(listStockID))
    theFile.close()

#====================================================================================================
data_dictionary = os.path.join(os.getcwd(), 'dulieuhnxindex')

# TODO: get all filename .csv
all_stocks_filepath = glob.glob(os.path.join(data_dictionary, "*.csv"))
print("Tổng số cổ phiếu của sàn HOSE: ", len(all_stocks_filepath))

# TODO: Read all of stocks from files
stocks = []
for i in range(0, len(all_stocks_filepath)):
    stock = read_detail_stock(all_stocks_filepath[i])
    
    if stock != None:
        if valid_stock(stock, 30):
            stocks.append(stock.ticker)
            
save_list_stockID_to_file(stocks, 'stockID_hnxindex.txt')
print(len(stocks))