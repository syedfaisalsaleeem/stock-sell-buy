import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))
# print(SCRIPT_DIR)

import json
from flask import Flask,request,jsonify
# import stock_sell_buy
# import setting_alpaca

# from stocks.account_data import AccountData
# from stocks.orders_data import * 
# from stocks.postions_data import * 
# from stocks.recommended_bid import * 
# from stocks.setting_alpaca import * 
# from stocks.stocks_value_data import * 
# from stocks.transactionmain import * 

app = Flask(__name__)

@app.route('/hello')
def hello(event, context):
    body = {
        "message": "Go Serverless v1.0! Your function executed successfully!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

# x = AccountData(userid="1234userid")
# # y=x.get_account()
# # x.get_account_activites()
# # print(y['equity'])
# @app.route("/users/<string:user_id>")
# def get_user(user_id):
#     resp = client.get_item(
#         TableName=USERS_TABLE,
#         Key={
#             'userId': { 'S': user_id }
#         }
#     )
#     item = resp.get('Item')
#     if not item:
#         return jsonify({'error': 'User does not exist'}), 404

#     return jsonify({
#         'userId': item.get('userId').get('S'),
#         'name': item.get('name').get('S')
#     })
# from stocks import orders_data
# print(orders_data)

        # response = {
        #         "statusCode": 200,
        #         "body": json.dumps(event["pathParameters"]["userid"])

        #     }
        # return response
@app.route('/stocks/orders')
def listorders(event, context):
    # import stocks
    def returnlimit(item):
        for key,values in item.items():
            if(key=="limit"):
                limit = int(item['limit'])
                return limit

        return None
    try:
        from stocks.orders_data import Orders_data
        limit = returnlimit(event['query'])
        x=Orders_data(event['query']['userid'])
        y=x.get_orders(limit=limit)
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response

@app.route('/stocks/buysellorders')
def buysellorders(event, context):
    # import stocks
    def returnlimit(item):
        for key,values in item.items():
            if(key=="limit"):
                limit = int(item['limit'])
                return limit

        return None



    try:
        from stocks.orders_data import Orders_data

        limit = returnlimit(event['query'])
        x = Orders_data(event['query']['userid'])
        y = x.bought_sell_orders(event['query']['side'],limit)
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response

@app.route('/stocks/orders/')
def listspecificorder(event, context):
    # import stocks
    try:
        from stocks.orders_data import Orders_data
        x=Orders_data(event['userid'])
        y=x.specific_get_order(event["pathParameters"]["orderid"])
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": "error in getting specific order"

            }
        return response

@app.route('/stocks/cancelorders',methods=["POST"])
def cancelallorder(event, context):
    # import stocks
    try:
        from stocks.orders_data import Orders_data
        x=Orders_data(user_id=event['body']['userid'])
        y=x.cancel_all_order()
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response

@app.route('/stocks/cancelorders/',methods=["POST"])
def cancelspecificorder(event, context):
    # import stocks
    try:
        from stocks.orders_data import Orders_data
        x=Orders_data(event['body']['userid'])
        y=x.cancel_single_order(event["path"]["orderid"])
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response


@app.route('/stocks/positions')
def listpositions(event, context):
    # import stocks
    try:
        from stocks.postions_data import Positions_data
        x=Positions_data(event['userid'])
        y=x.get_positions()
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": "error in getting positions"

            }
        return response

@app.route('/stocks/positions/')
def listspecificposition(event, context):
    # import stocks
    try:
        from stocks.postions_data import Positions_data
        x=Positions_data(event['query']['userid'])
        y=x.specific_get_position(event["path"]["ticker"])
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response

@app.route('/stocks/bid/')
def showrecommendedbid(event, context):
    # import stocks
    try:
        from stocks.recommended_bid import Bid
        # x = Bid(userid="1234userid")
# y=x.bid_info(ticker="AAPL")
# print(y)
        x=Bid(event['query']['userid'])
        y=x.bid_info(event["path"]["ticker"])
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response

@app.route('/stocks/createorder',methods=["POST"])
def createorder(event, context):
    # import stocks
    try:
        from stocks.transactionmain import Transaction
        x=Transaction(event['body']['userid'])
        if(event['body']['margin']==False):
            y=x.create_order_withoutmargin(     
            symbol=event['body']["symbol"],
            qty=event['body']["qty"],
            side=event['body']["side"],
            type=event['body']["type"],
            time_in_force=event['body']["time_in_force"],
            limit_price=event['body']["limit_price"],
            stop_price=event['body']["stop_price"], 
            client_order_id=event['body']["client_order_id"],
            order_class=event['body']["order_class"], 
            take_profit=event['body']["take_profit"], 
            stop_loss=event['body']["stop_loss"], 
            trail_price=event['body']["trail_price"], 
            trail_percent=event['body']["trail_percent"]
            )
            response = {
                    "statusCode": 200,
                    "body": y

                }
            return response
        else:
            y=x.create_order_withmargin(     
            symbol=event['body']["symbol"],
            qty=event['body']["qty"],
            side=event['body']["side"],
            type=event['body']["type"],
            time_in_force=event['body']["time_in_force"],
            limit_price=event['body']["limit_price"],
            stop_price=event['body']["stop_price"], 
            client_order_id=event['body']["client_order_id"],
            order_class=event['body']["order_class"], 
            take_profit=event['body']["take_profit"], 
            stop_loss=event['body']["stop_loss"], 
            trail_price=event['body']["trail_price"], 
            trail_percent=event['body']["trail_percent"]
            )
            response = {
                    "statusCode": 200,
                    "body": y

                }
            return response

    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response

@app.route('/stocks/accountdetails')
def showaccountdetails(event, context):
    # import stocks
    try:
        from stocks.account_data import AccountData
        x=AccountData(event['userid'])
        y=x.get_account()
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": "error in fetching details of account"

            }
        return response

@app.route('/stocks/accountactivites')
def showaccountactivites(event, context):
    # import stocks
    try:
        from stocks.account_data import AccountData
        x=AccountData(event['userid'])
        y=x.get_account_activites()
        response = {
                "statusCode": 200,
                "body": y

            }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": "error in fetching details of account"

            }
        return response


@app.route('/get-tickers-polygon')
def getTickersPolygon(event=None, context=None):
    
    try:
        from tickers import Tickers
        tickers = Tickers()
        result = tickers.getTickersFromPolygon()
        response = {
            "statusCode": 200,
            "body": result
        }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(e)

            }
        return response


@app.route('/get-tickers')
def getTickers(event=None, context=None):
    try:
        from tickers import Tickers
        lastTicker = event['query']['lastticker']
        limit = event['query']['limit']
        tickers = Tickers()
        result = tickers.getTickers(lastTicker,limit)
        response = {
            "statusCode": 200,
            "body": result
        }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(e)

            }
        return response

@app.route('/get-ticker')
def getTicker(event=None, context=None):
    try:
        from tickers import Tickers
        findTicker = event['query']['ticker']
        tickers = Tickers()
        result = tickers.getTicker(findTicker)
        response = {
            "statusCode": 200,
            "body": result
        }
        return response
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(e)

            }
        return response

@app.route('/get-ticker-details')
def getTickersDetails(event=None, context=None):
    try:
        from tickers import Tickers
        findTicker = event['query']['ticker']
        tickers = Tickers()
        result = tickers.getTickersDetails(findTicker)
        response = {
            "statusCode": 200,
            "body": result
        }
        return response
    
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(e)

            }
        return response

@app.route('/stocks/get-alpaca-asset-details')
def getalpacaassetDetails(event,context):
    try:
        from stocks.alpaca_asset_details import AlpacaAssetDetails
        tickername = event["path"]["ticker"]
        x = AlpacaAssetDetails(tickername)
        y = x.list_details()
        response = {
            "statusCode": 200,
            "body": y
        }
        return response
    
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response



# x = FinhubFile()
# # y = x._storeFinhubData("AAPL")
# y=x._getFinhubDynamoData("AAPL",1,10)
# print(y)

@app.route('/finhub/get-fillings')
def getfinhubfilings(event,context):
    try:
        from stocks.finhubfiles import FinhubFile
        tickername = event["path"]["ticker"]
        x = FinhubFile()
        # y = x._storeFinhubData("AAPL")
        y=x._getFinhubDynamoData(tickername,int(event["query"]["offset"]),int(event["query"]["limit"]))
        # x = AlpacaAssetDetails(tickername)
        # y = x.list_details()
        response = {
            "statusCode": 200,
            "body": y
        }
        return response
    
    except Exception as e:
        response = {
                "statusCode": 404,
                "body": json.dumps(str(e))

            }
        return response