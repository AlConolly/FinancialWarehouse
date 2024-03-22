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
      csv_file_paths = [os.path.join(root_dir, 'resources', 'data', 'index_fund', 'sp_500_index.csv'),
                        os.path.join(root_dir, 'resources', 'data', 'index_fund', 'sp_500_index_2.csv')]
      self.insert_index_fund_prices(csv_file_paths)

  def insert_index_fund_prices(self, csv_file_paths):
<<<<<<< HEAD
    index_fund_id = self.index_fund_etl_util.get_index_fund_id(self, 'S&P_500')
    if index_fund_id is None:
        raise Exception("Index Fund ID not found for S&P_500")
=======
>>>>>>> daily_transactions_util
    for csv_file_path in csv_file_paths:
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            next(csv_reader)
<<<<<<< HEAD
            transaction_infos = []
            for i, row in enumerate(csv_reader):
=======
            index_funds = []
            transaction_infos = []
            index_fund_id = self.index_fund_etl_util.get_max_index_fund_id()
            for i, row in enumerate(csv_reader):
                index_fund_id += 1
                index_fund = {'name': 'S&P_500', 'management_company': 'S&P Dow Jones Indices',
                              'price': float(row[1].replace(',', '')), 'yield': 0, 'type': 'index_fund'}
                index_funds.append(index_fund)
>>>>>>> daily_transactions_util
                date = datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d') if 'sp_500_index.csv' in csv_file_path else row[0]
                transaction_info = {
                    'date': date,
                    'price': float(row[1].replace(',', '')),
                    'symbol': 'SPX',
                    'open_price': float(row[2].replace(',', '')),
                    'high_price': float(row[3].replace(',', '')),
                    'low_price': float(row[4].replace(',', '')),
                    'index_fund_id': index_fund_id
                }
                transaction_infos.append(transaction_info)
                if (i + 1) % 1000 == 0:  # Every 1000 rows, do a batch insert
<<<<<<< HEAD
                    self.daily_transactions.insert_daily_transactions(transaction_infos)
                    transaction_infos = []
            # Insert remaining rows that didn't make up a full batch of 1000
            if transaction_infos:
=======
                    self.index_fund_etl_util.insert_index_funds(index_funds)
                    self.daily_transactions.insert_daily_transactions(transaction_infos)
                    index_funds = []
                    transaction_infos = []
            # Insert remaining rows that didn't make up a full batch of 1000
            if index_funds:
                self.index_fund_etl_util.insert_index_funds(index_funds)
>>>>>>> daily_transactions_util
                self.daily_transactions.insert_daily_transactions(transaction_infos)

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)
