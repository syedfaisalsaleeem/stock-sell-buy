import alpaca_trade_api as tradeapi
class Setting():
    def __init__(self):
        from dotenv import load_dotenv
        load_dotenv()
        import os
        self.key_id = os.getenv("key_id")
        self.secret_key = os.getenv("secret_key")
        # self.requesttradeapi()
    def headers(self):
        return {"APCA-API-KEY-ID":self.key_id,"APCA-API-SECRET-KEY":self.secret_key}
    
    def requesttradeapi(self):
        api = tradeapi.REST(self.key_id,self.secret_key, base_url='https://paper-api.alpaca.markets')
        return api