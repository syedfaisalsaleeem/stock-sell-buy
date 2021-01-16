import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import requests,json
from stocks.setting_alpaca import Setting


class Positions_data():
	def __init__(self,userid):
		self.userid=userid
		self.BASE_URL="https://paper-api.alpaca.markets"
	
	def get_positions(self):
		self.POSITIONS_URL="{}/v2/positions".format(self.BASE_URL)
		temp_header=Setting()
		self.Headers=temp_header.headers()
		r=requests.get(self.POSITIONS_URL,headers=self.Headers)
		return json.loads(r.content)

	def specific_get_position(self,ticker):
		self.POSITIONS_URL="{}/v2/positions/{}".format(self.BASE_URL,ticker)
		temp_header=Setting()
		self.Headers=temp_header.headers()
		r=requests.get(self.POSITIONS_URL,headers=self.Headers)
		return json.loads(r.content)




# x=Positions_data(userid="1234userid")

# y=x.specific_get_position("AAPL")
# print(y)