
from bs4 import BeautifulSoup
import requests
import os
import time
import sys
# from PyQt4.QtGui import QApplication
# from PyQt4.QtCore import QUrl
# from PyQt4.QtWebKit import QWebPage

path = "/intraQuarter"

# class Client(QWebPage):
#     def __init__(self,url):
#         self.app = QApplication(sys.argv)
#         QWebPage.__init__(self)
#         self.loadFinished.connect(self.on_page_load)
#         self.mainFrame().load(QUrl(url))
#         self.app.exec_()

#     def on_page_load(self):
#         self.app.quit()


def Check_Yahoo():
	statspath = path + "/_KeyStats"
	stock_list = [x[0] for x in os.walk(statspath)]

	for e in stock_list[1:]:
		try:
			e = e.replace("/Users/Pancho/Desktop/BI/ML/Scikit-Stock/intraQuarter/_KeyStats/","")
			link = "https://finance.yahoo.com/quote/"+str(e)+"/key-statistics"
			# client_response = Client(link)
			# resp = client_response.mainFrame().toHtml()
			resp = requests.get(link).text

			save = path+"/_Forward/"+str(e)+".html"
			store = open(save, "w+")
			store.write(resp.encode("utf-8"))
			print str(e)

		except Exception as e:
			print str(e)

Check_Yahoo()