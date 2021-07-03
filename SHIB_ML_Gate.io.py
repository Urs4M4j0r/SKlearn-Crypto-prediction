from sklearn.model_selection import train_test_split
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import linear_model
from sklearn import preprocessing
import numpy as np
import time
from sklearn.preprocessing import StandardScaler
import gate_api
from gate_api.exceptions import ApiException, GateApiException
from tkinter import Tk
from tkinter.filedialog import askopenfilename

configuration = gate_api.Configuration(
    host = "https://api.gateio.ws/api/v4"
)

api_client = gate_api.ApiClient(configuration)
api_instance = gate_api.SpotApi(api_client)


def getTicker(currencyPair):
    #retrieve data for a specified currency pair
    try:
        api_response = api_instance.list_tickers(currency_pair=currencyPair)
        api_response = api_instance.list_tickers(currency_pair=currencyPair)
        return api_response
    except GateApiException as ex:
        print("Gate api exception, label: %s, message: %s\n" % (ex.label, ex.message))
    except ApiException as e:
        print("Exception when calling SpotApi->list_tickers: %s\n" % e)
        

def getTickerValue(tick, value):
    #retrieve specific values
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


def priceNow():
    #Get the current price for checking against the prediction
    tickerInfo = str(getTicker("shib_usdt")[0]).replace("'","").replace("{", "").replace("}", "").split(",")
    return getTickerValue(tickerInfo, "last")


def dataNow():
    #retrieve current data to make a prediction for future price
    dataList = []
    tickerInfo = str(getTicker("shib_usdt")[0]).replace("'","").replace("{", "").replace("}", "").split(",")
    tickerInfo2 = str(getTicker("btc_usdt")[0]).replace("'","").replace("{", "").replace("}", "").split(",")
    tickerInfo3 = str(getTicker("eth_usdt")[0]).replace("'","").replace("{", "").replace("}", "").split(",")
    dataList.append(getTickerValue(tickerInfo2, "base_volume"))
    dataList.append(getTickerValue(tickerInfo2, "change_percentage"))
    dataList.append(getTickerValue(tickerInfo2, "high_24h"))
    dataList.append(getTickerValue(tickerInfo2, "highest_bid"))
    dataList.append(getTickerValue(tickerInfo2, "low_24h"))
    dataList.append(getTickerValue(tickerInfo2, "lowest_ask"))
    dataList.append(getTickerValue(tickerInfo2, "quote_volume"))
    dataList.append(getTickerValue(tickerInfo2, "last"))
    dataList.append(getTickerValue(tickerInfo3, "base_volume"))
    dataList.append(getTickerValue(tickerInfo3, "change_percentage"))
    dataList.append(getTickerValue(tickerInfo3, "high_24h"))
    dataList.append(getTickerValue(tickerInfo3, "highest_bid"))
    dataList.append(getTickerValue(tickerInfo3, "low_24h"))
    dataList.append(getTickerValue(tickerInfo3, "lowest_ask"))
    dataList.append(getTickerValue(tickerInfo3, "quote_volume"))
    dataList.append(getTickerValue(tickerInfo3, "last"))
    dataList.append(getTickerValue(tickerInfo, "base_volume"))
    dataList.append(getTickerValue(tickerInfo, "change_percentage"))
    dataList.append(getTickerValue(tickerInfo, "high_24h"))
    dataList.append(getTickerValue(tickerInfo, "highest_bid"))
    dataList.append(getTickerValue(tickerInfo, "low_24h"))
    dataList.append(getTickerValue(tickerInfo, "lowest_ask"))
    dataList.append(getTickerValue(tickerInfo, "quote_volume"))
    dataListnp = np.array([dataList])
    return dataListnp


#Train the models and print the time taken for training to complete
#Return the trained model
def sgd(X,Y,Z):
    start_time = time.time()
    clf = SGDRegressor(max_iter=1000000)
    clf.fit(X,Y)
    output = clf.predict(Z)
    print("Took " + str(round(time.time()-start_time,2)) + " seconds to run.")
    print(output)
    return clf
    
def linReg(X,Y,Z):
    start_time = time.time()
    linReg = LinearRegression(n_jobs=-1).fit(X=X,y=Y)
    output = linReg.predict(Z)
    print("Took " + str(round(time.time()-start_time,2)) + " seconds to run.")
    print(output)
    return linReg   

def randomForest(X,Y,Z):
    start_time = time.time()
    clf = RandomForestRegressor()
    clf.fit(X, Y)
    output = clf.predict(Z)
    print("Took " + str(round(time.time()-start_time,2)) + " seconds to run.")
    print(output)
    return clf

def gbr(X,Y,Z):
    start_time = time.time()
    reg = GradientBoostingRegressor(random_state=0)
    reg.fit(X, Y)
    output = reg.predict(Z)
    print("Took " + str(round(time.time()-start_time,2)) + " seconds to run.")
    print(output)
    return reg


#Pass current data and the trained models to return a prediction for the price in the future
def sgdPred(x, sgd):
    return sgd.predict(x)[0]

def gbrPred(x, gbr):
    return gbr.predict(x)[0]

def linRegPred(x,linreg):
    return linreg.predict(x)[0]

def randomForestPred(x, rf):
    return rf.predict(x)[0]


#Take the data and split it into train and test sets as well as scaling the data prior to training
def trainTestSplit(cryptoTrain_X,cryptoTrain_Y):
    loopNum = int(input("Enter the number of prediction loops you would like to run: "))
    cryptoTrain_X, cryptoTest_X, cryptoTrain_Y, y_test = train_test_split(cryptoTrain_X, cryptoTrain_Y, test_size=0.0001)

    #Scale data before training
    scaler = StandardScaler()
    scaler.fit(cryptoTrain_X)
    cryptoTrain_X2 = scaler.transform(cryptoTrain_X)
    cryptoTest_X2 = scaler.transform(cryptoTest_X)

    #Print just a couple test data points to validate correctness
    print('\nShould be: ' + str(y_test) + '\n')
    print('\nLinear Reg scaled')
    lR = linReg(cryptoTrain_X2,cryptoTrain_Y,cryptoTest_X2)
    print('\nRandom Forest scaled')
    rF = randomForest(cryptoTrain_X2,cryptoTrain_Y,cryptoTest_X2)
    print('\nSGD scaled')
    SGD = sgd(cryptoTrain_X2,cryptoTrain_Y,cryptoTest_X2)
    print('\nGradient Boosting Regressor scaled')
    GBR = gbr(cryptoTrain_X2,cryptoTrain_Y,cryptoTest_X2)
       
    #Initialize the variables to zero prior to the loop
    count=LRtotalavg=RFtotalavg=SGDtotalavg=GBRtotalavg=AVGtotalavg=AVGtotalchg=priceN=priceNprev=0
    
    while count < loopNum:
        print('Loop number: ' + str(count))
        dn = dataNow()
        dnsc = scaler.transform(dn)
        LRpred = linRegPred(dnsc,lR)
        RFpred = randomForestPred(dnsc, rF)
        SGDpred = sgdPred(dnsc,SGD)
        GBRpred = gbrPred(dnsc,GBR)
        avgPred = (LRpred + RFpred+ SGDpred + GBRpred) / 4

        #Set this to the number of seconds in the future you are training the model to predict, it allows for the testing/printing of percent errors for comparison 
        time.sleep(30)

        #Only calculate a percent change in price if not the first loop
        if count < 1:
            priceN = priceNow()
            priceNprev = priceN
        else:
            priceNprev = priceN
            priceN = priceNow()

        #Compare the current price against the predictions and print a percentage to assess inaccuracy
        print('\n')
        ac1 = round(abs((float(LRpred)/float(priceN))-1)*100,2)
        print('LR is: ' + str(ac1) + '% off.')
        LRtotalavg = LRtotalavg + ac1

        ac2 = round(abs((float(RFpred)/float(priceN))-1)*100,2)
        print('RF is: ' + str(ac2) + '% off.')
        RFtotalavg = RFtotalavg + ac2

        ac3 = round(abs((float(SGDpred)/float(priceN))-1)*100,2)
        print('SGD is: ' + str(ac3) + '% off.')
        SGDtotalavg = SGDtotalavg + ac3

        ac4 = round(abs((float(GBRpred)/float(priceN))-1)*100,2)
        print('GBR is: ' + str(ac4) + '% off.')
        GBRtotalavg = GBRtotalavg + ac4

        ac5 = round(abs((float(avgPred)/float(priceN))-1)*100,2)
        print('Avg Pred is: ' + str(ac5) + '% off.')
        AVGtotalavg = AVGtotalavg + ac5

        ac7 = round(abs((float(priceNprev)/float(priceN))-1)*100,2)
        print('change in price is: ' + str(ac7) + '%.')
        AVGtotalchg = AVGtotalchg + ac7

        #Every ten loops print an average of the percent errors
        if count % 10 == 0 and count != 0:
            print('\nTotal averages are: ')
            print(str(round((LRtotalavg/count),2)) + '% - Linear Regression')
            print(str(round((RFtotalavg/count),2)) + '% - Random Forrest')
            print(str(round((SGDtotalavg/count),2)) + '% - Stochastic Gradient Descent')
            print(str(round((GBRtotalavg/count),2)) + '% - Gradient Boosting Regressor')
            print(str(round((AVGtotalavg/count),2)) + '% - Average')
            print(str(round((AVGtotalchg/count),2)) + '% - Average price change\n')
        count = count + 1

def getInputFile():
    Tk().withdraw()
    filename = askopenfilename(title = "Select input csv file",filetypes = (("CSV Files","*.csv"),))
    return filename

    
run = 0
while run < 1:
    #Pull in data from the .csv file the user selects from the dialog
    inFile = getInputFile()
    cryptoTrain_X = np.loadtxt(inFile, delimiter=',', usecols=(2,3,4,5,6,7,8,9,12,13,14,15,16,17,18,19,22,23,24,25,26,27,28))
    cryptoTrain_Y = np.loadtxt(inFile, delimiter=',', usecols=(-1))
    trainTestSplit(cryptoTrain_X,cryptoTrain_Y) 
    print('\n')    
    run = run + 1
