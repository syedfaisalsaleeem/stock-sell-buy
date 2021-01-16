import requests
import boto3
from boto3.dynamodb.conditions import Key, Attr
import sys
import os

PACKAGE_PARENT = '..'
SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

class FinhubFile():
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        import os
        self.finhubtoken = os.getenv("finhubtoken")
         

    def _storeFinhubData(self,symbol):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('FinhubData')
        r = requests.get('https://finnhub.io/api/v1/stock/filings?symbol={}&token={}'.format(symbol,self.finhubtoken))
        # response = requests.get("https://api.polygon.io/v2/reference/tickers?sort={}&perpage={}&page={}&apiKey={}".format(sort,perPage,page,apiKey))
        data = r.json()
        r1 = requests.get('https://finnhub.io/api/v1/stock/financials-reported?symbol={}&token={}'.format(symbol,self.finhubtoken))
        data1 = r1.json()
        # print(data)
        # print(len(data1["data"]),len(data))
        for no,value in enumerate(data):
            table.put_item(Item={"hk": symbol, "sk": no,"SEC Filings": value ,"sk2":symbol})

        return "data inserted"

        # for value,value1 in zip(data,data1["data"]):
        #     pass
            # print(value,value1)
            # table.put_item(Item={"hk": "finhubsecfilings", "sk": symbol,"SEC Filings": value })
            # table.put_item(Item={"hk": "finhubsecfilings", "sk": symbol,"Financials As Reported":value1 })
            # print(data[0])
            # print(type(value))
        # response = json.loads(response._content)
        # responseTickers = response['tickers']
        #for index,values in enumerate(y["tickers"]):
#         table.update_item(
#     Key={
#         'username': 'janedoe',
#         'last_name': 'Doe'
#     },
#     UpdateExpression='SET age = :val1',
#     ExpressionAttributeValues={
#         ':val1': 26
#     }
# )
        # for values in responseTickers:
        #     table.put_item(Item={"hk": "finhubstockdata", "sk": symbol,"SEC Filings": data,"Financials As Reported":data1 })

    def _getFinhubDynamoData(self,symbol,offset,limit):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('FinhubData')
        response = table.query(KeyConditionExpression=Key('hk').eq(symbol)&Key('sk').gt(offset),Limit=limit)
        return response['Items']
        # print(response["Items"])


# x = FinhubFile()
# # y = x._storeFinhubData("AAPL")
# y=x._getFinhubDynamoData("AAPL",1,10)
# print(y)

        # dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        # table = dynamodb.Table('tickers')
        # apiKey = "Kl86glry7WIW9NDUUapKFyxli22n3tjt"
        # sort = 'ticker'
        # perPage = '50'
        # page = 1
        # response = requests.get("https://api.polygon.io/v2/reference/tickers?sort={}&perpage={}&page={}&apiKey={}".format(sort,perPage,page,apiKey))
        # response = json.loads(response._content)
        # responseTickers = response['tickers']
        # #for index,values in enumerate(y["tickers"]):
        # for values in responseTickers:
        #     table.put_item(Item={"id": "ticker", "ticker": values['ticker'],"details": values })
        
        # return True