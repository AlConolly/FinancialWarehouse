import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score

class sklearn_test:
    def __init__(self,dw_interface):
        cursor = dw_interface.connection.cursor()
        # select date and price of gold for analysis
        df = pd.DataFrame(cursor.execute("SELECT date_column, price FROM daily_transactions JOIN date_record ON daily_transactions.date_id = date_record.id WHERE COMMODITY_ID=2").fetchall(), columns=["date", "price"])
        # convert date to ordinal values so the are treated as quantitative values rather than categorical
        df['date']=df['date'].map(dt.datetime.toordinal)
        print(df)

        # Split the data into input features and target variable
        transactionX = df["date"]
        transactionY = df['price']

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