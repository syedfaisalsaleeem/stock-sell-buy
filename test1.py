import alpaca_trade_api as tradeapi
import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('D:/ismailwork/stock-sell-buy')  # adjust as appropriate
print(project_folder)
load_dotenv(os.path.join(project_folder, '.env'))
key_id=os.getenv("key_id")
secret_key=os.getenv("secret_key")
api = tradeapi.REST(key_id, secret_key, base_url='https://paper-api.alpaca.markets') # or use ENV Vars shown below
account = api.get_account()
api.list_positions()
# print(api.list_positions())
def get_market_status():
	print(api.get_clock())
print(api.get_clock())
# get_market_status()
# print(api.get_position("GOOGL"))
# print(api.list_assets())
print(api.get_last_trade("GOOGL"))
print(api.get_last_quote("GOOGL"))
# get_last_quote(symbol)