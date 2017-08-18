import pandas as pd 
import os
from Quandl import Quandl

# quandl.ApiConfig.api_key = 'YcgxzKKRjxeAoQymHsyH'

auth_tok = "YcgxzKKRjxeAoQymHsyH"

path = "/intraQuarter"

def Stock_Prices():

	df = pd.DataFrame()

	statspath = path + "/_KeyStats"
	stock_list = [x[0] for x in os.walk(statspath)]

	for each_dir in stock_list[1:]:

		ticker = each_dir.rsplit('/',1)[1]
		print ticker

		try:

			name = 'WIKI/' + ticker.upper()
			data = Quandl.get(name, trim_start = '2000-01-01', trim_end = '2016-12-30')

			data[ticker.upper()] = data['Adj. Close']
			df = pd.concat([df, data[ticker.upper()]], axis = 1)

		except Exception as e:
			print str(e)

	df.to_csv('stock_prices.csv')

Stock_Prices()