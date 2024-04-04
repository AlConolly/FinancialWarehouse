import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor
from sklearn.svm import SVR
from sklearn.preprocessing import normalize

class sklearn_test:
    def __init__(self,dw_interface):
        cursor = dw_interface.connection.cursor()
        # select date and price of gold for analysis
        self.df = pd.DataFrame(cursor.execute("SELECT date_column, price FROM daily_transactions JOIN date_record ON daily_transactions.date_id = date_record.id WHERE COMMODITY_ID=2").fetchall(), columns=["date", "price"])
        # convert date to ordinal values so the are treated as quantitative values rather than categorical
        self.df['date']=self.df['date'].map(dt.datetime.toordinal)
    def LinearRegression(self):

        # Split the data into input features and target variable
        transactionX = self.df["date"]
        transactionY = self.df['price']

        # Split the data into training and testing sets
        transactionX_train, transactionX_test, transactionY_train, transactionY_test = train_test_split(transactionX, transactionY, test_size=0.2, random_state=0)
        
        #convert to 2d dataframe. This may or may not be necessary for other machine learning models
        transactionX_train = transactionX_train.to_frame()
        transactionX_test = transactionX_test.to_frame()
        # Create linear regression object
        regr = linear_model.LinearRegression()

        # Train the model using the training sets
        regr.fit(transactionX_train, transactionY_train)

        # Make predictions using the testing set
        transaction_y_pred = regr.predict(transactionX_test)

        # The coefficients
        print("Linear Regression:")
        print("Coefficients: \n", regr.coef_)
        # The mean squared error
        print("Mean squared error: %.2f" % mean_squared_error(transactionY_test, transaction_y_pred))
        # The coefficient of determination: 1 is perfect prediction
        print("Coefficient of determination: %.2f" % r2_score(transactionY_test, transaction_y_pred))

        # Plot outputs
        plt.scatter(transactionX_test, transactionY_test, color="black")
        plt.plot(transactionX_test, transaction_y_pred, color="blue", linewidth=3)

        #removes ticks from the plot
        plt.xticks(())
        plt.yticks(())

        plt.show()

    def Random_Forest(self):
        transactionX = self.df["date"]
        transactionY = self.df['price']
        # Split the data into training and testing sets
        transactionX_train, transactionX_test, transactionY_train, transactionY_test = train_test_split(transactionX, transactionY, test_size=0.2, random_state=0)
        # Convert to 2d dataframe. This may or may not be necessary for other machine learning models
        transactionX_train = transactionX_train.to_frame()
        transactionX_test = transactionX_test.to_frame()
        # Create random forest regression object
        regr = RandomForestRegressor(max_depth=100, random_state=0)
        # Train the model using the training sets
        regr.fit(transactionX_train, transactionY_train)
        # Make predictions using the testing set
        transaction_y_pred = regr.predict(transactionX_test)
        # The mean squared error
        print("Random Forest:")
        print("Mean squared error: %.2f" % mean_squared_error(transactionY_test, transaction_y_pred))
        # The coefficient of determination: 1 is perfect prediction
        print("Coefficient of determination: %.2f" % r2_score(transactionY_test, transaction_y_pred))
        # Plot outputs
        plt.scatter(transactionX_test, transactionY_test, color="black")
        plt.plot(transactionX_test, transaction_y_pred, color="blue", linewidth=3)
        # Removes ticks from the plot
        plt.xticks(())
        plt.yticks(())
        plt.show()
    def MLP(self):
        # Split the data into input features and target variable
        transactionX = self.df["date"]
        transactionY = self.df['price']

        # Split the data into training and testing sets
        transactionX_train, transactionX_test, transactionY_train, transactionY_test = train_test_split(transactionX, transactionY, test_size=0.2, random_state=0)
        #convert to 2d dataframe. This may or may not be necessary for other machine learning models
        transactionX_train = transactionX_train.to_frame()
        transactionX_test = transactionX_test.to_frame()

        # Create MLP regression object
        mlp = MLPRegressor(activation="relu")

        # Train the model using the training sets
        mlp.fit(transactionX_train, transactionY_train)

        # Make predictions using the testing set
        transaction_y_pred = mlp.predict(transactionX_test)

        print("MLP:")
        print("Mean squared error: %.2f" % mean_squared_error(transactionY_test, transaction_y_pred))
        # MLP score
        print("Coefficient of Determination: \n", mlp.score(transactionX_test, transactionY_test))

        # Plot outputs
        plt.scatter(transactionX_test, transactionY_test, color="black")
        plt.plot(transactionX_test, transaction_y_pred, color="blue", linewidth=3)

        #removes ticks from the plot
        plt.xticks(())
        plt.yticks(())

        plt.show()

    def SVR(self):
        transactionX = self.df["date"]
        transactionY = self.df['price']
        # Split the data into training and testing sets
        transactionX_train, transactionX_test, transactionY_train, transactionY_test = train_test_split(transactionX, transactionY, test_size=0.2, random_state=0)
        # Convert to 2d dataframe. This may or may not be necessary for other machine learning models
        transactionX_train = transactionX_train.to_frame()
        transactionX_test = transactionX_test.to_frame()
        # Create support vector regression object
        svr = SVR()
        # Train the model using the training sets
        svr.fit(transactionX_train, transactionY_train)
        # Make predictions using the testing set
        transaction_y_pred = svr.predict(transactionX_test)
        print("SVR:")
        # The mean squared error
        print("Mean squared error: %.2f" % mean_squared_error(transactionY_test, transaction_y_pred))
        # The coefficient of determination: 1 is perfect prediction
        print("Coefficient of determination: %.2f" % r2_score(transactionY_test, transaction_y_pred))
        # Plot outputs
        plt.scatter(transactionX_test, transactionY_test, color="black")
        plt.plot(transactionX_test, transaction_y_pred, color="blue", linewidth=3)
        # Removes ticks from the plot
        plt.xticks(())
        plt.yticks(())
        plt.show()
