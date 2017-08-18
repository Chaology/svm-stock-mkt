This project is an updated replica based on sentdex's tutorial.

Firstly, I downloaded the scraped historical financial data of SP500 companies from Yahoo finance.

Then I did some feature engineering and data merge. Features are DE Ratio,Trailing P/E, Profit Margin, Revenue Per Share, etc. The label is the binary comparsion of the percentage of stock price change of each company with sp500 stock price change after 1 year.

After the data wrangling process, I applied SVM algorithm to predict the change of stock price of each company after 30 days then validate with the actual data. It turns out that my simple machine learning trading algorithm beat the market "in theory".

Reference: https://pythonprogramming.net/machine-learning-python-sklearn-intro/