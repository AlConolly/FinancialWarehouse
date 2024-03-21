import csv
import os
from scripts.ETL.utils.commodity import Commodity_ETL_Util
from scripts.ETL.utils.daily_transactions import Daily_Transactions_ETL

class Commodity_Silver_ETL():
    def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      self.commodity_etl_util = Commodity_ETL_Util(dw_interface)
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', 'commodity', 'silver.csv')
      self.insert_silver_prices(csv_file_path)

    def insert_silver_prices(self, csv_file_path):
      # Load date_ids
      date_ids = self.daily_transactions.load_date_ids()

      with open(csv_file_path, 'r') as file:
          csv_reader = csv.reader(file)
          next(csv_reader)
          transactions_info = []
          commodity_id = 22
          for row in csv_reader:
              #row format ['1968-02-07', '1.965']
              
              # Get the date_id for the date
              date_id = date_ids.get(row[0])
              if date_id is not None:
                  transactions_info.append({
                      'date': row[0],
                      'commodity_id': commodity_id,
                      'price': row[1]
                  })

      # Prepare data for insert and insert into DAILY_TRANSACTIONS table
      self.daily_transactions.insert_daily_transactions(transactions_info)

      print(f"Inserted silver prices into the DAILY_TRANSACTIONS table")