import requests,json
from setting_alpaca import Setting
# BASE_URL="https://paper-api.alpaca.markets"
# APCA_API_BASE_URL="https://paper-api.alpaca.markets"
# APCA_API_KEY_ID="PKY7QEBXMYLD033OPY3X"
# APCA_API_SECRET_KEY="ccHUhvMXSdQdZiWVSeofpI7DOdaINJnWPqnNzDkR"
# ACCOUNT_URL="{}/v2/account/activities".format(BASE_URL)
# ORDERS_URL="{}/v2/orders".format(BASE_URL)
# POSITIONS_URL="{}/v2/positions".format(BASE_URL)

class Stocks_value():
	def __init__(self,userid):
		self.userid=userid
		self.BASE_URL="https://paper-api.alpaca.markets"
		# pass

	def get_positions(self):
		temp_header=Setting()
		self.Headers=temp_header.headers()
		self.POSITIONS_URL="{}/v2/positions".format(self.BASE_URL)

		r=requests.get(self.POSITIONS_URL,headers=self.Headers)
		return json.loads(r.content)

	def get_positions_ticker(self,tickername):
		self.tickername=tickername
		temp_header=Setting()
		self.Headers=temp_header.headers()
		self.POSITIONS_URL="{}/v2/positions/{}".format(self.BASE_URL,self.tickername)

		r=requests.get(self.POSITIONS_URL,headers=self.Headers)
		return json.loads(r.content)


x=Stocks_value(userid="1234userid")
y=x.get_positions_ticker(tickername="AAPL")
print(y)