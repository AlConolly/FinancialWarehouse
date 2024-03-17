import csv
import os
from scripts.ETL.utils.index_fund import Index_Fund_ETL_Util
from datetime import datetime

class SP_500_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      self.index_fund_etl_util = Index_Fund_ETL_Util(dw_interface)
      root_dir = os.path.dirname(os.path.dirname(
          os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(
          root_dir, 'resources', 'data', 'index_fund', 'sp_500_index.csv')
      self.insert_index_fund_prices(csv_file_path)

  def insert_index_fund_prices(self, csv_file_path):
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        index_funds = []
        transaction_infos = []
        index_fund_id = self.index_fund_etl_util.get_max_index_fund_id()
        for i, row in enumerate(csv_reader):
            index_fund_id += 1
            index_fund = {'name': 'S&P_500', 'management_company': 'S&P Dow Jones Indices', 'net_asset_value': row[1], 'yield': 0, 'type': 'index_fund'}
            index_funds.append(index_fund)
            transaction_info = {
                'date': datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d'),
                'price': row[1],
                'symbol': 'SPX',
                'open_price': row[2],
                'high_price': row[3],
                'low_price': row[4],
                'index_fund_id': index_fund_id
            }
            transaction_infos.append(transaction_info)
            if (i + 1) % 1000 == 0:  # Every 1000 rows, do a batch insert
                self.index_fund_etl_util.insert_index_funds(index_funds)
                self.daily_transactions.insert_daily_transactions(
                    self, transaction_infos)
                index_funds = []
                transaction_infos = []
        # Insert remaining rows that didn't make up a full batch of 1000
        if index_funds:
            self.index_fund_etl_util.insert_index_funds(index_funds)
            self.daily_transactions.insert_daily_transactions(
                self, transaction_infos)

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)
