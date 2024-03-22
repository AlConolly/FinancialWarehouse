import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime as dt

from sklearn import linear_model
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import normalize

class sklearn_test_MLP:
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

        # Create MLP regression object
        mlp = MLPRegressor(hidden_layer_sizes=(100, 100), activation='relu', solver='adam', random_state=0)

        # Train the model using the training sets
        mlp.fit(transactionX_train, transactionY_train)

        # Make predictions using the testing set
        transaction_y_pred = mlp.predict(transactionX_test)

        # MLP score
        print("Coefficient of Determination: \n", mlp.score(transactionX_test, transactionY_test))

        # Plot outputs
        plt.scatter(transactionX_test, transactionY_test, color="black")
        plt.plot(transactionX_test, transaction_y_pred, color="blue", linewidth=3)

        #removes ticks from the plot
        plt.xticks(())
        plt.yticks(())

        plt.show()