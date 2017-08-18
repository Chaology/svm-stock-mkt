from __future__ import division
import pandas as pd
import os
import re

path = ""

def Forward(gather=["Total Debt/Equity",
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
                        'Net Income Avi to Common',
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
                        'Shares Short',
                        'Short Ratio',
                        'Short % of Float',
                        'Shares Short (prior ']):

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
    
    stock_list = os.listdir('intraQuarter/_Forward/')

    for each_stock in stock_list:

        ticker = each_stock.split('.html')[0]

        full_stock_path = path + 'intraQuarter/_Forward/' + each_stock

        source = open(full_stock_path, "r").read()

        try:
            print ticker

            feature_value_list = []

            for feature in gather:

                try:
                    regex = re.escape(feature) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A</span>)%?</td>'
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


            if feature_value_list.count('N/A</span>') > 0:
                pass

            else:

                df = df.append({'Date':'N/A',
                                'Unix':'N/A',
                                'Ticker':ticker,
                                'Price':'N/A',
                                'stock_p_change':'N/A',
                                'SP500':'N/A',
                                'sp500_p_change':'N/A',
                                'Difference':'N/A',
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
                                'Status':'N/A'},
                                ignore_index=True)
                print ticker, 'finished'

        except Exception as e:
            print str(e), ticker, file

    df.to_csv('forward_sample_NO_NA.csv')
    print 'File Saved'

Forward()