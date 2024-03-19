from itertools import islice
import os, csv
from scripts.ETL.utils.stock import Stock_ETL_Util

class Stock_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      self.stock_etl_util = Stock_ETL_Util(dw_interface)
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', 'stock', 'sp500_stocks.csv')
      index_csv_file_path = os.path.join(root_dir, 'scripts', 'ETL', 'stock', 'last_row.txt')
      self.insert_stock_prices(csv_file_path, index_csv_file_path)

  def insert_stock_prices(self, csv_file_path, index_csv_file_path):
    with open(index_csv_file_path, 'r') as f:
        last_row_str = f.read()
        last_row = int(last_row_str)

    prev_symbol = None
    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        transaction_infos = []
        for i, row in enumerate(islice(csv_reader, last_row, None)):
            symbol = row[1]
            company_id = None
            if symbol != prev_symbol:
                company_id = self.stock_etl_util.get_company_id_by_symbol(symbol)
                if company_id is None:
                    continue
                self.stock_etl_util.insert_stock(company_id, 0, '', 0)
                stock_id = self.stock_etl_util.get_stock_id_by_company_id(company_id)
                prev_symbol = symbol

            try:
                transaction_info = {
                    'date': row[0],
                    'price': round(float(row[3]), 2) if row[3] else 0.0,
                    'symbol': symbol,
                    'open_price': round(float(row[6]), 2) if row[6] else 0.0,
                    'high_price': round(float(row[4]), 2) if row[4] else 0.0,
                    'low_price': round(float(row[5]), 2) if row[5] else 0.0,
                    'volume': int(row[7]) if row[7] else 0,
                    'stock_id': int(stock_id)
                }
            except ValueError:
                continue

            transaction_infos.append(transaction_info)
            if (i + 1) % 1000 == 0:
                self.daily_transactions.insert_daily_transactions(
                    transaction_infos)
                transaction_infos = []

                # Store the index of the last processed row
                with open(index_csv_file_path, 'w') as f:
                    f.write(str(i))

        if transaction_infos:
            self.daily_transactions.insert_daily_transactions(
                transaction_infos)

        # Store the index of the last processed row
        with open(index_csv_file_path, 'w') as f:
            f.write(str(i))

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)