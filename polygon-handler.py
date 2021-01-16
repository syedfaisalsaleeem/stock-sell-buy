@app.route('/get-tickers-polygon')
def getTickersPolygon(event=None, context=None):
    tickers = Tickers()
    result = tickers.getTickersFromPolygon()
    response = {
        "statusCode": 200,
        "body": result
    }
    return response


@app.route('/get-tickers')
def getTickers(event=None, context=None):
    lastTicker = request.args.get("lastticker")
    limit = request.args.get("limit")
    tickers = Tickers()
    result = tickers.getTickers(lastTicker,limit)
    response = {
        "statusCode": 200,
        "body": result
    }
    return response

@app.route('/get-ticker')
def getTicker(event=None, context=None):
    findTicker = request.args.get("ticker")
    tickers = Tickers()
    result = tickers.getTicker(findTicker)
    response = {
        "statusCode": 200,
        "body": result
    }
    return response


@app.route('/get-ticker-details')
def getTickersDetails(event=None, context=None):
    findTicker = request.args.get("ticker")
    tickers = Tickers()
    result = tickers.getTickersDetails(findTicker)
    response = {
        "statusCode": 200,
        "body": result
    }
    return response