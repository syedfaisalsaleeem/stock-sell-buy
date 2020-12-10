from key import Key
import alpaca_trade_api as tradeapi
class Setting():
	def __init__(self):
		self.key_id=Key.key_id
		self.secret_key=Key.secret_key
		# self.requesttradeapi()
	def headers(self):
		return {"APCA-API-KEY-ID":self.key_id,"APCA-API-SECRET-KEY":self.secret_key}
	def requesttradeapi(self):
		api = tradeapi.REST(self.key_id,self.secret_key, base_url='https://paper-api.alpaca.markets')
		return api