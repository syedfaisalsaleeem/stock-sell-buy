import requests,json

BASE_URL="https://paper-api.alpaca.markets"
APCA_API_BASE_URL="https://paper-api.alpaca.markets"
APCA_API_KEY_ID="PKY7QEBXMYLD033OPY3X"
APCA_API_SECRET_KEY="ccHUhvMXSdQdZiWVSeofpI7DOdaINJnWPqnNzDkR"
ACCOUNT_URL="{}/v2/account/activities".format(BASE_URL)
ORDERS_URL="{}/v2/orders".format(BASE_URL)
POSITIONS_URL="{}/v2/positions".format(BASE_URL)
# HEADERS={"APCA-API-KEY-ID":"PKT914573IYN611YLDCD","APCA-API-SECRET-KEY":"Kond4n0EMGpeQeyUdA8eqMJ2B7fyd6ckP886RVHA"}
# HEADERS={"APCA-API-KEY-ID":"PKYSKE2YZ9RTAWDQ5KTC","APCA-API-SECRET-KEY":"hwvIECYy8F2yvQASCxYLI5b7FynRqbNXT4lmolAT"}

def get_account():
	r=requests.get("https://paper-api.alpaca.markets/v2/account/activities",headers=HEADERS)
	return json.loads(r.content)
	print(r.content)

response=get_account()
print(response)

def create_order(symbol,qty,side,type,time_in_force):
	data={
	"symbol":symbol,
	"qty":qty,
	"side":side,
	"type":type,
	"time_in_force":time_in_force
	}
	r=requests.post(ORDERS_URL,json=data,headers=HEADERS)
	return json.loads(r.content)

def get_orders():
	r=requests.get(ORDERS_URL,headers=HEADERS)
	return json.loads(r.content)

# response=create_order("AAPL",1,"buy","market","gtc")
# print(response)

# response=get_orders()
# print(response)

def get_postitions():
	r=requests.get(POSITIONS_URL+"/AAPL",headers=HEADERS)
	return json.loads(r.content)

# response=get_postitions()
# print(response)

# def get_account():
# 	/v2/account
#method,
# class function calling

# function caller(method, url, body,parameters){
	
# }