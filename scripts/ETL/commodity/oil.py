import csv
import os
from scripts.ETL.utils.commodity import Commodity_ETL_Util

class Commodity_Oil_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      self.commodity_etl_util = Commodity_ETL_Util(dw_interface)
      root_dir = os.path.dirname(os.path.dirname(
          os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(
          root_dir, 'resources', 'data', 'commodity', 'crude_oil.csv')
      self.insert_oil_prices(csv_file_path)

  def insert_oil_prices(self, csv_file_path):
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        commodities = []
        transaction_infos = []
        commodity_id = self.commodity_etl_util.get_max_commodity_id()
        for i, row in enumerate(csv_reader):
            commodity_id += 1
            commodity = {'name': 'Crude Oil',
                         'unit_of_measure': row[1], 'type': "fossil_fuel"}
            commodities.append(commodity)
            transaction_info = {
                'date': row[0],
                'price': (float(row[1])),
                'symbol': 'CRUDE_OIL',
                'open_price': (float(row[2])),
                'high_price': (float(row[3])),
                'low_price': (float(row[4])),
                'volume': (float(row[5].replace('K', '').replace('M', '')) * 1000) if 'K' in row[5] else int(float(row[5].replace('M', '')) * 1000000) if 'M' in row[5] else 0,
                'commodity_id': commodity_id
            }
            transaction_infos.append(transaction_info)
            if (i + 1) % 1000 == 0:  # Every 1000 rows, do a batch insert
                # self.commodity_etl_util.insert_commodities(commodities)
                self.daily_transactions.insert_daily_transactions(transaction_infos)
                commodities = []
                transaction_infos = []
        # Insert remaining rows that didn't make up a full batch of 1000
        # if commodities:
        #     self.commodity_etl_util.insert_commodities(commodities)
        #     self.daily_transactions.insert_daily_transactions(
        #         self, transaction_infos)

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)
