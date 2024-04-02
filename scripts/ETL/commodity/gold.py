import csv
import os
from scripts.ETL.utils.commodity import Commodity_ETL_Util

class Commodity_Gold_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      self.commodity_etl_util = Commodity_ETL_Util(dw_interface)
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', 'commodity', 'gold.csv')
      self.insert_gold_prices(csv_file_path)

  def insert_gold_prices(self, csv_file_path):
    commodity_id = self.commodity_etl_util.get_commodity_id('Gold')
    if commodity_id is None:
        raise Exception("Commodity ID not found for Gold")
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        transaction_infos = []
        for i, row in enumerate(csv_reader):
            transaction_info = {
                'date': row[0],
                'price': row[4],
                'symbol': 'GOLD',
                'open_price': row[1],
                'high_price': row[2],
                'low_price': row[3],
                'volume': row[5],
                'commodity_id': commodity_id
            }
            transaction_infos.append(transaction_info)
            if (i + 1) % 1000 == 0:  # Every 1000 rows, do a batch insert
                self.daily_transactions.insert_daily_transactions(transaction_infos)
                transaction_infos = []
        # Insert remaining rows that didn't make up a full batch of 1000
        if transaction_infos:
            self.daily_transactions.insert_daily_transactions(transaction_infos)

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)
