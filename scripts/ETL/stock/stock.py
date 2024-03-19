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

    with open(csv_file_path, 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)
        transaction_infos = []
        for i, row in enumerate(csv_reader):
            if i <= last_row:
                continue
            if row[1] != 'MMM':
                break

            transaction_info = {
                'date': row[0],
                'price': round(float(row[3]), 2),
                'symbol': 'MMM',
                'open_price': round(float(row[6]), 2),
                'high_price': round(float(row[4]), 2),
                'low_price': round(float(row[5]), 2),
                'volume': int(row[7]),
                'stock_id': 4
            }

            transaction_infos.append(transaction_info)
            if (i + 1) % 1000 == 0:
                self.daily_transactions.insert_daily_transactions(transaction_infos)
                transaction_infos = []

                # Store the index of the last processed row
                with open('last_row.txt', 'w') as f:
                    f.write(str(i))

        if transaction_infos:
            self.daily_transactions.insert_daily_transactions(transaction_infos)

            # Store the index of the last processed row
            with open('last_row.txt', 'w') as f:
                f.write(str(i))

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)