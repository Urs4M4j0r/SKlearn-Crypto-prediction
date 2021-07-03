import time
import csv
import gate_api
from gate_api.exceptions import ApiException, GateApiException

#Set the API configuration for pulling data
configuration = gate_api.Configuration(host = "https://api.gateio.ws/api/v4")
api_client = gate_api.ApiClient(configuration)
api_instance = gate_api.SpotApi(api_client)

#Get data for the currency pair
def getTicker(currencyPair):
    try:
        api_response = api_instance.list_tickers(currency_pair=currencyPair)
        api_response = api_instance.list_tickers(currency_pair=currencyPair)
        return api_response
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_tickers: %s\n" % e)

#Get values
def getTickerValue(tick, value):
    switcher = {
        "base_volume": str(tick[0]).split(": ")[1],
        "change_percentage": str(tick[1]).split(": ")[1],
        "currency_pair": str(tick[2]).split(": ")[1],
        "high_24h": str(tick[7]).split(": ")[1],
        "highest_bid": str(tick[8]).split(": ")[1],
        "last": str(tick[9]).split(": ")[1],
        "low_24h": str(tick[10]).split(": ")[1],
        "lowest_ask": str(tick[11]).split(": ")[1],
        "quote_volume": str(tick[12]).split(": ")[1],
        }
    return switcher.get(value, "Invalid ticker info requested.")

#Write the collected data to output.csv
def writedata(datalist):
    with open('output.csv', 'a', newline='', encoding='utf-8') as fp:
        wr = csv.writer(fp)
        wr.writerow(datalist)

#Collect all the data and add it to array dataList, then send dataList to writedata() to create/add to the output file  
def getdata():
    dataList = []

    tickerInfo = str(getTicker("shib_usdt")[0]).replace("'","").replace("{", "").replace("}", "").split(",")
    tickerInfo2 = str(getTicker("btc_usdt")[0]).replace("'","").replace("{", "").replace("}", "").split(",")
    tickerInfo3 = str(getTicker("eth_usdt")[0]).replace("'","").replace("{", "").replace("}", "").split(",")
    dataList.append('BTC-USD')
    dataList.append(str(round(time.time(),0)))
    dataList.append(getTickerValue(tickerInfo2, "base_volume"))
    dataList.append(getTickerValue(tickerInfo2, "change_percentage"))
    dataList.append(getTickerValue(tickerInfo2, "high_24h"))
    dataList.append(getTickerValue(tickerInfo2, "highest_bid"))
    dataList.append(getTickerValue(tickerInfo2, "low_24h"))
    dataList.append(getTickerValue(tickerInfo2, "lowest_ask"))
    dataList.append(getTickerValue(tickerInfo2, "quote_volume"))
    dataList.append(getTickerValue(tickerInfo2, "last"))
    
    dataList.append('ETH-USD')
    dataList.append(str(round(time.time(),0)))
    dataList.append(getTickerValue(tickerInfo3, "base_volume"))
    dataList.append(getTickerValue(tickerInfo3, "change_percentage"))
    dataList.append(getTickerValue(tickerInfo3, "high_24h"))
    dataList.append(getTickerValue(tickerInfo3, "highest_bid"))
    dataList.append(getTickerValue(tickerInfo3, "low_24h"))
    dataList.append(getTickerValue(tickerInfo3, "lowest_ask"))
    dataList.append(getTickerValue(tickerInfo3, "quote_volume"))
    dataList.append(getTickerValue(tickerInfo3, "last"))

    dataList.append('SHIB-USD')
    dataList.append(str(round(time.time(),0)))
    dataList.append(getTickerValue(tickerInfo, "base_volume"))
    dataList.append(getTickerValue(tickerInfo, "change_percentage"))
    dataList.append(getTickerValue(tickerInfo, "high_24h"))
    dataList.append(getTickerValue(tickerInfo, "highest_bid"))
    dataList.append(getTickerValue(tickerInfo, "low_24h"))
    dataList.append(getTickerValue(tickerInfo, "lowest_ask"))
    dataList.append(getTickerValue(tickerInfo, "quote_volume"))
    dataList.append(getTickerValue(tickerInfo, "last"))
    
    writedata(dataList)
    print(dataList)

while True:
    getdata()
    #Set this to change the interval you are collecting data at
    time.sleep(30)
