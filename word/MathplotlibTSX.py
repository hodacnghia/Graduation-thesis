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
        'total_AR_of_central_portfolios': -0.0076699223300970955,
        'total_AR_of_peripheral_portfolios': -0.0024433786407767294,
        'total_AR_of_random_portfolios': -0.013082504854368895,
        'rd_of_MC_in_selection_horizon': 0.5970873786407767,
        'rd_of_MC_in_investment_horizon': 0.5507246376811594,
        'rf_of_MC_in_selection_horizon': 0.597743825324889,
        'rf_of_MC_in_investment_horizon': 0.503991187598524,
    },

    {
        'day_t': '2014-07-01',
        'total_AR_of_central_portfolios': -0.007073200000000033,
        'total_AR_of_peripheral_portfolios': -0.0003442390243902049,
        'total_AR_of_random_portfolios': -0.0029511853658535743,
        'rd_of_MC_in_selection_horizon': 0.6183574879227053,
        'rd_of_MC_in_investment_horizon': 0.5339805825242718,
        'rf_of_MC_in_selection_horizon': 0.6145727893005277,
        'rf_of_MC_in_investment_horizon': 0.5040182825029076,
    },
    {
        'day_t': '2014-07-31',
        'total_AR_of_central_portfolios': 0.007107843137254901,
        'total_AR_of_peripheral_portfolios': 0.002303921568627437,
        'total_AR_of_random_portfolios': -0.009950970588235308,
        'rd_of_MC_in_selection_horizon': 0.6183574879227053,
        'rd_of_MC_in_investment_horizon': 0.5317073170731708,
        'rf_of_MC_in_selection_horizon': 0.6206062772142298,
        'rf_of_MC_in_investment_horizon': 0.49690450480983334,
    },
    {
        'day_t': '2014-08-30',
        'total_AR_of_central_portfolios': -0.005242728155339855,
        'total_AR_of_peripheral_portfolios': 0.00548548058252426,
        'total_AR_of_random_portfolios': -0.0021602281553398457,
        'rd_of_MC_in_selection_horizon': 0.6086956521739131,
        'rd_of_MC_in_investment_horizon': 0.5169082125603864,
        'rf_of_MC_in_selection_horizon': 0.6077114946281644,
        'rf_of_MC_in_investment_horizon': 0.47703745888336174,
    },
    {
        'day_t': '2014-09-29',
        'total_AR_of_central_portfolios': 0.0024390439024390316,
        'total_AR_of_peripheral_portfolios': -0.00034146829268298504,
        'total_AR_of_random_portfolios': 0.003268263414634075,
        'rd_of_MC_in_selection_horizon': 0.587378640776699,
        'rd_of_MC_in_investment_horizon': 0.5339805825242718,
        'rf_of_MC_in_selection_horizon': 0.5756414169846661,
        'rf_of_MC_in_investment_horizon': 0.4789385235979459,
    },
    {
        'day_t': '2014-10-29',
        'total_AR_of_central_portfolios': -0.03975608780487802,
        'total_AR_of_peripheral_portfolios': -0.007365887804878074,
        'total_AR_of_random_portfolios': -0.019585331707317084,
        'rd_of_MC_in_selection_horizon': 0.5673076923076923,
        'rd_of_MC_in_investment_horizon': 0.5339805825242718,
        'rf_of_MC_in_selection_horizon': 0.5365712064976771,
        'rf_of_MC_in_investment_horizon': 0.4639791996224698,
    },
    {
        'day_t': '2014-11-28',
        'total_AR_of_central_portfolios': 0.006225490196078386,
        'total_AR_of_peripheral_portfolios': -0.0010657156862745724,
        'total_AR_of_random_portfolios': 0.0007843088235294209,
        'rd_of_MC_in_selection_horizon': 0.5769230769230769,
        'rd_of_MC_in_investment_horizon': 0.5219512195121951,
        'rf_of_MC_in_selection_horizon': 0.5488969735615102,
        'rf_of_MC_in_investment_horizon': 0.46663590270874217,
    },
    {
        'day_t': '2014-12-28',
        'total_AR_of_central_portfolios': 0.01330106310679615,
        'total_AR_of_peripheral_portfolios': -0.005776699029126233,
        'total_AR_of_random_portfolios': 0.005533941747572732,
        'rd_of_MC_in_selection_horizon': 0.5507246376811594,
        'rd_of_MC_in_investment_horizon': 0.5314009661835749,
        'rf_of_MC_in_selection_horizon': 0.5136414233974324,
        'rf_of_MC_in_investment_horizon': 0.48145090650792977,
    },
    {
        'day_t': '2015-02-26',
        'total_AR_of_central_portfolios': 0.022151830917874437,
        'total_AR_of_peripheral_portfolios': -0.009617893719806722,
        'total_AR_of_random_portfolios': 0.005966178743961379,
        'rd_of_MC_in_selection_horizon': 0.5533980582524272,
        'rd_of_MC_in_investment_horizon': 0.5048076923076923,
        'rf_of_MC_in_selection_horizon': 0.5149940185646942,
        'rf_of_MC_in_investment_horizon': 0.45192838168128624,
    },
    {
        'day_t': '2015-03-28',
        'total_AR_of_central_portfolios': 0.028780478048780627,
        'total_AR_of_peripheral_portfolios': 0.000923931707317091,
        'total_AR_of_random_portfolios': 0.00551219024390243,
        'rd_of_MC_in_selection_horizon': 0.5507246376811594,
        'rd_of_MC_in_investment_horizon': 0.4854368932038835,
        'rf_of_MC_in_selection_horizon': 0.503991187598524,
        'rf_of_MC_in_investment_horizon': 0.44037605416040965,
    },
    {
        'day_t': '2016-12-17',
        'total_AR_of_central_portfolios': -0.008039240196078493,
        'total_AR_of_peripheral_portfolios': 0.01186272058823518,
        'total_AR_of_random_portfolios': 0.00039216176470584306,
        'rd_of_MC_in_selection_horizon': 0.5598086124401914,
        'rd_of_MC_in_investment_horizon': 0.5073170731707317,
        'rf_of_MC_in_selection_horizon': 0.5872247152724998,
        'rf_of_MC_in_investment_horizon': 0.5221360601422687,
    },
    {
        'day_t': '2017-01-16',
        'total_AR_of_central_portfolios': 0.014417470873786399,
        'total_AR_of_peripheral_portfolios': 0.023252296116505526,
        'total_AR_of_random_portfolios': 0.0015533737864077274,
        'rd_of_MC_in_selection_horizon': 0.5631067961165048,
        'rd_of_MC_in_investment_horizon': 0.5072463768115942,
        'rf_of_MC_in_selection_horizon': 0.5750763500807076,
        'rf_of_MC_in_investment_horizon': 0.5256483613912207,
    },
    {
        'day_t': '2017-02-15',
        'total_AR_of_central_portfolios': -0.00635923786407767,
        'total_AR_of_peripheral_portfolios': -0.004805810679611629,
        'total_AR_of_random_portfolios': -0.0038834805825243043,
        'rd_of_MC_in_selection_horizon': 0.5700483091787439,
        'rd_of_MC_in_investment_horizon': 0.4927536231884058,
        'rf_of_MC_in_selection_horizon': 0.5749392916499921,
        'rf_of_MC_in_investment_horizon': 0.510908477131093,
    },
    {
        'day_t': '2017-03-17',
        'total_AR_of_central_portfolios': 0.055196117647058784,
        'total_AR_of_peripheral_portfolios': -0.011176480392156784,
        'total_AR_of_random_portfolios': 0.021323470588235267,
        'rd_of_MC_in_selection_horizon': 0.5679611650485437,
        'rd_of_MC_in_investment_horizon': 0.5219512195121951,
        'rf_of_MC_in_selection_horizon': 0.5579176936133146,
        'rf_of_MC_in_investment_horizon': 0.5397728625836751,
    },
    {
        'day_t': '2017-04-16',
        'total_AR_of_central_portfolios': 0.0145630825242717,
        'total_AR_of_peripheral_portfolios': -0.01631066504854363,
        'total_AR_of_random_portfolios': 0.002038883495145784,
        'rd_of_MC_in_selection_horizon': 0.5728155339805825,
        'rd_of_MC_in_investment_horizon': 0.4975845410628019,
        'rf_of_MC_in_selection_horizon': 0.5576048511019513,
        'rf_of_MC_in_investment_horizon': 0.4708544488296055,
    },
    {
        'day_t': '2017-05-16',
        'total_AR_of_central_portfolios': 0.01813726470588242,
        'total_AR_of_peripheral_portfolios': -0.10142141176470595,
        'total_AR_of_random_portfolios': -0.0039215686274509925,
        'rd_of_MC_in_selection_horizon': 0.5555555555555556,
        'rd_of_MC_in_investment_horizon': 0.5170731707317073,
        'rf_of_MC_in_selection_horizon': 0.5382807171772692,
        'rf_of_MC_in_investment_horizon': 0.515392962254425,
    },

    {
        'day_t': '2015-01-27',
        'total_AR_of_central_portfolios': 0.00931784951456311,
        'total_AR_of_peripheral_portfolios': -0.014527082524271918,
        'total_AR_of_random_portfolios': -0.01538836893203884,
        'rd_of_MC_in_selection_horizon': 0.5436893203883495,
        'rd_of_MC_in_investment_horizon': 0.5120772946859904,
        'rf_of_MC_in_selection_horizon': 0.5119845780110706,
        'rf_of_MC_in_investment_horizon': 0.46780990563532265,
    },
    {
        'day_t': '2015-04-27',
        'total_AR_of_central_portfolios': -0.01950368137254899,
        'total_AR_of_peripheral_portfolios': 0.00392161274509805,
        'total_AR_of_random_portfolios': -0.002598039215686281,
        'rd_of_MC_in_selection_horizon': 0.5339805825242718,
        'rd_of_MC_in_investment_horizon': 0.47317073170731705,
        'rf_of_MC_in_selection_horizon': 0.5040182825029076,
        'rf_of_MC_in_investment_horizon': 0.4459399944451558,
    },
    {
        'day_t': '2015-05-27',
        'total_AR_of_central_portfolios': -0.015197190243902434,
        'total_AR_of_peripheral_portfolios': 0.006780507317073229,
        'total_AR_of_random_portfolios': 0.0034146243902438977,
        'rd_of_MC_in_selection_horizon': 0.529126213592233,
        'rd_of_MC_in_investment_horizon': 0.49029126213592233,
        'rf_of_MC_in_selection_horizon': 0.49353993756764303,
        'rf_of_MC_in_investment_horizon': 0.465864697706606,
    },
    {
        'day_t': '2015-06-26',
        'total_AR_of_central_portfolios': -0.006232475490196143,
        'total_AR_of_peripheral_portfolios': -0.019754882352941122,
        'total_AR_of_random_portfolios': -0.018039200980392175,
        'rd_of_MC_in_selection_horizon': 0.5169082125603864,
        'rd_of_MC_in_investment_horizon': 0.4975609756097561,
        'rf_of_MC_in_selection_horizon': 0.47703745888336174,
        'rf_of_MC_in_investment_horizon': 0.4868173770618521,
    },
    {
        'day_t': '2015-07-26',
        'total_AR_of_central_portfolios': -0.015987713592233017,
        'total_AR_of_peripheral_portfolios': 0.0083494805825243,
        'total_AR_of_random_portfolios': -0.0037378834951456146,
        'rd_of_MC_in_selection_horizon': 0.5314009661835749,
        'rd_of_MC_in_investment_horizon': 0.4927536231884058,
        'rf_of_MC_in_selection_horizon': 0.47851159396409976,
        'rf_of_MC_in_investment_horizon': 0.49819527831045396,
    },
    {
        'day_t': '2015-08-25',
        'total_AR_of_central_portfolios': -0.09229265853658536,
        'total_AR_of_peripheral_portfolios': -0.04946338048780488,
        'total_AR_of_random_portfolios': -0.039707282926829325,
        'rd_of_MC_in_selection_horizon': 0.5314009661835749,
        'rd_of_MC_in_investment_horizon': 0.49514563106796117,
        'rf_of_MC_in_selection_horizon': 0.46222487120893596,
        'rf_of_MC_in_investment_horizon': 0.5149349162095751,
    },
    {
        'day_t': '2015-09-24',
        'total_AR_of_central_portfolios': 0.050585336585365785,
        'total_AR_of_peripheral_portfolios': 0.035053395121951283,
        'total_AR_of_random_portfolios': 0.03726827804878049,
        'rd_of_MC_in_selection_horizon': 0.5194174757281553,
        'rd_of_MC_in_investment_horizon': 0.5048543689320388,
        'rf_of_MC_in_selection_horizon': 0.4637640064769215,
        'rf_of_MC_in_investment_horizon': 0.528600164715158,
    },
    {
        'day_t': '2015-10-24',
        'total_AR_of_central_portfolios': 0.014271830097087275,
        'total_AR_of_peripheral_portfolios': 0.0006310533980582198,
        'total_AR_of_random_portfolios': 0.027184524271844736,
        'rd_of_MC_in_selection_horizon': 0.5314009661835749,
        'rd_of_MC_in_investment_horizon': 0.5024154589371981,
        'rf_of_MC_in_selection_horizon': 0.48145090650792977,
        'rf_of_MC_in_investment_horizon': 0.5239901923620032,
    },
    {
        'day_t': '2015-11-23',
        'total_AR_of_central_portfolios': 0.0005391666666667005,
        'total_AR_of_peripheral_portfolios': -0.005354936274509819,
        'total_AR_of_random_portfolios': -0.009362720588235252,
        'rd_of_MC_in_selection_horizon': 0.5096153846153846,
        'rd_of_MC_in_investment_horizon': 0.5365853658536586,
        'rf_of_MC_in_selection_horizon': 0.4621782518608009,
        'rf_of_MC_in_investment_horizon': 0.5288609105955662,
    },
    {
        'day_t': '2015-12-23',
        'total_AR_of_central_portfolios': 0.01275862068965519,
        'total_AR_of_peripheral_portfolios': 0.0023152758620689383,
        'total_AR_of_random_portfolios': -0.0014285714285714249,
        'rd_of_MC_in_selection_horizon': 0.5023923444976076,
        'rd_of_MC_in_investment_horizon': 0.5294117647058824,
        'rf_of_MC_in_selection_horizon': 0.45177463229738635,
        'rf_of_MC_in_investment_horizon': 0.5422289831713911,
    },
    {
        'day_t': '2016-08-19',
        'total_AR_of_central_portfolios': -0.02624388780487818,
        'total_AR_of_peripheral_portfolios': 0.029658551219512237,
        'total_AR_of_random_portfolios': -0.007463439024390255,
        'rd_of_MC_in_selection_horizon': 0.5024154589371981,
        'rd_of_MC_in_investment_horizon': 0.5388349514563107,
        'rf_of_MC_in_selection_horizon': 0.5239901923620032,
        'rf_of_MC_in_investment_horizon': 0.5151713708493474,
    },
    {
        'day_t': '2016-09-18',
        'total_AR_of_central_portfolios': -0.013155359223300979,
        'total_AR_of_peripheral_portfolios': -0.007378689320388342,
        'total_AR_of_random_portfolios': -0.016893199029126213,
        'rd_of_MC_in_selection_horizon': 0.5388349514563107,
        'rd_of_MC_in_investment_horizon': 0.5169082125603864,
        'rf_of_MC_in_selection_horizon': 0.5295223042656747,
        'rf_of_MC_in_investment_horizon': 0.5255477603535484,
    },
    {
        'day_t': '2016-10-18',
        'total_AR_of_central_portfolios': 0.012048824390243993,
        'total_AR_of_peripheral_portfolios': -0.0032195170731708278,
        'total_AR_of_random_portfolios': 0.007463482926829412,
        'rd_of_MC_in_selection_horizon': 0.5317073170731708,
        'rd_of_MC_in_investment_horizon': 0.5097087378640777,
        'rf_of_MC_in_selection_horizon': 0.5428953749714863,
        'rf_of_MC_in_investment_horizon': 0.5109116918332823,
    },
    {
        'day_t': '2016-11-17',
        'total_AR_of_central_portfolios': -0.01985291666666659,
        'total_AR_of_peripheral_portfolios': -0.004754926470588229,
        'total_AR_of_random_portfolios': -0.013774475490196114,
        'rd_of_MC_in_selection_horizon': 0.5480769230769231,
        'rd_of_MC_in_investment_horizon': 0.4975609756097561,
        'rf_of_MC_in_selection_horizon': 0.576377870131146,
        'rf_of_MC_in_investment_horizon': 0.5106947430309929,
    },

    {
        'day_t': '2016-01-22',
        'total_AR_of_central_portfolios': -0.03038834951456314,
        'total_AR_of_peripheral_portfolios': -0.015825257281553415,
        'total_AR_of_random_portfolios': -0.025534004854368953,
        'rd_of_MC_in_selection_horizon': 0.4854368932038835,
        'rd_of_MC_in_investment_horizon': 0.5507246376811594,
        'rf_of_MC_in_selection_horizon': 0.44037605416040965,
        'rf_of_MC_in_investment_horizon': 0.5854214296882347,
    },
    {
        'day_t': '2016-02-21',
        'total_AR_of_central_portfolios': 0.03163464423076913,
        'total_AR_of_peripheral_portfolios': -0.010961543269230756,
        'total_AR_of_random_portfolios': 0.00999997115384615,
        'rd_of_MC_in_selection_horizon': 0.47572815533980584,
        'rd_of_MC_in_investment_horizon': 0.5598086124401914,
        'rf_of_MC_in_selection_horizon': 0.4459872956479804,
        'rf_of_MC_in_investment_horizon': 0.5872247152724998,
    },
    {
        'day_t': '2016-03-22',
        'total_AR_of_central_portfolios': 0.03676474509803943,
        'total_AR_of_peripheral_portfolios': -0.0038724950980390457,
        'total_AR_of_random_portfolios': 0.0038725049019607614,
        'rd_of_MC_in_selection_horizon': 0.48792270531400966,
        'rd_of_MC_in_investment_horizon': 0.5658536585365853,
        'rf_of_MC_in_selection_horizon': 0.46579571689270965,
        'rf_of_MC_in_investment_horizon': 0.5800765554973561,
    },
    {
        'day_t': '2016-04-21',
        'total_AR_of_central_portfolios': 0.016195190243902355,
        'total_AR_of_peripheral_portfolios': 0.027463434146341434,
        'total_AR_of_random_portfolios': 0.01004879512195123,
        'rd_of_MC_in_selection_horizon': 0.49514563106796117,
        'rd_of_MC_in_investment_horizon': 0.5728155339805825,
        'rf_of_MC_in_selection_horizon': 0.4802084035549508,
        'rf_of_MC_in_investment_horizon': 0.575255408494719,
    },
    {
        'day_t': '2016-05-21',
        'total_AR_of_central_portfolios': -0.01385366341463408,
        'total_AR_of_peripheral_portfolios': -0.013707351219512222,
        'total_AR_of_random_portfolios': -0.009902419512195131,
        'rd_of_MC_in_selection_horizon': 0.4927536231884058,
        'rd_of_MC_in_investment_horizon': 0.5679611650485437,
        'rf_of_MC_in_selection_horizon': 0.49819527831045396,
        'rf_of_MC_in_investment_horizon': 0.5579176936133146,
    },
    {
        'day_t': '2016-06-20',
        'total_AR_of_central_portfolios': -0.0009803382352941016,
        'total_AR_of_peripheral_portfolios': -0.009411799019607803,
        'total_AR_of_random_portfolios': 0.002647014705882355,
        'rd_of_MC_in_selection_horizon': 0.4975845410628019,
        'rd_of_MC_in_investment_horizon': 0.5756097560975609,
        'rf_of_MC_in_selection_horizon': 0.5201544743858806,
        'rf_of_MC_in_investment_horizon': 0.5577231761754448,
    },
    {
        'day_t': '2016-07-20',
        'total_AR_of_central_portfolios': -0.019951146341463305,
        'total_AR_of_peripheral_portfolios': -0.005024395121951286,
        'total_AR_of_random_portfolios': -0.0023902585365853037,
        'rd_of_MC_in_selection_horizon': 0.5072463768115942,
        'rd_of_MC_in_investment_horizon': 0.5533980582524272,
        'rf_of_MC_in_selection_horizon': 0.5295298054269655,
        'rf_of_MC_in_investment_horizon': 0.5371506197801983,
    },


]
b = [
    {
        'day_t': '2014-06-01',
        'total_AR_of_central_portfolios': -0.044202893719806846,
        'total_AR_of_peripheral_portfolios': 0.2646377053140096,
        'total_AR_of_random_portfolios': 0.37922707246376774,
    },
    {
        'day_t': '2014-07-01',
        'total_AR_of_central_portfolios': 0.14244228640776688,
        'total_AR_of_peripheral_portfolios': -0.02315530582524264,
        'total_AR_of_random_portfolios': 0.12461164077669906,
    },
    {
        'day_t': '2014-07-31',
        'total_AR_of_central_portfolios': -0.45684731067961165,
        'total_AR_of_peripheral_portfolios': 0.17150489805825248,
        'total_AR_of_random_portfolios': -0.19761163592233005,
    },
    {
        'day_t': '2014-08-30',
        'total_AR_of_central_portfolios': -0.4945304927536231,
        'total_AR_of_peripheral_portfolios': 0.1809903429951691,
        'total_AR_of_random_portfolios': -0.08739128502415461,
    },
    {
        'day_t': '2014-09-29',
        'total_AR_of_central_portfolios': -0.6561835942028986,
        'total_AR_of_peripheral_portfolios': -0.24342994685990335,
        'total_AR_of_random_portfolios': -0.07398546859903374,
    },
    {
        'day_t': '2014-10-29',
        'total_AR_of_central_portfolios': -0.6552656714975845,
        'total_AR_of_peripheral_portfolios': -0.32528002415458945,
        'total_AR_of_random_portfolios': -0.44289850724637686,
    },
    {
        'day_t': '2014-11-28',
        'total_AR_of_central_portfolios': -0.387524281553398,
        'total_AR_of_peripheral_portfolios': -0.2138835242718447,
        'total_AR_of_random_portfolios': -0.06446600970873789,
    },
    {
        'day_t': '2014-12-28',
        'total_AR_of_central_portfolios': -0.34231884057971007,
        'total_AR_of_peripheral_portfolios': -0.17323671497584542,
        'total_AR_of_random_portfolios': 1.022608661835748,
    },
    {
        'day_t': '2015-01-27',
        'total_AR_of_central_portfolios': -0.21225728846153838,
        'total_AR_of_peripheral_portfolios': -0.3266826634615383,
        'total_AR_of_random_portfolios': -0.32648564423076915,
    },
    {
        'day_t': '2015-02-26',
        'total_AR_of_central_portfolios': -0.5336216315789472,
        'total_AR_of_peripheral_portfolios': -0.27406701435406705,
        'total_AR_of_random_portfolios': -0.3031578708133971,
    },
    {
        'day_t': '2015-03-28',
        'total_AR_of_central_portfolios': -0.3380582475728154,
        'total_AR_of_peripheral_portfolios': -0.3794174757281554,
        'total_AR_of_random_portfolios': -0.41252426213592214,
    },
    {
        'day_t': '2015-04-27',
        'total_AR_of_central_portfolios': -0.5463592281553397,
        'total_AR_of_peripheral_portfolios': -0.24626212621359225,
        'total_AR_of_random_portfolios': -0.3696602281553398,
    },
    {
        'day_t': '2015-05-27',
        'total_AR_of_central_portfolios': -0.3921141256038647,
        'total_AR_of_peripheral_portfolios': -0.3335749323671497,
        'total_AR_of_random_portfolios': -0.37265700966183574,
    },
    {
        'day_t': '2015-06-26',
        'total_AR_of_central_portfolios': -0.13553396116504848,
        'total_AR_of_peripheral_portfolios': -0.021067951456310685,
        'total_AR_of_random_portfolios': -0.14679610194174758,
    },
    {
        'day_t': '2015-07-26',
        'total_AR_of_central_portfolios': 0.05046883574879231,
        'total_AR_of_peripheral_portfolios': -0.14942028985507247,
        'total_AR_of_random_portfolios': 0.10917874396135265,
    },
    {
        'day_t': '2015-08-25',
        'total_AR_of_central_portfolios': 0.15235179227053142,
        'total_AR_of_peripheral_portfolios': 0.08748791304347824,
        'total_AR_of_random_portfolios': 0.0023671835748793058,
    },
    {
        'day_t': '2015-09-24',
        'total_AR_of_central_portfolios': 0.2290661835748792,
        'total_AR_of_peripheral_portfolios': 0.1824637342995169,
        'total_AR_of_random_portfolios': 0.034380178743961404,
    },
    {
        'day_t': '2015-10-24',
        'total_AR_of_central_portfolios': -0.020231207729468507,
        'total_AR_of_peripheral_portfolios': 0.12275361835748791,
        'total_AR_of_random_portfolios': 0.15342994202898544,
    },
    {
        'day_t': '2015-11-23',
        'total_AR_of_central_portfolios': 0.28720058737864074,
        'total_AR_of_peripheral_portfolios': 0.16242722330097087,
        'total_AR_of_random_portfolios': 0.10694175242718444,
    },
    {
        'day_t': '2015-12-23',
        'total_AR_of_central_portfolios': 0.4121444926829268,
        'total_AR_of_peripheral_portfolios': 0.42009750243902405,
        'total_AR_of_random_portfolios': 0.2536585073170732,
    },
    {
        'day_t': '2016-01-22',
        'total_AR_of_central_portfolios': 0.46255583173076914,
        'total_AR_of_peripheral_portfolios': 1.0259616009615387,
        'total_AR_of_random_portfolios': 0.5434317596153847,
    },
    {
        'day_t': '2016-02-21',
        'total_AR_of_central_portfolios': 0.7182318038277512,
        'total_AR_of_peripheral_portfolios': 0.4825836937799042,
        'total_AR_of_random_portfolios': 0.38239233971291875,
    },
    {
        'day_t': '2016-03-22',
        'total_AR_of_central_portfolios': 0.2987826116504853,
        'total_AR_of_peripheral_portfolios': 0.6189319466019417,
        'total_AR_of_random_portfolios': 0.1851941456310679,
    },
    {
        'day_t': '2016-04-21',
        'total_AR_of_central_portfolios': 0.23529320772946857,
        'total_AR_of_peripheral_portfolios': 0.2449758550724637,
        'total_AR_of_random_portfolios': 0.2736394202898551,
    },
    {
        'day_t': '2016-05-21',
        'total_AR_of_central_portfolios': 0.2060194611650486,
        'total_AR_of_peripheral_portfolios': 0.3700000339805826,
        'total_AR_of_random_portfolios': 0.1208737766990291,
    },
    {
        'day_t': '2016-06-20',
        'total_AR_of_central_portfolios': 0.11975728155339806,
        'total_AR_of_peripheral_portfolios': 1.1907765388349518,
        'total_AR_of_random_portfolios': 0.21742716990291266,
    },
    {
        'day_t': '2016-07-20',
        'total_AR_of_central_portfolios': 0.19623191304347826,
        'total_AR_of_peripheral_portfolios': 1.133864966183575,
        'total_AR_of_random_portfolios': 0.9439132946859903,
    },
    {
        'day_t': '2016-08-19',
        'total_AR_of_central_portfolios': 0.25642512560386477,
        'total_AR_of_peripheral_portfolios': 0.07000000483091788,
        'total_AR_of_random_portfolios': 0.1362318599033816,
    },
    {
        'day_t': '2016-09-18',
        'total_AR_of_central_portfolios': 0.08347825603864728,
        'total_AR_of_peripheral_portfolios': 0.12091786473429947,
        'total_AR_of_random_portfolios': 0.32768114492753614,
    },
    {
        'day_t': '2016-10-18',
        'total_AR_of_central_portfolios': 0.06966179710144932,
        'total_AR_of_peripheral_portfolios': 0.04869568599033821,
        'total_AR_of_random_portfolios': 0.14676329468599034,
    },
    {
        'day_t': '2016-11-17',
        'total_AR_of_central_portfolios': 0.1458737766990291,
        'total_AR_of_peripheral_portfolios': 0.12344660679611649,
        'total_AR_of_random_portfolios': 0.06747571359223284,
    },
    {
        'day_t': '2016-12-17',
        'total_AR_of_central_portfolios': 0.042390209756097585,
        'total_AR_of_peripheral_portfolios': 0.45756099024390257,
        'total_AR_of_random_portfolios': 0.6440485219512181,
    },
    {
        'day_t': '2017-01-16',
        'total_AR_of_central_portfolios': 0.0460095961538462,
        'total_AR_of_peripheral_portfolios': 1.0491347115384617,
        'total_AR_of_random_portfolios': 0.7094231057692307,
    },
    {
        'day_t': '2017-02-15',
        'total_AR_of_central_portfolios': -0.1543269423076923,
        'total_AR_of_peripheral_portfolios': 1.1206732307692309,
        'total_AR_of_random_portfolios': 0.21519233653846154,
    },
    {
        'day_t': '2017-03-17',
        'total_AR_of_central_portfolios': -0.04475729126213593,
        'total_AR_of_peripheral_portfolios': 0.1259708932038835,
        'total_AR_of_random_portfolios': 0.2972815873786407,
    },
    {
        'day_t': '2017-04-16',
        'total_AR_of_central_portfolios': -0.0628019033816425,
        'total_AR_of_peripheral_portfolios': 0.061884019323671415,
        'total_AR_of_random_portfolios': -0.12743962801932374,
    },
    {
        'day_t': '2017-05-16',
        'total_AR_of_central_portfolios': 0.25660190776699016,
        'total_AR_of_peripheral_portfolios': 0.03131071844660198,
        'total_AR_of_random_portfolios': 0.024174742718446603,
    },
]
c = [
    {
        'day_t': '2014-06-01',
        'total_AR_of_central_portfolios': 0.40896844444444436,
        'total_AR_of_peripheral_portfolios': 0.21666676190476197,
        'total_AR_of_random_portfolios': 0.3875395238095234,
    },
    {
        'day_t': '2014-07-01',
        'total_AR_of_central_portfolios': 0.47481177419354853,
        'total_AR_of_peripheral_portfolios': 0.12398083870967712,
        'total_AR_of_random_portfolios': -0.02252685483870963,
    },
    {
        'day_t': '2014-07-31',
        'total_AR_of_central_portfolios': -0.1650000483870966,
        'total_AR_of_peripheral_portfolios': -0.00451604838709678,
        'total_AR_of_random_portfolios': -0.11661304838709687,
    },
    {
        'day_t': '2014-08-30',
        'total_AR_of_central_portfolios': -1.396666603174603,
        'total_AR_of_peripheral_portfolios': -0.2601586825396824,
        'total_AR_of_random_portfolios': 0.06134928571428599,
    },
    {
        'day_t': '2014-09-29',
        'total_AR_of_central_portfolios': -0.3188708387096773,
        'total_AR_of_peripheral_portfolios': 0.519838741935484,
        'total_AR_of_random_portfolios': 0.03749995161290308,
    },
    {
        'day_t': '2014-10-29',
        'total_AR_of_central_portfolios': -0.6682516451612907,
        'total_AR_of_peripheral_portfolios': 0.17096793548387101,
        'total_AR_of_random_portfolios': 0.0655467258064515,
    },
    {
        'day_t': '2014-11-28',
        'total_AR_of_central_portfolios': -0.2017908524590165,
        'total_AR_of_peripheral_portfolios': 1.1984426721311483,
        'total_AR_of_random_portfolios': 0.4055739180327872,
    },
    {
        'day_t': '2014-12-28',
        'total_AR_of_central_portfolios': -0.16658761904761893,
        'total_AR_of_peripheral_portfolios': 0.35349225396825434,
        'total_AR_of_random_portfolios': 0.10061436507936508,
    },
    {
        'day_t': '2015-01-27',
        'total_AR_of_central_portfolios': 0.5811906031746037,
        'total_AR_of_peripheral_portfolios': 2.316984238095238,
        'total_AR_of_random_portfolios': 0.27749198412698384,
    },
    {
        'day_t': '2015-02-26',
        'total_AR_of_central_portfolios': -0.14968253968253914,
        'total_AR_of_peripheral_portfolios': 0.9278570634920632,
        'total_AR_of_random_portfolios': 0.055793539682539695,
    },
    {
        'day_t': '2015-03-28',
        'total_AR_of_central_portfolios': 1.0864281111111116,
        'total_AR_of_peripheral_portfolios': 0.02015857142857142,
        'total_AR_of_random_portfolios': -0.30222236507936456,
    },
    {
        'day_t': '2015-04-27',
        'total_AR_of_central_portfolios': -1.086190666666667,
        'total_AR_of_peripheral_portfolios': 1.2601586349206353,
        'total_AR_of_random_portfolios': -0.9276412857142857,
    },
    {
        'day_t': '2015-05-27',
        'total_AR_of_central_portfolios': -0.3122225079365075,
        'total_AR_of_peripheral_portfolios': -0.7509622222222225,
        'total_AR_of_random_portfolios': -0.4204764761904759,
    },
    {
        'day_t': '2015-06-26',
        'total_AR_of_central_portfolios': -1.4138710161290324,
        'total_AR_of_peripheral_portfolios': -0.47338700000000017,
        'total_AR_of_random_portfolios': -0.7708550967741934,
    },
    {
        'day_t': '2015-07-26',
        'total_AR_of_central_portfolios': 0.6112902741935479,
        'total_AR_of_peripheral_portfolios': 0.3222579999999971,
        'total_AR_of_random_portfolios': 0.09128422580645146,
    },
    {
        'day_t': '2015-08-25',
        'total_AR_of_central_portfolios': 0.28460326984126993,
        'total_AR_of_peripheral_portfolios': 0.3588889365079366,
        'total_AR_of_random_portfolios': 0.665556190476193,
    },
    {
        'day_t': '2015-09-24',
        'total_AR_of_central_portfolios': 0.24390609374999986,
        'total_AR_of_peripheral_portfolios': 0.07859381250000053,
        'total_AR_of_random_portfolios': -0.012318921875000263,
    },
    {
        'day_t': '2015-10-24',
        'total_AR_of_central_portfolios': -0.8379032258064512,
        'total_AR_of_peripheral_portfolios': -1.4769354354838713,
        'total_AR_of_random_portfolios': -1.1991934193548386,
    },
    {
        'day_t': '2015-11-23',
        'total_AR_of_central_portfolios': -0.9804918032786885,
        'total_AR_of_peripheral_portfolios': -0.5516394098360659,
        'total_AR_of_random_portfolios': -0.3259016393442622,
    },
    {
        'day_t': '2015-12-23',
        'total_AR_of_central_portfolios': -0.07363444262295095,
        'total_AR_of_peripheral_portfolios': -1.0608194918032794,
        'total_AR_of_random_portfolios': -0.1775410655737712,
    },
    {
        'day_t': '2016-01-22',
        'total_AR_of_central_portfolios': 1.0760317777777773,
        'total_AR_of_peripheral_portfolios': 1.1404761587301588,
        'total_AR_of_random_portfolios': 1.1857893809523805,
    },
    {
        'day_t': '2016-02-21',
        'total_AR_of_central_portfolios': 0.7173437656250005,
        'total_AR_of_peripheral_portfolios': 0.5657809375000009,
        'total_AR_of_random_portfolios': 0.6878124531250001,
    },
    {
        'day_t': '2016-03-22',
        'total_AR_of_central_portfolios': -0.11349177777777786,
        'total_AR_of_peripheral_portfolios': 0.3930157619047618,
        'total_AR_of_random_portfolios': 0.2648428412698415,
    },
    {
        'day_t': '2016-04-21',
        'total_AR_of_central_portfolios': 0.07793647619047599,
        'total_AR_of_peripheral_portfolios': 0.16460239682539785,
        'total_AR_of_random_portfolios': 0.42444447619047615,
    },
    {
        'day_t': '2016-05-21',
        'total_AR_of_central_portfolios': 0.14354845161290314,
        'total_AR_of_peripheral_portfolios': 1.067742338709678,
        'total_AR_of_random_portfolios': 0.46241914516128996,
    },
    {
        'day_t': '2016-06-20',
        'total_AR_of_central_portfolios': 0.3264518064516127,
        'total_AR_of_peripheral_portfolios': 0.6624193870967741,
        'total_AR_of_random_portfolios': 0.06580656451612894,
    },
    {
        'day_t': '2016-07-20',
        'total_AR_of_central_portfolios': 0.25370954838709664,
        'total_AR_of_peripheral_portfolios': 1.0540327903225792,
        'total_AR_of_random_portfolios': 0.35193540322580646,
    },
    {
        'day_t': '2016-08-19',
        'total_AR_of_central_portfolios': 0.5484127460317468,
        'total_AR_of_peripheral_portfolios': 0.2504762063492064,
        'total_AR_of_random_portfolios': 1.4084121428571423,
    },
    {
        'day_t': '2016-09-18',
        'total_AR_of_central_portfolios': 0.95062484375,
        'total_AR_of_peripheral_portfolios': 0.5843750468750025,
        'total_AR_of_random_portfolios': 0.37953137500000006,
    },
    {
        'day_t': '2016-10-18',
        'total_AR_of_central_portfolios': 0.7435487741935487,
        'total_AR_of_peripheral_portfolios': -0.10903232258064452,
        'total_AR_of_random_portfolios': 0.23306477419354862,
    },
    {
        'day_t': '2016-11-17',
        'total_AR_of_central_portfolios': 1.0816127096774184,
        'total_AR_of_peripheral_portfolios': 0.08612896774193585,
        'total_AR_of_random_portfolios': 0.500161370967742,
    },
    {
        'day_t': '2016-12-17',
        'total_AR_of_central_portfolios': 0.38770485245901604,
        'total_AR_of_peripheral_portfolios': 0.13180340983606598,
        'total_AR_of_random_portfolios': -0.05918018032786859,
    },
    {
        'day_t': '2017-01-16',
        'total_AR_of_central_portfolios': -0.02301604761904763,
        'total_AR_of_peripheral_portfolios': 0.49444450793650807,
        'total_AR_of_random_portfolios': 0.5695238412698412,
    },
    {
        'day_t': '2017-02-15',
        'total_AR_of_central_portfolios': -0.43253968253968283,
        'total_AR_of_peripheral_portfolios': 0.0950794444444446,
        'total_AR_of_random_portfolios': -0.6312698571428572,
    },
    {
        'day_t': '2017-03-17',
        'total_AR_of_central_portfolios': -0.3114286349206345,
        'total_AR_of_peripheral_portfolios': 1.0338095238095244,
        'total_AR_of_random_portfolios': -0.0650792539682537,
    },
    {
        'day_t': '2017-04-16',
        'total_AR_of_central_portfolios': -0.11317460317460362,
        'total_AR_of_peripheral_portfolios': 0.13428576190476163,
        'total_AR_of_random_portfolios': -0.22793657142857127,
    },
    {
        'day_t': '2017-05-16',
        'total_AR_of_central_portfolios': -0.20096772580645159,
        'total_AR_of_peripheral_portfolios': 0.21935467741935452,
        'total_AR_of_random_portfolios': -0.3438708225806455,
    },
]
dateArray = []
# rf_of_MC_in_selection_horizon_array_d = []
# rf_of_MC_in_selection_horizon_array_c = []
# rf_of_MC_in_selection_horizon_array_dd = []
# rf_of_MC_in_selection_horizon_array_dis = []
rf_of_MC_in_selection_horizon_array_corr = []
bai2 = []
bai3 = []
# a=sorted(a10Degree, key=lambda student: student['day_t'])
# b=sorted(a10C, key=lambda student: student['day_t'])
# c=sorted(a10DDegree, key=lambda student: student['day_t'])
# d= sorted(a10Distance, key=lambda student: student['day_t'])
a = sorted(a10Correlation, key=lambda student: student['day_t'])
b = sorted(b, key=lambda student: student['day_t'])
c = sorted(c, key=lambda student: student['day_t'])
for o in a:
    string_day = o['day_t']
    dtime = datetime.date(int(string_day[:4]), int(
        string_day[5:7]), int(string_day[8:10]))
    dateArray.append(dtime)
for o in a:
    string_day = o['total_AR_of_central_portfolios']
    rf_of_MC_in_selection_horizon_array_corr.append(string_day)
for o in b:
    string_day = o['total_AR_of_central_portfolios']
    bai2.append(string_day)
for o in c:
    string_day = o['total_AR_of_central_portfolios']
    bai3.append(string_day)
# for o in d:
#     string_day = o['total_AR_of_central_portfolios']
#     rf_of_MC_in_selection_horizon_array_dis.append(string_day)
# for o in e:
#     string_day = o['total_AR_of_central_portfolios']
#     rf_of_MC_in_selection_horizon_array_corr.append(string_day)
# sum = 0
# for o in a:
#     sum += o[''total_AR_of_peripheral_portfolios'']

# print(sum)
plt.plot_date(dateArray, rf_of_MC_in_selection_horizon_array_corr, 'k-')
plt.xlabel("TSX")
plt.plot_date(dateArray, bai2, 'y-')
plt.plot_date(dateArray, bai3, 'r-')
# plt.plot_date(dateArray,
#               rf_of_MC_in_selection_horizon_array_dd, 'b-',)
# plt.plot_date(dateArray, rf_of_MC_in_selection_horizon_array_dis, 'g-',)
plt.legend(['Phương pháp 1', 'Phương pháp 2', 'Phương pháp 3', ])

plt.show()
