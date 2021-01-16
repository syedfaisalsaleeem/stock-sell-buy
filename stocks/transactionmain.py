import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

from stocks.setting_alpaca import Setting
from stocks.account_data import AccountData
import requests
import json
## if input value which is transferred from flutter application becomes greater than equity then the user can not do transaction
## we check the input value and current equity value if(the inputvalue becomes greater than equity): then order can not be placed 
class Transaction():
	def __init__(self,userid):
		# submit_order(symbol, qty, side, type, time_in_force, limit_price=None, stop_price=None, client_order_id=None, order_class=None, take_profit=None, stop_loss=None, trail_price=None, trail_percent=None)
		self.userid=userid
		self.BASE_URL="https://paper-api.alpaca.markets"

	def check_equity(self):
		x = AccountData(userid="1234userid")
		y=x.get_account()
		return y['cash']
		# print(y['equity'])
	def check_value_symbol(self,symbol):
		temp_api=Setting()
		api=temp_api.requesttradeapi()
		t1=api.get_last_trade(symbol)
		return t1._raw['price']

	def check_buy(self,qty,symbol):
		ch_equity=self.check_equity()
		current_price=self.check_value_symbol(symbol=symbol)
		if(float(current_price*qty)>float(ch_equity)):
			return False
		else:
			return True


	def create_order_withoutmargin(self,symbol,qty,side,type,time_in_force,limit_price=None, stop_price=None, client_order_id=None, order_class=None, take_profit=None, stop_loss=None, trail_price=None, trail_percent=None):
		ch_buy=self.check_buy(qty,symbol)
		# print(ch_buy)
		# return ch_buy
		if(ch_buy):
			temp_header=Setting()
			self.Headers=temp_header.headers()
			self.ORDERS_URL="{}/v1/orders".format(self.BASE_URL)
			data={
			"symbol":symbol,
			"qty":qty,
			"side":side,
			"type":type,
			"time_in_force":time_in_force,
			"limit_price":limit_price,
			"stop_price":stop_price, 
			"client_order_id":client_order_id,
			"order_class":order_class, 
			"take_profit":take_profit, 
			"stop_loss":stop_loss, 
			"trail_price":trail_price, 
			"trail_percent":trail_percent
			}
			try:
				r=requests.post(self.ORDERS_URL,json=data,headers=self.Headers)
				return json.loads(r.content)
			except:
				return "invalid parameters"
		else:
			return "Current equity is less than the order placed"

	def create_order_withmargin(self,symbol,qty,side,type,time_in_force,limit_price=None, stop_price=None, client_order_id=None, order_class=None, take_profit=None, stop_loss=None, trail_price=None, trail_percent=None):
		temp_header=Setting()
		self.Headers=temp_header.headers()
		self.ORDERS_URL="{}/v2/orders".format(self.BASE_URL)
		data={
		"symbol":symbol,
		"qty":qty,
		"side":side,
		"type":type,
		"time_in_force":time_in_force,
		"limit_price":limit_price,
		"stop_price":stop_price, 
		"client_order_id":client_order_id,
		"order_class":order_class, 
		"take_profit":take_profit, 
		"stop_loss":stop_loss, 
		"trail_price":trail_price, 
		"trail_percent":trail_percent
		}
		r=requests.post(self.ORDERS_URL,json=data,headers=self.Headers)
		return json.loads(r.content)

# x=Transaction(userid="1234userid")
# y=x.create_order_withoutmargin("AAPL",1,"buy","market","gtc")
# print(y)