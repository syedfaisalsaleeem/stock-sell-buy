import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

import requests,json
from stocks.setting_alpaca import Setting
class AlpacaAssetDetails():
	def __init__(self,tickername):
		self.tickername = tickername
		self.BASE_URL = "https://paper-api.alpaca.markets"
		self.temp_dict = {}
	def list_details(self):
		temp_header = Setting()
		self.Headers = temp_header.headers()
		ASSET_URL = "{}/v2/assets/{}".format(self.BASE_URL,self.tickername)
		r = requests.get(ASSET_URL,headers=self.Headers)
		data1 = json.loads(r.content)
		# return json.loads(r.content)
		Clock_URL = "{}/v2/clock".format(self.BASE_URL)
		r1 = requests.get(Clock_URL,headers=self.Headers)
		data2 = json.loads(r1.content)
		self.temp_dict["assets"] = data1 
		self.temp_dict["clock"] = data2 
		# print(r1.content)
		return self.temp_dict

# x = AlpacaAssetDetails("AAPL")
# y = x.list_details()
# print(y)