import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
import requests,json
from stocks.setting_alpaca import Setting
import boto3
from boto3.dynamodb.conditions import Key, Attr

class Orders_data():
    def __init__(self,userid):
        self.userid=userid
        self.BASE_URL="https://paper-api.alpaca.markets"

    def polygonAssetDetails(self,ticker):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('ticker_details')
         
        response = table.query(KeyConditionExpression=Key('ticker_details').eq('ticker_details') & Key('ticker').eq(ticker))
        if(response["Items"]):
            return json.loads(response["Items"][0]["details"])
            
        else:
            #save get from polygon
            apiKey = "Kl86glry7WIW9NDUUapKFyxli22n3tjt"
            response = requests.get("https://api.polygon.io/v1/meta/symbols/{}/company?apiKey={}".format(ticker,apiKey))
            response = json.loads(response._content)
            table.put_item(Item={"ticker_details": "ticker_details", "ticker": ticker,"details": json.dumps(response)})
            return response
    
    def get_orders(self,limit=None):
        self.ORDERS_URL="{}/v2/orders".format(self.BASE_URL)
        temp_header=Setting()
        self.Headers=temp_header.headers()
        r = requests.get(self.ORDERS_URL,headers=self.Headers)
        pending = json.loads(r.content)
        self.temp_list = []
        # print(pending)
        for values in pending:
            self.temp_dict = {}
            self.temp_dict["symbol"] = values["symbol"]
            polygonDetails = self.polygonAssetDetails(values["symbol"])
            alpacaDetails = self.alpacaAssetDetails(values["symbol"])
            self.temp_dict["symbolimage"] = polygonDetails["logo"]
            self.temp_dict["qty"] = values["qty"]
            self.temp_dict["id"] = values["id"]
            self.temp_dict['filled_avg_price'] = values['filled_avg_price']
            self.temp_dict['side'] = values['side']
            self.temp_dict['name'] = alpacaDetails['assets']['name']
            self.temp_dict['exchange'] = alpacaDetails['assets']['exchange']
            
            # print(alpacaDetails)
            self.temp_list.append(self.temp_dict)
        if(limit!=None):
            return self.temp_list[0:limit]
        else:
            return self.temp_list

    def specific_get_order(self,orderid):
        self.ORDERS_URL="{}/v2/orders/{}".format(self.BASE_URL,orderid)
        temp_header=Setting()
        self.Headers=temp_header.headers()
        r=requests.get(self.ORDERS_URL,headers=self.Headers)
        return json.loads(r.content)

    def alpacaAssetDetails(self,ticker):
        from stocks.alpaca_asset_details import AlpacaAssetDetails
        x = AlpacaAssetDetails(ticker)
        y = x.list_details()
        return y
    def bought_sell_orders(self,query,limit=None):
        self.ORDERS_URL="{}/v2/orders?status=all".format(self.BASE_URL,limit)
        temp_header=Setting()
        self.Headers=temp_header.headers()
        r=requests.get(self.ORDERS_URL,headers=self.Headers)
        bought = json.loads(r.content)
        # print(bought,"bought")
        self.temp_list = []
        
        
        for values in bought:
            if(values['side']==query and values['status']=='filled'):
                self.temp_dict = {}
                polygonDetails = self.polygonAssetDetails(values["symbol"])
                alpacaDetails = self.alpacaAssetDetails(values["symbol"])
                self.temp_dict["symbol"] = values["symbol"]
                self.temp_dict["symbolimage"] = polygonDetails["logo"]
                self.temp_dict["qty"] = values["qty"]
                self.temp_dict['filled_avg_price'] = values['filled_avg_price']
                self.temp_dict['side'] = values['side']
                self.temp_dict['name'] = alpacaDetails['assets']['name']
                self.temp_dict['exchange'] = alpacaDetails['assets']['exchange']
                
                # print(alpacaDetails)
                self.temp_list.append(self.temp_dict)
        if limit==None:
            return self.temp_list
            
        elif (limit==0):
            return self.temp_list[0]
        
        else:
            return self.temp_list[0:limit]
                # print(values)
        # self.ORDERS_URL="{}/v2/orders?status=all".format(self.BASE_URL)
        # temp_header=Setting()
        # self.Headers=temp_header.headers()
        # r=requests.get(self.ORDERS_URL,headers=self.Headers)
        # return json.loads(r.content)




    # def check_equity(self):
    #   x = AccountData(userid="1234userid")
    #   y=x.get_account()
    #   return y['equity']
    #   # print(y['equity'])
    # def check_value_symbol(self,symbol):
    #   temp_api=Setting()
    #   api=temp_api.requesttradeapi()
    #   t1=api.get_last_trade(symbol)
    #   return t1._raw['price']

    # def check_buy(self,qty,symbol):
    #   ch_equity=self.check_equity()
    #   current_price=self.check_value_symbol(symbol=symbol)
    #   if(float(current_price*qty)>float(ch_equity)):
    #       return False
    #   else:
    #       return True
    # def update_orders_withmargin(self,orderid,symbol,qty,side,type,time_in_force,limit_price=None, stop_price=None, client_order_id=None, order_class=None, take_profit=None, stop_loss=None, trail_price=None, trail_percent=None):
        
    #   ch_buy=self.check_buy(qty,symbol)
    #   try:
    #       temp_api=Setting()
    #       api=temp_api.requesttradeapi()
    #       api.cancel_order(orderid)
    #       return "successfully cancel order"  
    #   except:
    #       return "invalid parameters"

    #   if(ch_buy):
    #       temp_header=Setting()
    #       self.Headers=temp_header.headers()
    #       self.ORDERS_URL="{}/v1/orders".format(self.BASE_URL)
    #       data={
    #       "symbol":symbol,
    #       "qty":qty,
    #       "side":side,
    #       "type":type,
    #       "time_in_force":time_in_force,
    #       "limit_price":limit_price,
    #       "stop_price":stop_price, 
    #       "client_order_id":client_order_id,
    #       "order_class":order_class, 
    #       "take_profit":take_profit, 
    #       "stop_loss":stop_loss, 
    #       "trail_price":trail_price, 
    #       "trail_percent":trail_percent
    #       }
    #       try:
    #           r=requests.post(self.ORDERS_URL,json=data,headers=self.Headers)
    #           return json.loads(r.content)
    #       except:
    #           return "invalid parameters"
    #   else:
    #       return "Current equity is less than the order placed"

    # def update_orders_withoutmargin(self,orderid,symbol,qty,side,type,time_in_force,limit_price=None, stop_price=None, client_order_id=None, order_class=None, take_profit=None, stop_loss=None, trail_price=None, trail_percent=None):
    #   # /v2/orders/{order_id}
    #   self.ORDERS_URL="{}/v2/orders/{}".format(self.BASE_URL,orderid)
    #   temp_header=Setting()
    #   self.Headers=temp_header.headers()
    #   data={
    #   "qty":qty,
    #   # "time_in_force":time_in_force,
    #   # "limit_price":limit_price,
    #   # "stop_price":stop_price, 
    #   # "client_order_id":client_order_id,
    #   # "trail":trail, 
    #   }
    #   # try:
    #   r=requests.post(self.ORDERS_URL,json=data,headers=self.Headers)
    #   return r.content
    #   # return json.loads(r.content)
    #   # except:
    #   #   return "invalid parameters"

    # def get_all_cancel_order(self,query,limit=None):
    #     self.ORDERS_URL="{}/v2/orders?status=all".format(self.BASE_URL,limit)
    #     temp_header=Setting()
    #     self.Headers=temp_header.headers()
    #     r=requests.get(self.ORDERS_URL,headers=self.Headers)
    #     bought = json.loads(r.content)
    #     # print(bought,"bought")
    #     self.temp_list = []
        
        
    #     for values in bought:
    #         if(values['side']==query and values['status']=='filled'):
    #             self.temp_dict = {}
    #             polygonDetails = self.polygonAssetDetails(values["symbol"])
    #             alpacaDetails = self.alpacaAssetDetails(values["symbol"])
    #             self.temp_dict["symbol"] = values["symbol"]
    #             self.temp_dict["symbolimage"] = polygonDetails["logo"]
    #             self.temp_dict["qty"] = values["qty"]
    #             self.temp_dict['filled_avg_price'] = values['filled_avg_price']
    #             self.temp_dict['side'] = values['side']
    #             self.temp_dict['name'] = alpacaDetails['assets']['name']
    #             self.temp_dict['exchange'] = alpacaDetails['assets']['exchange']
                
    #             # print(alpacaDetails)
    #             self.temp_list.append(self.temp_dict)
    #     if limit==None:
    #         return self.temp_list
            
    #     elif (limit==0):
    #         return self.temp_list[0]
        
    #     else:
    #         return self.temp_list[0:limit]

    def cancel_single_order(self,orderid):
        temp_api = Setting()
        api = temp_api.requesttradeapi()
        api.cancel_order(orderid)
        x = self.get_orders()
        return "successfully cancel order"
    
    def cancel_all_order(self):
        temp_api=Setting()
        api=temp_api.requesttradeapi()
        api.cancel_all_orders()
        x=self.get_orders()
        return x


# x=Orders_data(userid="1234userid")
# y1=x.get_orders(None)
# print(y1)
# y1=x.bought_sell_orders("buy",limit=1)
# print(y1)
# # # print(y)
# # # y=x.update_orders(orderid="3585882b-ff35-475c-8d6f-d19fb41a0c92",qty="2")
# # y=x.cancel_all_order()
# y=x.cancel_single_order("f7f9a324-058f-479c-a639-904d6a2f2dd8")
# print(y)