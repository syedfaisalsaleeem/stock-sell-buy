import os
import requests
import json
import boto3
from boto3.dynamodb.conditions import Key, Attr

class Tickers():

    #This is test function
    def tickersTest(self):
        test = 'This is test function tickers class'
        return test
    
    # This function get tickers from polygon and save to amazon DB
    def getTickersFromPolygon(self):
        from dotenv import load_dotenv
        load_dotenv()
        import os
        polygonapikey = os.getenv("polygonapikey")

        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('tickers')
        apiKey = polygonapikey
        sort = 'ticker'
        perPage = '50'
        page = 1
        response = requests.get("https://api.polygon.io/v2/reference/tickers?sort={}&perpage={}&page={}&apiKey={}".format(sort,perPage,page,apiKey))
        response = json.loads(response._content)
        responseTickers = response['tickers']
        #for index,values in enumerate(y["tickers"]):
        for values in responseTickers:
            table.put_item(Item={"id": "ticker", "ticker": values['ticker'],"details": values })
        
        return True
    
    #Get tickeres from database base
    #Param:
    #      

    def getTickers(self,lastticker=None,limit=None):
        lastKey = None

        offsetLimit = 10
        
        if(limit):
            offsetLimit = limit

        if(lastticker):
            lastKey = {
                "id": "ticker",
                "ticker": lastticker
            }
        
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('tickers')
        if(lastKey):
            response = table.query(KeyConditionExpression=Key('id').eq('ticker'), Limit=offsetLimit,ExclusiveStartKey=lastKey)
        else:
            response = table.query(KeyConditionExpression=Key('id').eq('ticker'), Limit=offsetLimit)

        return response

    def getTicker(self,ticker):
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('tickers')
        response = table.query(KeyConditionExpression=Key('id').eq('ticker') & Key('ticker').eq(ticker))
        return response["Items"]

    def getTickersDetails(self, ticker):
        # ticker = 'AAPL'
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.Table('ticker_details')
         
        response = table.query(KeyConditionExpression=Key('ticker_details').eq('ticker_details') & Key('ticker').eq(ticker))
        if(response["Items"]):
            return json.loads(response["Items"][0]["details"])
            
        else:
            #save get from polygon
            from dotenv import load_dotenv
            load_dotenv()
            import os
            polygonapikey = os.getenv("polygonapikey")
            apiKey = polygonapikey
            response = requests.get("https://api.polygon.io/v1/meta/symbols/{}/company?apiKey={}".format(ticker,apiKey))
            response = json.loads(response._content)
            table.put_item(Item={"ticker_details": "ticker_details", "ticker": ticker,"details": json.dumps(response)})
            return response

# x = Tickers()
# y = x.getTickersDetails(ticker="TSLA")

# print(y)