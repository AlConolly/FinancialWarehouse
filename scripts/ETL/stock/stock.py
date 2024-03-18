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
      self.insert_stock_prices(csv_file_path)

  # def load_company_ids(self):
  #     cursor = self.dw_interface.connection.cursor()
  #     cursor.execute(
  #         "SELECT symbol, id FROM company")
  #     company_ids = {symbol: id for symbol, id in cursor}
  #     cursor.close()
  #     print("Company_IDs loaded successfully")
  #     return company_ids

  # def insert_stock_prices(self, csv_file_path):
  #   company_ids = self.load_company_ids()
  #   with open(csv_file_path, 'r') as file:
  #     csv_reader = csv.reader(file)
  #     next(csv_reader)
  #     stocks = []
  #     transaction_infos = []
  #     stock_id = self.stock_etl_util.get_max_stock_id()
  #     for i, row in enumerate(csv_reader):
  #         company_id = company_ids[row[1]]
  #         transaction_info = {
  #             'date': row[0],
  #             'price': row[4],
  #             'symbol': 'GOLD',
  #             'open_price': row[1],
  #             'high_price': row[2],
  #             'low_price': row[3],
  #             'volume': row[5],
  #             'stock_id': stock_id
  #         }
  #         transaction_infos.append(transaction_info)
  #         if (i + 1) % 2000 == 0:
  #             self.stock_etl_util.insert_stocks(stocks)
  #             self.daily_transactions.insert_daily_transactions(transaction_infos)
  #             stocks = []
  #             transaction_infos = []
  #     # Insert remaining rows that didn't make up a full batch of 1000
  #     if stocks:
  #         self.stock_etl_util.insert_stocks(stocks)
  #         self.daily_transactions.insert_daily_transactions(transaction_infos)

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)