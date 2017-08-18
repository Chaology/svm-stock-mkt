from __future__ import division

import numpy as np 
from sklearn import svm, preprocessing
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import pandas as pd
from collections import Counter
from matplotlib import style
import statistics
style.use('ggplot')

premium_baseline = 0.06

features = ['DE Ratio',
			'Trailing P/E',
			'Price/Sales',
			'Price/Book',
			'Profit Margin',
			'Operating Margin',
			'Return on Assets',
			'Return on Equity',
			'Revenue Per Share',
			'Market Cap',
			'Enterprise Value',
			'Forward P/E',
			'PEG Ratio',
			'Enterprise Value/Revenue',
			'Enterprise Value/EBITDA',
			'Revenue',
			'Gross Profit',
			'EBITDA',
			'Net Income Avl to Common ',
			'Diluted EPS',
			'Earnings Growth',
			'Revenue Growth',
			'Total Cash',
			'Total Cash Per Share',
			'Total Debt',
			'Current Ratio',
			'Book Value Per Share',
			'Cash Flow',
			'Beta',
			'Held by Insiders',
			'Held by Institutions',
			'Shares Short (as of',
			'Short Ratio',
			'Short % of Float',
			'Shares Short (prior ']

def Premium(stock, sp500):
	difference = stock - sp500

	if difference > premium_baseline:
		return 1
	else:
		return 0

def Build_Data_Set():

	data_df = pd.read_csv('key_stats_acc_perf_WITH_NA.csv')
	data_df = data_df.fillna(0)
	data_df = data_df.reindex(np.random.permutation(data_df.index))
	data_df['premium'] = list(map(Premium, data_df['stock_p_change'], data_df['sp500_p_change']))

	X = data_df[features].values
	sc_X = StandardScaler()
	X = sc_X.fit_transform(X)
	# y = data_df['Status'].replace('underperform',0).replace('outperform',1).values
	y = data_df['premium'].values

	return X, y, data_df, sc_X

# def Randomizing():
# 	df = pd.DataFrame({'D1':range(5),"D2":range(5)})
# 	print df
# 	df2 = df.reindex(np.random.permutation(df.index))
# 	print df2


def Analysis():

	X, y, data_df, sc_X = Build_Data_Set()

	test_size = 1500
	invest_amount = 10000
	total_invests = 0
	if_market = 0
	if_strat = 0

	X_train = X[:-test_size]
	X_test = X[-test_size:]
	y_train = y[:-test_size]
	y_test = y[-test_size:]
	# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)

	clf = svm.SVC(kernel = "linear", C = 1.0)
	clf.fit(X_train, y_train)

	y_pred = clf.predict(X_test)

	accuracy = np.mean(y_pred == y_test)
	print accuracy

	cm = confusion_matrix(y_test, y_pred)
	print cm

	for i in range(y_pred.shape[0]):
		if y_pred[i] == 1:
			invest_return = invest_amount * (1 + data_df.loc[data_df.index[-(i+1)],'stock_p_change'])
			market_return = invest_amount * (1 + data_df.loc[data_df.index[-(i+1)],'sp500_p_change'])
			total_invests += 1
			if_strat += invest_return
			if_market += market_return

	print "Total Trades:", total_invests
	print "Total Return with ML strategy trading", '$'+str(if_strat)
	print "Total Return with sp500 basic market", '$'+str(if_market) 

	premium = round(((if_strat - if_market)/ if_market) * 100.0,2)

	do_nothing = total_invests * invest_amount
	avg_strat = round(((if_strat - do_nothing)/do_nothing) * 100.0,2)
	avg_market = round(((if_market - do_nothing)/do_nothing) * 100.0,2)

	print "Compared to sp500 basic market, we earn", str(premium)+"% more."
	print "Average ML strategy trading return:", str(avg_strat) +"%."
	print "Average sp500 investment return:", str(avg_market) + "%."

	sample_data_df = pd.read_csv('forward_sample_WITH_NA.csv')
	sample_data_df = sample_data_df.replace({'N/A</span>': np.nan}, regex=True)
	sample_data_df = sample_data_df.fillna(0)

	X_sample = sample_data_df[features].values
	X_sample = sc_X.transform(X_sample)

	invest_list = []

	for i in range(len(X_sample)):
		pred = clf.predict([X_sample[i]])[0]
		if pred == 1:
			invest_list.append(sample_data_df['Ticker'][i])

	print len(invest_list), 'out of', len(X_sample)

	return invest_list


final_list = []

loops = 8

for x in range(loops):
	stock_list = Analysis()
	for i in stock_list:
		final_list.append(i)
	print (15*"_")

x = Counter(final_list)
print x

print (15*"_")
for each in x:
	if x[each] > loops - (loops/3.0):
		print each


	# w = clf.coef_[0]
	# a = -w[0] / w[1]

	# xx = np.linspace(min(X[:,0]), max(X[:,0]))
	# yy = a * xx - clf.intercept_[0] / w[1]

	# h0 = plt.plot(xx, yy, 'k-', label = "non weighted")

	# plt.scatter(X[:,0], X[:,1], c = y)
	# plt.ylabel('Trailing P/E')
	# plt.xlabel('DE Ratio')
	# plt.legend()
	# plt.show()


# High recall (989/989+40) but low accuracy (989/(989+748))
# 0.57127312296
# [[ 61 748]
#  [ 40 989]]


# 2012 companies from yahoo went out business in 2013 from quandl lower the sp500value, overestimate difference.
