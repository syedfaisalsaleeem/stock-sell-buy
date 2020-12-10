import requests,json
from setting_alpaca import Setting
class AccountData():
	def __init__(self,userid):
		self.userid=userid
		self.BASE_URL="https://paper-api.alpaca.markets"

	def get_account(self):
		temp_header=Setting()
		self.Headers=temp_header.headers()
		ACCOUNT_URL="{}/v2/account".format(self.BASE_URL)
		r=requests.get(ACCOUNT_URL,headers=self.Headers)
		return json.loads(r.content)
		print(r.content)

	def get_account_activites(self):
		temp_header=Setting()
		self.Headers=temp_header.headers()
		ACCOUNT_URL="{}/v2/account/activities".format(self.BASE_URL)
		r=requests.get(ACCOUNT_URL,headers=self.Headers)
		return json.loads(r.content)
		print(r.content)
x = AccountData(userid="1234userid")
y=x.get_account()
print(y['equity'])