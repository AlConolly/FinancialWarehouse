import os
import matplotlib.pyplot as plt
import pandas as pd

class Visualization:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface
    #   data = get_data(self)
    #   plot_data(data)
    #   data2 = get_data2(self)
    #   plot_data2(data2)
      data3 = get_data3(self)
      plot_data3(data3)

def get_data(self):
    cursor = self.dw_interface.connection.cursor()
    # Get the price of stocks 328, 311, 352 and the S&P 500
    cursor.execute("""
        SELECT DT.stock_id, DT.price, DT.price_sp500, DR.day, DR.month, DR.year
        FROM DAILY_TRANSACTIONS DT
        JOIN DATE_RECORD DR ON DT.date_id = DR.id 
        WHERE DT.stock_id IN (328, 311, 352) AND DR.year <= 2022
        ORDER BY DT.date_id ASC
    """)
    data = cursor.fetchall()
    cursor.close()
    print("Data Fetched")
    return data

def plot_data(data):
    print("Plotting data")
    df = pd.DataFrame(data, columns=['stock_id', 'price', 'price_sp500', 'day', 'month', 'year'])
    
    # Convert day, month, year to datetime
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    df.set_index('date', inplace=True)
    
    # Drop the day, month, year columns
    df.drop(['day', 'month', 'year'], axis=1, inplace=True)
    
    # Create a dictionary mapping stock IDs to names
    stock_names = {328: 'Apple Inc', 311: 'Amazon', 352: 'Best Buy'}
    
    # Plot each stock separately
    fig, ax = plt.subplots()
    for stock_id in df['stock_id'].unique():
        df[df['stock_id'] == stock_id].plot(ax=ax, y='price', label=stock_names[stock_id])
    
    # Labels
    ax.set_ylabel('Price (USD)')
    ax.set_title('Stock Prices')
    ax.set_xlabel('Date')
    plt.show()

    
def get_data2(self):
    cursor = self.dw_interface.connection.cursor()
    # Get the price of 'AAPL', 'MSFT', 'GOOGL', gold, oil and the S&P 500
    cursor.execute("""
        SELECT DT.symbol, DT.price, DT.price_sp500, DT.price_gold, DT.price_oil, DR.day, DR.month, DR.year
        FROM DAILY_TRANSACTIONS DT
        JOIN DATE_RECORD DR ON DT.date_id = DR.id
        WHERE DT.symbol IN ('AAPL', 'MSFT', 'GOOGL') AND DR.year <= 2022
        ORDER BY DT.date_id ASC, DT.symbol ASC
    """)
    data = cursor.fetchall()
    cursor.close()
    print("Data Fetched")
    return data

def get_data3(self):
    cursor = self.dw_interface.connection.cursor()
    # Get the price of commodity with ID 42
    cursor.execute("""
        SELECT c.name, DT.price, DR.day, DR.month, DR.year
        FROM DAILY_TRANSACTIONS DT
        JOIN DATE_RECORD DR ON DT.date_id = DR.id
        JOIN COMMODITY c ON DT.commodity_id = c.id
        WHERE DT.commodity_id IN (53, 57, 42, 1)
        ORDER BY DT.date_id ASC
    """)
    data = cursor.fetchall()
    cursor.close()
    print("Data Fetched")
    return data


def plot_data3(data):
    print("Plotting data")
    df = pd.DataFrame(data, columns=['name', 'price', 'day', 'month', 'year'])
    
    # Create a datetime column from the day, month, and year
    df['date'] = pd.to_datetime(df[['year', 'month', 'day']])
    
    # Plot data
    plt.figure(figsize=(10, 6))
    
    # Loop through each commodity
    for name, group in df.groupby('name'):
        plt.plot(group['date'], group['price'], label=name)
    
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title('Commodity Prices Over Time')
    plt.legend()
    plt.tight_layout()
    plt.show()
   
    
     
      
