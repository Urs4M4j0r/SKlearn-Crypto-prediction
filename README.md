## What is this?
This project is something I created trying to learn/experiment with machine learning (ML) using scikit-learn

## What does it do?
There are three main files included as part of this repository, output.csv, gatedata.py, and SHIB_ML_Gate.io.py.

output.csv - The file which is output by gatedata.py containing various values for Bitcoin (BTC), Ethereum (ETH), and Shib (SHIB). These data are used by SHIB-ML-Gate.io.py for ML model training.

gatedata.py - This Python script gathers data using the Gate.io API and writes it to output.csv every 30 seconds. This script was kept seperate from SHIB-ML-Gate.io.py as I found it beneficial to
leave it running on a raspberry pi (or similar) to collect a large amount of data over several days/weeks. For a complete list of what data is collected see [Data](https://github.com/ehoop10/SKlearn-Crypto-prediction/blob/main/README.md#data)

SHIB-ML-Gate.io.py - This is the main code for the project, it takes in a csv file of a format like output.csv and trains 4 machine learning models using seperate algorithms. Live price data is then
pulled using the Gate.io API and prediction are made for 30 seconds in the future. Once 30 seconds have passed from the time of prediction the actual price at that time is compared to the prediction
and the error for each model is printed as a percentage along with the average error of all 4 models and the percent change in price over the 30 seconds time period. For additional information about
the models used see [Models](https://github.com/ehoop10/SKlearn-Crypto-prediction/blob/main/README.md#models-details-taken-from-scikit-learnorg)


## Data
For each of the three cryptocurrencies used the following data is collected

|Data | Currency pair| Time (given as UNIX epoch)| Base volume| Change percentage| High 24h| Highest bid| Low 24h| Lowest ask| Quote volume| last|
|-----|--------------|---------------------------|------------|------------------|---------|------------|--------|-----------|-------------|-----|
|Details| The pair of currency used(ex BTC-USD)|  The UNIX time of when the data was gotten| The amount traded in the past 24 hours given in the base currency (eg BTC)| The live percent change in the currency| The 24 high price| The current highest bid on the currency| The 24 hour low price| The current lowest ask price| The base volume equivalent for the other part of the pair (eg USD)| The last actual price the currency was traded at|


## Models (details taken from scikit-learn.org)
|Model | Full name| Details| Link to documentation|
|------|----------|--------|----------------------|
|SGD | Stochastic Gradient Descent| Linear model fitted by minimizing a regularized empirical loss with SGD| [SGDRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.SGDRegressor.html)|
|GBR | Gradient Boosting Regressor| Gradient Boosting for regression | [GradientBoostingRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.GradientBoostingRegressor.html)|
|LR | Linear Regression| Ordinary least squares Linear Regression | [LinearRegression](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.LinearRegression.html)|
|RF | Random Forest Regressor | A random forest regressor | [RandomForestRegressor](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html)|
