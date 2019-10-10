"""Steps for stock prediction only."""

from csv import reader
from sklearn import svm
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np


def predict_stock(dates, close, date_to_predict, company):
    """
    Price prediction.

    Linear vs. Support Vector (RBF) Regression.
    """
    dates = np.reshape(dates, (len(dates), 1))  # converting to matrix of n X 1
    # defining the support vector regression models
    svr_rbf = svm.SVR(kernel='rbf', C=1e3, gamma=0.1)
    lm = LinearRegression()  # defining linear regression model
    lm.fit(dates, close)  # fitting the data points in the models
    svr_rbf.fit(dates, close)
    print("\nThe stock close price for day " + str(date_to_predict) + " is:")
    print("RBF kernel: $", str(svr_rbf.predict(date_to_predict)[0]))
    print("Linear Regression: $", str(lm.predict(date_to_predict)[0]))
    print("Preparing Graph...")
    # plotting the initial datapoints
    plt.scatter(dates, close, color='black', label='Data')
    plt.plot(dates, svr_rbf.predict(dates), color='red',
             label='RBF model')  # plotting the lines made by models
    plt.plot(dates, lm.predict(dates), color='blue', label='Linear Regression')
    plt.scatter(date_to_predict, svr_rbf.predict(date_to_predict),
                color="green", label='RBF One Day Ahead Prediction')
    plt.scatter(date_to_predict, lm.predict(date_to_predict),
                color="purple", label='Linear One Day Ahead Prediction')
    plt.xlabel('Day')
    plt.ylabel('Close Price')
    plt.title(
        'Regression - One Day Ahead Prediction for Stocks, Company label: '
        + company)
    plt.legend()
    plt.show()


def get_data(filename, company):
    """
    Read a specific company's stock data.

    Once reading and cleaning is finished, the stock prediction is done.
    """
    dates = []
    prices = []
    with open(filename, 'r') as csvfile:
        csvFileReader = reader(csvfile)
        print("Company Label:", company)
        next(csvFileReader)	 # skipping column names
        i = 1
        for row in csvFileReader:
            if row[1] == company:
                dates.append(row[0])
                i += 1
                prices.append(float(row[3]))
        # sort prices list by the actual date (clean data)
        prices = [x for (y, x) in sorted(
            zip(sorted(dates,
                       key=lambda d: tuple(map(int, d.split('-')))), prices))]
        dates = range(0, len(dates))  # number of days
        predict_stock(dates, prices, len(dates) + 1, company)
    return
