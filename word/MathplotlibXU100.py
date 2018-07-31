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


a10Correlation = [

    {
        'day_t': '2014-06-01',
        'total_AR_of_central_portfolios': -0.0005537850467289746,
        'total_AR_of_peripheral_portfolios': -0.008767046728971946,
        'total_AR_of_random_portfolios': -0.005320135514018675,
        'rd_of_MC_in_selection_horizon': 0.4604651162790698,
        'rd_of_MC_in_investment_horizon': 0.5162790697674419,
        'rf_of_MC_in_selection_horizon': 0.5137909387071563,
        'rf_of_MC_in_investment_horizon': 0.5034613721102505,
    },
    {
        'day_t': '2014-07-01',
        'total_AR_of_central_portfolios': -0.024935084507042255,
        'total_AR_of_peripheral_portfolios': -0.009530488262910773,
        'total_AR_of_random_portfolios': -0.007457737089201871,
        'rd_of_MC_in_selection_horizon': 0.4883720930232558,
        'rd_of_MC_in_investment_horizon': 0.514018691588785,
        'rf_of_MC_in_selection_horizon': 0.5285524409193618,
        'rf_of_MC_in_investment_horizon': 0.5147519452490427,
    },
    {
        'day_t': '2014-07-31',
        'total_AR_of_central_portfolios': 0.002629112676056341,
        'total_AR_of_peripheral_portfolios': 0.05812539906103286,
        'total_AR_of_random_portfolios': 0.05071822535211269,
        'rd_of_MC_in_selection_horizon': 0.5116279069767442,
        'rd_of_MC_in_investment_horizon': 0.4953271028037383,
        'rf_of_MC_in_selection_horizon': 0.5183728273298536,
        'rf_of_MC_in_investment_horizon': 0.5033514181481445,
    },
    {
        'day_t': '2014-08-30',
        'total_AR_of_central_portfolios': -0.0013201074766355386,
        'total_AR_of_peripheral_portfolios': -0.007476640186915896,
        'total_AR_of_random_portfolios': -0.007516392523364484,
        'rd_of_MC_in_selection_horizon': 0.5116279069767442,
        'rd_of_MC_in_investment_horizon': 0.5069767441860465,
        'rf_of_MC_in_selection_horizon': 0.5122081739665073,
        'rf_of_MC_in_investment_horizon': 0.5040200910983421,
    },
    {
        'day_t': '2014-09-29',
        'total_AR_of_central_portfolios': -0.0006572863849765298,
        'total_AR_of_peripheral_portfolios': -0.000780422535211268,
        'total_AR_of_random_portfolios': 0.0006572769953051669,
        'rd_of_MC_in_selection_horizon': 0.5069767441860465,
        'rd_of_MC_in_investment_horizon': 0.5093457943925234,
        'rf_of_MC_in_selection_horizon': 0.5049014622969146,
        'rf_of_MC_in_investment_horizon': 0.5055103829135741,
    },
    {
        'day_t': '2014-10-29',
        'total_AR_of_central_portfolios': -0.0010328638497652612,
        'total_AR_of_peripheral_portfolios': 0.0024121596244131432,
        'total_AR_of_random_portfolios': 0.0028638497652582156,
        'rd_of_MC_in_selection_horizon': 0.5162790697674419,
        'rd_of_MC_in_investment_horizon': 0.5,
        'rf_of_MC_in_selection_horizon': 0.5426461296447579,
        'rf_of_MC_in_investment_horizon': 0.4908239413206975,
    },
    {
        'day_t': '2014-11-28',
        'total_AR_of_central_portfolios': 0.003990610328638506,
        'total_AR_of_peripheral_portfolios': -0.04272300469483567,
        'total_AR_of_random_portfolios': -0.047887319248826284,
        'rd_of_MC_in_selection_horizon': 0.5395348837209303,
        'rd_of_MC_in_investment_horizon': 0.48130841121495327,
        'rf_of_MC_in_selection_horizon': 0.5851128441868605,
        'rf_of_MC_in_investment_horizon': 0.48334300695163285,
    },
    {
        'day_t': '2014-12-28',
        'total_AR_of_central_portfolios': 0.0003271028037383232,
        'total_AR_of_peripheral_portfolios': -0.010046742990654212,
        'total_AR_of_random_portfolios': -0.009299051401869155,
        'rd_of_MC_in_selection_horizon': 0.5209302325581395,
        'rd_of_MC_in_investment_horizon': 0.4930232558139535,
        'rf_of_MC_in_selection_horizon': 0.580067526435767,
        'rf_of_MC_in_investment_horizon': 0.4931201657598643,
    },
    {
        'day_t': '2015-01-27',
        'total_AR_of_central_portfolios': 0.004835671361502355,
        'total_AR_of_peripheral_portfolios': 0.0029733755868544594,
        'total_AR_of_random_portfolios': 0.026572765258215964,
        'rd_of_MC_in_selection_horizon': 0.5162790697674419,
        'rd_of_MC_in_investment_horizon': 0.4766355140186916,
        'rf_of_MC_in_selection_horizon': 0.5332696034383733,
        'rf_of_MC_in_investment_horizon': 0.47014326258962846,
    },
    {
        'day_t': '2015-02-26',
        'total_AR_of_central_portfolios': -0.002394366197183104,
        'total_AR_of_peripheral_portfolios': 0.0037089248826291214,
        'total_AR_of_random_portfolios': -0.008638492957746475,
        'rd_of_MC_in_selection_horizon': 0.5209302325581395,
        'rd_of_MC_in_investment_horizon': 0.4719626168224299,
        'rf_of_MC_in_selection_horizon': 0.5171990608004609,
        'rf_of_MC_in_investment_horizon': 0.47236124349261516,
    },
    {
        'day_t': '2015-03-28',
        'total_AR_of_central_portfolios': 0.0,
        'total_AR_of_peripheral_portfolios': 0.0,
        'total_AR_of_random_portfolios': 0.0,
        'rd_of_MC_in_selection_horizon': 0.5162790697674419,
        'rd_of_MC_in_investment_horizon': 0.46511627906976744,
        'rf_of_MC_in_selection_horizon': 0.5034613721102505,
        'rf_of_MC_in_investment_horizon': 0.46568057061592444,
    },
    {
        'day_t': '2015-04-27',
        'total_AR_of_central_portfolios': 0.0055868544600938905,
        'total_AR_of_peripheral_portfolios': 0.01014103286384976,
        'total_AR_of_random_portfolios': 0.010985901408450684,
        'rd_of_MC_in_selection_horizon': 0.5116279069767442,
        'rd_of_MC_in_investment_horizon': 0.4672897196261682,
        'rf_of_MC_in_selection_horizon': 0.5143156059428203,
        'rf_of_MC_in_investment_horizon': 0.46174242754138994,
    },
    {
        'day_t': '2015-05-27',
        'total_AR_of_central_portfolios': 0.0032863849765258223,
        'total_AR_of_peripheral_portfolios': 0.006619751173708956,
        'total_AR_of_random_portfolios': 0.024084525821596252,
        'rd_of_MC_in_selection_horizon': 0.4930232558139535,
        'rd_of_MC_in_investment_horizon': 0.5046728971962616,
        'rf_of_MC_in_selection_horizon': 0.503071526223614,
        'rf_of_MC_in_investment_horizon': 0.4948039015086025,
    },
    {
        'day_t': '2015-06-26',
        'total_AR_of_central_portfolios': -0.004507037558685448,
        'total_AR_of_peripheral_portfolios': 0.050025633802816896,
        'total_AR_of_random_portfolios': -0.004647910798122087,
        'rd_of_MC_in_selection_horizon': 0.5069767441860465,
        'rd_of_MC_in_investment_horizon': 0.5,
        'rf_of_MC_in_selection_horizon': 0.5040200910983421,
        'rf_of_MC_in_investment_horizon': 0.5118938734401829,
    },
    {
        'day_t': '2015-07-26',
        'total_AR_of_central_portfolios': -0.004999990654205616,
        'total_AR_of_peripheral_portfolios': -0.022394953271028036,
        'total_AR_of_random_portfolios': -0.0032242897196261672,
        'rd_of_MC_in_selection_horizon': 0.5116279069767442,
        'rd_of_MC_in_investment_horizon': 0.48372093023255813,
        'rf_of_MC_in_selection_horizon': 0.5059317666749554,
        'rf_of_MC_in_investment_horizon': 0.49694265055740355,
    },
    {
        'day_t': '2015-08-25',
        'total_AR_of_central_portfolios': 0.001267605633802821,
        'total_AR_of_peripheral_portfolios': -0.08309859154929577,
        'total_AR_of_random_portfolios': -0.05765257276995303,
        'rd_of_MC_in_selection_horizon': 0.5023255813953489,
        'rd_of_MC_in_investment_horizon': 0.48130841121495327,
        'rf_of_MC_in_selection_horizon': 0.49127628453241623,
        'rf_of_MC_in_investment_horizon': 0.5120985233774586,
    },
    {
        'day_t': '2015-09-24',
        'total_AR_of_central_portfolios': 0.0007042253521126714,
        'total_AR_of_peripheral_portfolios': 0.0059593427230047015,
        'total_AR_of_random_portfolios': -0.044413150234741794,
        'rd_of_MC_in_selection_horizon': 0.4790697674418605,
        'rd_of_MC_in_investment_horizon': 0.48598130841121495,
        'rf_of_MC_in_selection_horizon': 0.48331323071809745,
        'rf_of_MC_in_investment_horizon': 0.5008650176882653,
    },
    {
        'day_t': '2015-10-24',
        'total_AR_of_central_portfolios': 0.013224313084112168,
        'total_AR_of_peripheral_portfolios': 0.039496168224299064,
        'total_AR_of_random_portfolios': 0.012196280373831801,
        'rd_of_MC_in_selection_horizon': 0.4930232558139535,
        'rd_of_MC_in_investment_horizon': 0.4930232558139535,
        'rf_of_MC_in_selection_horizon': 0.4931201657598643,
        'rf_of_MC_in_investment_horizon': 0.4967955588926642,
    },
    {
        'day_t': '2015-11-23',
        'total_AR_of_central_portfolios': 2.0599841277224584e-18,
        'total_AR_of_peripheral_portfolios': -0.040070938967136156,
        'total_AR_of_random_portfolios': -0.058309859154929575,
        'rd_of_MC_in_selection_horizon': 0.4744186046511628,
        'rd_of_MC_in_investment_horizon': 0.48598130841121495,
        'rf_of_MC_in_selection_horizon': 0.46801126854631336,
        'rf_of_MC_in_investment_horizon': 0.4993264420458347,
    },
    {
        'day_t': '2015-12-23',
        'total_AR_of_central_portfolios': -0.012253521126760564,
        'total_AR_of_peripheral_portfolios': -0.012224676056338061,
        'total_AR_of_random_portfolios': 0.0029577276995305093,
        'rd_of_MC_in_selection_horizon': 0.4697674418604651,
        'rd_of_MC_in_investment_horizon': 0.49065420560747663,
        'rf_of_MC_in_selection_horizon': 0.4678358753050354,
        'rf_of_MC_in_investment_horizon': 0.5136983318378268,
    },
    {
        'day_t': '2016-01-22',
        'total_AR_of_central_portfolios': -0.0019248826291079794,
        'total_AR_of_peripheral_portfolios': -0.07592276525821602,
        'total_AR_of_random_portfolios': -0.05441316901408453,
        'rd_of_MC_in_selection_horizon': 0.46511627906976744,
        'rd_of_MC_in_investment_horizon': 0.48598130841121495,
        'rf_of_MC_in_selection_horizon': 0.46568057061592444,
        'rf_of_MC_in_investment_horizon': 0.5146155412526774,
    },
    {
        'day_t': '2016-02-21',
        'total_AR_of_central_portfolios': -0.000981308411214948,
        'total_AR_of_peripheral_portfolios': 0.00443917757009338,
        'total_AR_of_random_portfolios': -0.011355102803738274,
        'rd_of_MC_in_selection_horizon': 0.46511627906976744,
        'rd_of_MC_in_investment_horizon': 0.48372093023255813,
        'rf_of_MC_in_selection_horizon': 0.46122782842437227,
        'rf_of_MC_in_investment_horizon': 0.5087360293033742,
    },
    {
        'day_t': '2016-03-22',
        'total_AR_of_central_portfolios': -0.003802816901408449,
        'total_AR_of_peripheral_portfolios': -0.0030047370892019544,
        'total_AR_of_random_portfolios': -0.00408452112676061,
        'rd_of_MC_in_selection_horizon': 0.5023255813953489,
        'rd_of_MC_in_investment_horizon': 0.46261682242990654,
        'rf_of_MC_in_selection_horizon': 0.49275263819773224,
        'rf_of_MC_in_investment_horizon': 0.50447144445489,
    },
    {
        'day_t': '2016-04-21',
        'total_AR_of_central_portfolios': -0.0006071830985915469,
        'total_AR_of_peripheral_portfolios': 0.0014148873239436623,
        'total_AR_of_random_portfolios': -0.0034271924882628845,
        'rd_of_MC_in_selection_horizon': 0.49767441860465117,
        'rd_of_MC_in_investment_horizon': 0.4766355140186916,
        'rf_of_MC_in_selection_horizon': 0.5063861842193423,
        'rf_of_MC_in_investment_horizon': 0.5069022793683196,
    },
    {
        'day_t': '2016-05-21',
        'total_AR_of_central_portfolios': -0.007757009345794386,
        'total_AR_of_peripheral_portfolios': -0.0021755140186915907,
        'total_AR_of_random_portfolios': -0.055934546728971926,
        'rd_of_MC_in_selection_horizon': 0.48372093023255813,
        'rd_of_MC_in_investment_horizon': 0.49767441860465117,
        'rf_of_MC_in_selection_horizon': 0.49694265055740355,
        'rf_of_MC_in_investment_horizon': 0.5464616412152113,
    },
    {
        'day_t': '2016-06-20',
        'total_AR_of_central_portfolios': 0.0012206572769953008,
        'total_AR_of_peripheral_portfolios': 0.014381882629107995,
        'total_AR_of_random_portfolios': 0.012629107981220657,
        'rd_of_MC_in_selection_horizon': 0.48372093023255813,
        'rd_of_MC_in_investment_horizon': 0.4953271028037383,
        'rf_of_MC_in_selection_horizon': 0.5124191872660072,
        'rf_of_MC_in_investment_horizon': 0.5448353851508614,
    },
    {
        'day_t': '2016-07-20',
        'total_AR_of_central_portfolios': -0.009295774647887327,
        'total_AR_of_peripheral_portfolios': -0.0003436760563380476,
        'total_AR_of_random_portfolios': -0.0006572816901408637,
        'rd_of_MC_in_selection_horizon': 0.48372093023255813,
        'rd_of_MC_in_investment_horizon': 0.5046728971962616,
        'rf_of_MC_in_selection_horizon': 0.5008650176882653,
        'rf_of_MC_in_investment_horizon': 0.5947480569146885,
    },
    {
        'day_t': '2016-08-19',
        'total_AR_of_central_portfolios': 0.003145483568075047,
        'total_AR_of_peripheral_portfolios': 0.005539896713615017,
        'total_AR_of_random_portfolios': 0.00577469953051649,
        'rd_of_MC_in_selection_horizon': 0.4930232558139535,
        'rd_of_MC_in_investment_horizon': 0.4953271028037383,
        'rf_of_MC_in_selection_horizon': 0.4967955588926642,
        'rf_of_MC_in_investment_horizon': 0.5831379459096251,
    },
    {
        'day_t': '2016-09-18',
        'total_AR_of_central_portfolios': 0.0063551448598131045,
        'total_AR_of_peripheral_portfolios': -0.0002018224299065434,
        'total_AR_of_random_portfolios': 0.018457962616822463,
        'rd_of_MC_in_selection_horizon': 0.48372093023255813,
        'rd_of_MC_in_investment_horizon': 0.5162790697674419,
        'rf_of_MC_in_selection_horizon': 0.4889682800090717,
        'rf_of_MC_in_investment_horizon': 0.6088508225755326,
    },
    {
        'day_t': '2016-10-18',
        'total_AR_of_central_portfolios': -0.0013614976525821434,
        'total_AR_of_peripheral_portfolios': -0.0004583098591549298,
        'total_AR_of_random_portfolios': -0.005399028169014029,
        'rd_of_MC_in_selection_horizon': 0.4930232558139535,
        'rd_of_MC_in_investment_horizon': 0.5186915887850467,
        'rf_of_MC_in_selection_horizon': 0.5137152905806623,
        'rf_of_MC_in_investment_horizon': 0.616840554235277,
    },
    {
        'day_t': '2016-11-17',
        'total_AR_of_central_portfolios': 0.0023004741784037742,
        'total_AR_of_peripheral_portfolios': -0.0007051690140845051,
        'total_AR_of_random_portfolios': -0.0026760281690140484,
        'rd_of_MC_in_selection_horizon': 0.4883720930232558,
        'rd_of_MC_in_investment_horizon': 0.5233644859813084,
        'rf_of_MC_in_selection_horizon': 0.5155246036611972,
        'rf_of_MC_in_investment_horizon': 0.6268338820580481,
    },
    {
        'day_t': '2016-12-17',
        'total_AR_of_central_portfolios': -0.002102803738317758,
        'total_AR_of_peripheral_portfolios': -0.0015887897196261817,
        'total_AR_of_random_portfolios': -0.025560738317757,
        'rd_of_MC_in_selection_horizon': 0.48372093023255813,
        'rd_of_MC_in_investment_horizon': 0.5302325581395348,
        'rf_of_MC_in_selection_horizon': 0.5087360293033742,
        'rf_of_MC_in_investment_horizon': 0.6042149916151307,
    },
    {
        'day_t': '2017-01-16',
        'total_AR_of_central_portfolios': -0.002816892018779348,
        'total_AR_of_peripheral_portfolios': 0.01056343661971838,
        'total_AR_of_random_portfolios': 0.03061033333333333,
        'rd_of_MC_in_selection_horizon': 0.4604651162790698,
        'rd_of_MC_in_investment_horizon': 0.5186915887850467,
        'rf_of_MC_in_selection_horizon': 0.4998183446398283,
        'rf_of_MC_in_investment_horizon': 0.5890446374509428,
    },
    {
        'day_t': '2017-02-15',
        'total_AR_of_central_portfolios': -0.0023004647887323966,
        'total_AR_of_peripheral_portfolios': -0.012214629107981255,
        'total_AR_of_random_portfolios': -0.01042250704225348,
        'rd_of_MC_in_selection_horizon': 0.4790697674418605,
        'rd_of_MC_in_investment_horizon': 0.5,
        'rf_of_MC_in_selection_horizon': 0.507425048777595,
        'rf_of_MC_in_investment_horizon': 0.5659791514833733,
    },
    {
        'day_t': '2017-03-17',
        'total_AR_of_central_portfolios': -0.0017370938967136203,
        'total_AR_of_peripheral_portfolios': 0.0038523474178403746,
        'total_AR_of_random_portfolios': 0.0015022863849764572,
        'rd_of_MC_in_selection_horizon': 0.49767441860465117,
        'rd_of_MC_in_investment_horizon': 0.5046728971962616,
        'rf_of_MC_in_selection_horizon': 0.5464616412152113,
        'rf_of_MC_in_investment_horizon': 0.5725954258510525,
    },
    {
        'day_t': '2017-04-16',
        'total_AR_of_central_portfolios': -0.00439253271028037,
        'total_AR_of_peripheral_portfolios': -0.0006045794392523346,
        'total_AR_of_random_portfolios': -0.01303744859813091,
        'rd_of_MC_in_selection_horizon': 0.49767441860465117,
        'rd_of_MC_in_investment_horizon': 0.5116279069767442,
        'rf_of_MC_in_selection_horizon': 0.5448623282977838,
        'rf_of_MC_in_investment_horizon': 0.5643416804771229,
    },
    {
        'day_t': '2017-05-16',
        'total_AR_of_central_portfolios': 0.0022065539906103073,
        'total_AR_of_peripheral_portfolios': 0.00103093896713615,
        'total_AR_of_random_portfolios': 0.029624399061032862,
        'rd_of_MC_in_selection_horizon': 0.5023255813953489,
        'rd_of_MC_in_investment_horizon': 0.5233644859813084,
        'rf_of_MC_in_selection_horizon': 0.579950314625476,
        'rf_of_MC_in_investment_horizon': 0.5617998960071289,
    },

]
b = [
    {
        'day_t': '2014-06-01',
        'total_AR_of_central_portfolios': -0.0315153441860465,
        'total_AR_of_peripheral_portfolios': 0.02717079534883722,
        'total_AR_of_random_portfolios': -0.014392693023255822,
    },
    {
        'day_t': '2014-07-01',
        'total_AR_of_central_portfolios': 0.03664343720930234,
        'total_AR_of_peripheral_portfolios': 0.10182981395348836,
        'total_AR_of_random_portfolios': 0.08177744186046512,
    },
    {
        'day_t': '2014-07-31',
        'total_AR_of_central_portfolios': 0.06051161395348836,
        'total_AR_of_peripheral_portfolios': 0.02328232558139535,
        'total_AR_of_random_portfolios': 0.07402702325581396,
    },
    {
        'day_t': '2014-08-30',
        'total_AR_of_central_portfolios': 0.5817116325581395,
        'total_AR_of_peripheral_portfolios': 0.0633953488372093,
        'total_AR_of_random_portfolios': 0.22192744186046512,
    },
    {
        'day_t': '2014-09-29',
        'total_AR_of_central_portfolios': -0.008511627906976736,
        'total_AR_of_peripheral_portfolios': 0.06753945581395349,
        'total_AR_of_random_portfolios': 0.009906990697674445,
    },
    {
        'day_t': '2014-10-29',
        'total_AR_of_central_portfolios': 0.25451162790697673,
        'total_AR_of_peripheral_portfolios': 0.0013745999999999945,
        'total_AR_of_random_portfolios': 4.3395348837221154e-05,
    },
    {
        'day_t': '2014-11-28',
        'total_AR_of_central_portfolios': 0.025350837209302316,
        'total_AR_of_peripheral_portfolios': -0.0644121069767442,
        'total_AR_of_random_portfolios': 0.04003986511627907,
    },
    {
        'day_t': '2014-12-28',
        'total_AR_of_central_portfolios': 0.06001490232558141,
        'total_AR_of_peripheral_portfolios': -0.03322669767441861,
        'total_AR_of_random_portfolios': -0.009730325581395347,
    },
    {
        'day_t': '2015-01-27',
        'total_AR_of_central_portfolios': -0.013251860465116286,
        'total_AR_of_peripheral_portfolios': -0.04706977209302325,
        'total_AR_of_random_portfolios': -0.0031009302325581425,
    },
    {
        'day_t': '2015-02-26',
        'total_AR_of_central_portfolios': -0.06399999999999999,
        'total_AR_of_peripheral_portfolios': -0.03636348837209303,
        'total_AR_of_random_portfolios': 0.0954271488372093,
    },
    {
        'day_t': '2015-03-28',
        'total_AR_of_central_portfolios': -0.05502325581395348,
        'total_AR_of_peripheral_portfolios': 0.006580893023255883,
        'total_AR_of_random_portfolios': -0.015255762790697626,
    },
    {
        'day_t': '2015-04-27',
        'total_AR_of_central_portfolios': -0.03401706976744186,
        'total_AR_of_peripheral_portfolios': -0.046,
        'total_AR_of_random_portfolios': -0.11249439534883723,
    },
    {
        'day_t': '2015-05-27',
        'total_AR_of_central_portfolios': -0.05692767441860465,
        'total_AR_of_peripheral_portfolios': 0.020410883720930237,
        'total_AR_of_random_portfolios': -0.009120702325581386,
    },
    {
        'day_t': '2015-06-26',
        'total_AR_of_central_portfolios': 0.02714953023255816,
        'total_AR_of_peripheral_portfolios': -0.02272087906976742,
        'total_AR_of_random_portfolios': -0.022012744186046512,
    },
    {
        'day_t': '2015-07-26',
        'total_AR_of_central_portfolios': 0.0070622325581395275,
        'total_AR_of_peripheral_portfolios': -0.023069767441860446,
        'total_AR_of_random_portfolios': -0.042312795348837216,
    },
    {
        'day_t': '2015-08-25',
        'total_AR_of_central_portfolios': 0.025545488372093025,
        'total_AR_of_peripheral_portfolios': 0.018673302325581394,
        'total_AR_of_random_portfolios': 0.052670916279069765,
    },
    {
        'day_t': '2015-09-24',
        'total_AR_of_central_portfolios': -0.00811227906976744,
        'total_AR_of_peripheral_portfolios': -0.008597488372093022,
        'total_AR_of_random_portfolios': -0.001379860465116275,
    },
    {
        'day_t': '2015-10-24',
        'total_AR_of_central_portfolios': -0.005557265116279081,
        'total_AR_of_peripheral_portfolios': -0.2333798372093023,
        'total_AR_of_random_portfolios': -0.22986044186046506,
    },
    {
        'day_t': '2015-11-23',
        'total_AR_of_central_portfolios': -0.03351743720930232,
        'total_AR_of_peripheral_portfolios': -0.03652093023255814,
        'total_AR_of_random_portfolios': 0.02057366511627911,
    },
    {
        'day_t': '2015-12-23',
        'total_AR_of_central_portfolios': 0.0036942325581395354,
        'total_AR_of_peripheral_portfolios': 0.05308043255813955,
        'total_AR_of_random_portfolios': -0.46116272093023253,
    },
    {
        'day_t': '2016-01-22',
        'total_AR_of_central_portfolios': -0.009311906976744182,
        'total_AR_of_peripheral_portfolios': 0.04446512558139536,
        'total_AR_of_random_portfolios': 0.012291348837209299,
    },
    {
        'day_t': '2016-02-21',
        'total_AR_of_central_portfolios': -0.03731325581395347,
        'total_AR_of_peripheral_portfolios': 0.04760813488372091,
        'total_AR_of_random_portfolios': 0.0423198976744186,
    },
    {
        'day_t': '2016-03-22',
        'total_AR_of_central_portfolios': -0.0558514511627907,
        'total_AR_of_peripheral_portfolios': 0.0046653488372093,
        'total_AR_of_random_portfolios': -0.003767441860465114,
    },
    {
        'day_t': '2016-04-21',
        'total_AR_of_central_portfolios': -0.2811017162790697,
        'total_AR_of_peripheral_portfolios': 0.0015901162790697997,
        'total_AR_of_random_portfolios': -0.26028278139534883,
    },
    {
        'day_t': '2016-05-21',
        'total_AR_of_central_portfolios': 0.032232553488372076,
        'total_AR_of_peripheral_portfolios': 0.1533899348837209,
        'total_AR_of_random_portfolios': 0.13037472558139535,
    },
    {
        'day_t': '2016-06-20',
        'total_AR_of_central_portfolios': 0.19981395348837208,
        'total_AR_of_peripheral_portfolios': 0.03765893953488372,
        'total_AR_of_random_portfolios': 0.20413953953488373,
    },
    {
        'day_t': '2016-07-20',
        'total_AR_of_central_portfolios': 0.3027442558139536,
        'total_AR_of_peripheral_portfolios': 0.284,
        'total_AR_of_random_portfolios': 0.08381395348837209,
    },
    {
        'day_t': '2016-08-19',
        'total_AR_of_central_portfolios': 0.0428372046511628,
        'total_AR_of_peripheral_portfolios': 0.015466558139534884,
        'total_AR_of_random_portfolios': 0.0191593488372093,
    },
    {
        'day_t': '2016-09-18',
        'total_AR_of_central_portfolios': 0.2801257395348837,
        'total_AR_of_peripheral_portfolios': 0.24869767906976745,
        'total_AR_of_random_portfolios': 0.2620930418604651,
    },
    {
        'day_t': '2016-10-18',
        'total_AR_of_central_portfolios': 0.15950066511627922,
        'total_AR_of_peripheral_portfolios': 0.34451677674418607,
        'total_AR_of_random_portfolios': 0.11184596744186057,
    },
    {
        'day_t': '2016-11-17',
        'total_AR_of_central_portfolios': 0.0777315953488372,
        'total_AR_of_peripheral_portfolios': 0.08818604186046511,
        'total_AR_of_random_portfolios': 0.05646513023255814,
    },
    {
        'day_t': '2016-12-17',
        'total_AR_of_central_portfolios': 0.020135674418604643,
        'total_AR_of_peripheral_portfolios': 0.4689767488372094,
        'total_AR_of_random_portfolios': 0.14762695813953491,
    },
    {
        'day_t': '2017-01-16',
        'total_AR_of_central_portfolios': 0.13911626976744187,
        'total_AR_of_peripheral_portfolios': 0.09079455813953488,
        'total_AR_of_random_portfolios': 0.06595348372093024,
    },
    {
        'day_t': '2017-02-15',
        'total_AR_of_central_portfolios': -0.08334885116279073,
        'total_AR_of_peripheral_portfolios': 0.08853546511627904,
        'total_AR_of_random_portfolios': 0.15967439534883718,
    },
    {
        'day_t': '2017-03-17',
        'total_AR_of_central_portfolios': 0.09025977209302327,
        'total_AR_of_peripheral_portfolios': 0.018596176744186038,
        'total_AR_of_random_portfolios': 0.07493025116279071,
    },
    {
        'day_t': '2017-04-16',
        'total_AR_of_central_portfolios': 0.11811681395348841,
        'total_AR_of_peripheral_portfolios': -0.05390697209302324,
        'total_AR_of_random_portfolios': 0.04483720930232558,
    },
    {
        'day_t': '2017-05-16',
        'total_AR_of_central_portfolios': 0.0874106418604651,
        'total_AR_of_peripheral_portfolios': 0.022325586046511622,
        'total_AR_of_random_portfolios': 0.03798748372093025,
    },
]
c = [
]
dateArray = []
# rf_of_MC_in_selection_horizon_array_d = []
# rf_of_MC_in_selection_horizon_array_c = []
# rf_of_MC_in_selection_horizon_array_dd = []
# rf_of_MC_in_selection_horizon_array_dis = []
rf_of_MC_in_selection_horizon_array_corr = []
# a=sorted(a10Degree, key=lambda student: student['day_t'])
# b=sorted(a10C, key=lambda student: student['day_t'])
# c=sorted(a10DDegree, key=lambda student: student['day_t'])
# d= sorted(a10Distance, key=lambda student: student['day_t'])
e = sorted(a10Correlation, key=lambda student: student['day_t'])

for o in a:
    string_day = o['day_t']
    dtime = datetime.date(int(string_day[:4]), int(
        string_day[5:7]), int(string_day[8:10]))
    dateArray.append(dtime)
for o in a:
    string_day = o['total_AR_of_central_portfolios']
    rf_of_MC_in_selection_horizon_array_d.append(string_day)
for o in b:
    string_day = o['total_AR_of_central_portfolios']
    rf_of_MC_in_selection_horizon_array_c.append(string_day)
for o in c:
    string_day = o['total_AR_of_central_portfolios']
    rf_of_MC_in_selection_horizon_array_dd.append(string_day)
for o in d:
    string_day = o['total_AR_of_central_portfolios']
    rf_of_MC_in_selection_horizon_array_dis.append(string_day)
for o in e:
    string_day = o['total_AR_of_central_portfolios']
    rf_of_MC_in_selection_horizon_array_corr.append(string_day)
# sum = 0
# for o in a:
#     sum += o[''total_AR_of_peripheral_portfolios'']

# print(sum)
plt.plot_date(dateArray, rf_of_MC_in_selection_horizon_array_d, 'y-')
plt.plot_date(dateArray, rf_of_MC_in_selection_horizon_array_corr, 'r-')
plt.plot_date(dateArray,
              rf_of_MC_in_selection_horizon_array_dd, 'b-',)
plt.plot_date(dateArray, rf_of_MC_in_selection_horizon_array_dis, 'g-',)
plt.plot_date(dateArray, rf_of_MC_in_selection_horizon_array_corr, 'k-')
plt.legend(['Degree', 'Closeness', 'DDegree', 'Distance',  'Correlation'])

plt.show()
