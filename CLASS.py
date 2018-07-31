import numpy as np

#==========================================================================================#
class Stock():
    ratio = 0
    ticker = ""
    list_close_price = []
    list_trading_day = []
    r = []

    def set_ticker(self, ticker):
        self.ticker = ticker
    def set_ratio(self, ratio):
        self.ratio = ratio
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