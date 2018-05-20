import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook

years = mdates.YearLocator()   # every year
months = mdates.MonthLocator()  # every month
yearsFmt = mdates.DateFormatter('%Y')

# Load a numpy record array from yahoo csv data with fields date, open, close,
# volume, adj_close from the mpl-data/example directory. The record array
# stores the date as an np.datetime64 with a day unit ('D') in the date column.
a = [{
    'day_t': '2015-06-01',
    'total_AR_of_central_portfolios': 0.0004887095014726656,
    'total_AR_of_peripheral_portfolios': -0.009075868524258696,
    'total_AR_of_random_portfolios': -0.008599793553586452,
    'rd_of_MC_in_selection_horizon': 0.5074626865671642,
    'rd_of_MC_in_investment_horizon': 0.4830917874396135,
    'rf_of_MC_in_selection_horizon': 0.5138686131386863,
    'rf_of_MC_in_investment_horizon': 0.4852941176470589,
},
    {
    'day_t': '2015-07-01',
    'total_AR_of_central_portfolios': -0.0041803743618831525,
    'total_AR_of_peripheral_portfolios': -0.008122873424347725,
    'total_AR_of_random_portfolios': -0.0030780113952229363,
    'rd_of_MC_in_selection_horizon': 0.4729064039408867,
    'rd_of_MC_in_investment_horizon': 0.48058252427184467,
    'rf_of_MC_in_selection_horizon': 0.4918265813788201,
    'rf_of_MC_in_investment_horizon': 0.47363636363636363,
},
    {
    'day_t': '2015-07-31',
    'total_AR_of_central_portfolios': 0.0009384236453201896,
    'total_AR_of_peripheral_portfolios': 0.0005784731396677972,
    'total_AR_of_random_portfolios': 0.001107165248082308,
    'rd_of_MC_in_selection_horizon': 0.458128078817734,
    'rd_of_MC_in_investment_horizon': 0.47058823529411764,
    'rf_of_MC_in_selection_horizon': 0.4793447293447295,
    'rf_of_MC_in_investment_horizon': 0.4887755102040816,
},
    {
    'day_t': '2015-08-30',
    'total_AR_of_central_portfolios': -0.00011292395746177844,
    'total_AR_of_peripheral_portfolios': 0.0011979202424167949,
    'total_AR_of_random_portfolios': 1.931807205640863e-06,
    'rd_of_MC_in_selection_horizon': 0.45320197044334976,
    'rd_of_MC_in_investment_horizon': 0.4878048780487805,
    'rf_of_MC_in_selection_horizon': 0.46394557823129245,
    'rf_of_MC_in_investment_horizon': 0.5400238948626045,
},
    {
    'day_t': '2015-09-29',
    'total_AR_of_central_portfolios': -0.001520013241904969,
    'total_AR_of_peripheral_portfolios': 0.001594370860927154,
    'total_AR_of_random_portfolios': 0.0017578836279264027,
    'rd_of_MC_in_selection_horizon': 0.45544554455445546,
    'rd_of_MC_in_investment_horizon': 0.48292682926829267,
    'rf_of_MC_in_selection_horizon': 0.4626135569531797,
    'rf_of_MC_in_investment_horizon': 0.5337837837837838,
},
    {
    'day_t': '2015-10-29',
    'total_AR_of_central_portfolios': 0.010442959001782534,
    'total_AR_of_peripheral_portfolios': -2.90426411480265e-05,
    'total_AR_of_random_portfolios': 0.0078201141051304,
    'rd_of_MC_in_selection_horizon': 0.4827586206896552,
    'rd_of_MC_in_investment_horizon': 0.4585365853658537,
    'rf_of_MC_in_selection_horizon': 0.49725920125293654,
    'rf_of_MC_in_investment_horizon': 0.505050505050505,
},
    {
    'day_t': '2015-11-28',
    'total_AR_of_central_portfolios': 0.0004431082777938755,
    'total_AR_of_peripheral_portfolios': -0.0027839542626304126,
    'total_AR_of_random_portfolios': 0.0008451591955414622,
    'rd_of_MC_in_selection_horizon': 0.4852941176470588,
    'rd_of_MC_in_investment_horizon': 0.47804878048780486,
    'rf_of_MC_in_selection_horizon': 0.48804616652926625,
    'rf_of_MC_in_investment_horizon': 0.5154334997730368,
}, ]
day_t = []
for o in a:
    string_day = o['day_t']
    dtime = datetime.date(int(string_day[:4]), int(
        string_day[5:7]), int(string_day[8:10]))
    day_t.append(dtime)
rf_of_MC_in_selection_horizon = []
for o in a:
    string_day = o['rf_of_MC_in_investment_horizon']
    rf_of_MC_in_selection_horizon.append(string_day)
print(rf_of_MC_in_selection_horizon)

plt.plot_date(day_t, rf_of_MC_in_selection_horizon, 'ro')
plt.show()
