from setting_alpaca import Setting

class Bid():
	def __init__(self,userid):
		self.userid=userid

	def bid_info(self,ticker):
		temp_api=Setting()
		dict1={}
		api=temp_api.requesttradeapi()
		t1=api.get_last_trade(ticker)
		t2=api.get_last_quote("GOOGL")
		dict1['trade']=t1._raw
		dict1['quote']=t2._raw
		return dict1

x = Bid(userid="1234userid")
y=x.bid_info(ticker="AAPL")
print(y)