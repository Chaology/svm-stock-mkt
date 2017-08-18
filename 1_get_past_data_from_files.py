from __future__ import division
import pandas as pd
import os
import time
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib import style
style.use('dark_background')
import re

path = "/intraQuarter"

def Key_Stats(gather=["Total Debt/Equity",
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
                        'Shares Short (prior ']):

    statspath = path + '/_KeyStats'

    stock_list = [x[0] for x in os.walk(statspath)]

    df = pd.DataFrame(columns = ['Date',
                                'Unix',
                                'Ticker',
                                'Price',
                                'stock_p_change',
                                'SP500',
                                'sp500_p_change',
                                'Difference',
                                ##########
                                'DE Ratio',
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
                                'Shares Short (prior ',
                                #############
                                'Status'])
    
    sp500_df = pd.read_csv('S&P500.csv')
    stock_df = pd.read_csv('stock_prices.csv')
    
    ticker_list = []
    

    for each_dir in stock_list[1:]: #remove the first home dir 

        each_stock = os.listdir(each_dir)

        ticker = each_dir.rsplit('/',1)[1]
        ticker_list.append(ticker)
        
        # starting_stock_value = False
        # starting_sp500_value = False
        
        if len(each_stock) > 0:

            for file in each_stock:

                each_file_path = each_dir + '/' + file
                source = open(each_file_path, 'r').read()

                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())

                try:
                    ##########
                    feature_value_list = []

                    for feature in gather:

                        try:
                            regex = re.escape(feature) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                            value = re.search(regex, source)
                            value = value.group(1)

                            if "B" in value:
                                value = float(value.replace('B','')) * 1000000000
                            elif "M" in value:
                                value = float(value.replace('M','')) * 1000000

                            feature_value_list.append(value)
                        
                        except Exception as e:
                            value = "N/A"
                            feature_value_list.append(value)

                    ###########
                    sp500_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                    row = sp500_df[sp500_df['Date'] == sp500_date]

                    if len(row) > 0:
                        sp500_value = float(row['Adj Close'])
                    else:
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df['Date'] == sp500_date)]
                        if len(row) > 0:
                            sp500_value = float(row['Adj Close'])
                        else:
                            sp500_date = datetime.fromtimestamp(unix_time - 345600).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df['Date'] == sp500_date)]
                            if len(row) > 0:
                                sp500_value = float(row['Adj Close'])
                            else:
                                sp500_date = datetime.fromtimestamp(unix_time - 432000).strftime('%Y-%m-%d')
                                row = sp500_df[(sp500_df['Date'] == sp500_date)]
                                sp500_value = float(row['Adj Close'])

                    ### 1 year from now for sp500
                    one_year_late = int(unix_time + 31536000) 

                    sp500_ly = datetime.fromtimestamp(one_year_late).strftime('%Y-%m-%d')
                    row = sp500_df[(sp500_df['Date'] == sp500_ly)]
                    if len(row) > 0:
                        sp500_ly_value = float(row['Adj Close'])
                    else:
                        sp500_ly = datetime.fromtimestamp(one_year_late - 259200).strftime('%Y-%m-%d')
                        row = sp500_df[(sp500_df['Date'] == sp500_ly)]
                        if len(row) > 0:
                            sp500_ly_value = float(row['Adj Close'])
                        else:
                            sp500_ly = datetime.fromtimestamp(one_year_late - 345600).strftime('%Y-%m-%d')
                            row = sp500_df[(sp500_df['Date'] == sp500_ly)]
                            if len(row) > 0:
                                sp500_ly_value = float(row['Adj Close'])
                            else:
                                sp500_ly = datetime.fromtimestamp(unix_time - 432000).strftime('%Y-%m-%d')
                                row = sp500_df[(sp500_df['Date'] == sp500_ly)]
                                sp500_ly_value = float(row['Adj Close'])

                    # try:
                    #     stock_price = source.split('</small><big><b>')[1].split('</b></big>')[0]
                    #     stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                    #     stock_price = float(stock_price.group(1))
                    # except Exception as e:
                    #     stock_price = source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0]
                    #     stock_price = re.search(r'(\d{1,8}\.\d{1,8})', stock_price)
                    #     stock_price = float(stock_price.group(1))


                    # if not starting_stock_value:
                    #     starting_stock_value = stock_price
                    # if not starting_sp500_value:
                    #     starting_sp500_value = sp500_value

                    stock_date = datetime.fromtimestamp(unix_time).strftime('%Y-%m-%d')
                    row = stock_df[stock_df['Date'] == stock_date][ticker.upper()]

                    if len(row) > 0:
                        stock_price = float(row)
                    else:
                        stock_date = datetime.fromtimestamp(unix_time - 259200).strftime('%Y-%m-%d')
                        row = stock_df[(stock_df['Date'] == stock_date)][ticker.upper()]
                        if len(row) > 0:
                            stock_price = float(row)
                        else:
                            stock_date = datetime.fromtimestamp(unix_time - 345600).strftime('%Y-%m-%d')
                            row = stock_df[(stock_df['Date'] == stock_date)][ticker.upper()]
                            if len(row) > 0:
                                stock_price = float(row)
                            else:
                                stock_date = datetime.fromtimestamp(unix_time - 432000).strftime('%Y-%m-%d')
                                row = stock_df[(stock_df['Date'] == stock_date)][ticker.upper()]
                                stock_price = float(row)

                    ### 1 yr from now for stock price                      
                    stock_ly = datetime.fromtimestamp(one_year_late).strftime('%Y-%m-%d')
                    row = stock_df[(stock_df['Date'] == sp500_ly)][ticker.upper()]
                    if len(row) > 0:
                        stock_ly_value = float(row)
                    else:
                        stock_ly = datetime.fromtimestamp(one_year_late - 259200).strftime('%Y-%m-%d')
                        row = stock_df[(sp500_df['Date'] == stock_ly)][ticker.upper()]
                        if len(row) > 0:
                            stock_ly_value = float(row)
                        else:
                            stock_ly = datetime.fromtimestamp(one_year_late - 345600).strftime('%Y-%m-%d')
                            row = stock_df[(sp500_df['Date'] == stock_ly)][ticker.upper()]
                            if len(row) > 0:
                                stock_ly_value = float(row)
                            else:
                                stock_ly = datetime.fromtimestamp(unix_time - 432000).strftime('%Y-%m-%d')
                                row = stock_df[(sp500_df['Date'] == stock_ly)][ticker.upper()]
                                stock_ly_value = float(row)
                    #######
                    stock_p_change = round(((stock_ly_value - stock_price) / stock_price),2)
                    sp500_p_change = round(((sp500_ly_value - sp500_value) / sp500_value),2)
                    difference = stock_p_change - sp500_p_change

                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"

                    if feature_value_list.count('N/A') > 15:
                        pass

                    else:
                        df = df.append({'Date':date_stamp,
                                        'Unix':unix_time,
                                        'Ticker':ticker,

                                        'Price':stock_price,
                                        'stock_p_change':stock_p_change,
                                        'SP500':sp500_value,
                                        'sp500_p_change':sp500_p_change,
                                        'Difference':difference,
                                        'DE Ratio':feature_value_list[0],
                                        'Trailing P/E':feature_value_list[1],
                                        'Price/Sales':feature_value_list[2],
                                        'Price/Book':feature_value_list[3],
                                        'Profit Margin':feature_value_list[4],
                                        'Operating Margin':feature_value_list[5],
                                        'Return on Assets':feature_value_list[6],
                                        'Return on Equity':feature_value_list[7],
                                        'Revenue Per Share':feature_value_list[8],
                                        'Market Cap':feature_value_list[9],
                                        'Enterprise Value':feature_value_list[10],
                                        'Forward P/E':feature_value_list[11],
                                        'PEG Ratio':feature_value_list[12],
                                        'Enterprise Value/Revenue':feature_value_list[13],
                                        'Enterprise Value/EBITDA':feature_value_list[14],
                                        'Revenue':feature_value_list[15],
                                        'Gross Profit':feature_value_list[16],
                                        'EBITDA':feature_value_list[17],
                                        'Net Income Avl to Common ':feature_value_list[18],
                                        'Diluted EPS':feature_value_list[19],
                                        'Earnings Growth':feature_value_list[20],
                                        'Revenue Growth':feature_value_list[21],
                                        'Total Cash':feature_value_list[22],
                                        'Total Cash Per Share':feature_value_list[23],
                                        'Total Debt':feature_value_list[24],
                                        'Current Ratio':feature_value_list[25],
                                        'Book Value Per Share':feature_value_list[26],
                                        'Cash Flow':feature_value_list[27],
                                        'Beta':feature_value_list[28],
                                        'Held by Insiders':feature_value_list[29],
                                        'Held by Institutions':feature_value_list[30],
                                        'Shares Short (as of':feature_value_list[31],
                                        'Short Ratio':feature_value_list[32],
                                        'Short % of Float':feature_value_list[33],
                                        'Shares Short (prior ':feature_value_list[34],
                                        'Status':status},
                                        ignore_index=True)
                except Exception as e:
                    print str(e), ticker, file

    # for each_ticker in ticker_list:
    #     try:
    #         plot_df = df[df['Ticker'] == each_ticker]
    #         plot_df = plot_df.set_index(['Date'])

    #         if plot_df['Status'][-1] == "underperform":
    #             color = "r"
    #         else:
    #             color = 'g'
            
    #         plot_df['Difference'].plot(label = each_ticker, color = color)

    #         plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
            
    #     except:
    #         pass
    
    # plt.show()
                                
    # save = gather.replace(' ','').replace(')','').replace('(','').replace('/','') + ('.csv')
    # print (save)
    df.to_csv('key_stats_acc_perf_WITH_NA.csv')
    print 'File Saved'


Key_Stats()