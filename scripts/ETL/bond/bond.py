import csv
import os
from scripts.ETL.utils.bond import Bond_ETL_Util

class Bond_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      self.bond_etl_util = Bond_ETL_Util(dw_interface)
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', 'bond', 'United States 14-Year Bond Yield Historical Data.csv')
      self.insert_bondPrices(csv_file_path)
  
  def insert_bondPrices(self, csv_file_path):
    bond_id = self.bond_etl_util.get_bond_id('U.S. Treasury Bond')
    if bond_id is None:
        raise Exception("Bond ID not found for Bond")
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        transaction_infos = []
        for i, row in enumerate(csv_reader):
            transaction_info = {
                'date': row[0],
                'price': (float(row[1])),
                'symbol': 'US_TREASURY_BOND',
                'open_price': (float(row[2])),
                'high_price': (float(row[3])),
                'low_price': (float(row[4])),
                'bond_id': bond_id
            }
            transaction_infos.append(transaction_info)
            if (i + 1) % 1000 == 0:  # Every 1000 rows, do a batch insert
                self.daily_transactions.insert_daily_transactions(transaction_infos)
                transaction_infos = []
        if transaction_infos:
            self.daily_transactions.insert_daily_transactions(transaction_infos)

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)