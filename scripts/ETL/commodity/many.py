import os
import csv
from scripts.ETL.utils.commodity import Commodity_ETL_Util

class Commodity_Many_ETL():
    def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      self.commodity_etl_util = Commodity_ETL_Util(dw_interface)
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', 'commodity', 'various_commodities.csv')
      self.insert_many_commodities(csv_file_path)

    def insert_many_commodities(self, csv_file_path):
        # Map commodity names to their IDs
        commodity_ids = {
            "WHEAT": 53,
            "SUGAR": 54,
            "CORN": 43,
            "COTTON": 58,
            "SOYBEAN MEAL": 49,
            "HRW WHEAT": 57,
            "SOYBEAN OIL": 47,
            "COFFEE": 55,
            "SOYBEANS": 42,
            "LOW SULPHUR GAS OIL": 45,
            "NATURAL GAS": 41,
            "ULS DIESEL": 51,
            "CRUDE OIL": 2,
            "ZINC": 50,
            "ALUMINIUM": 48,
            "COPPER": 44,
            "NICKEL": 52,
            "LEAN HOGS": 56,
            "LIVE CATTLE": 46,
            "GOLD": 1,
            "SILVER": 22
        }

        # Load date_ids
        date_ids = self.daily_transactions.load_date_ids()

        transactions_info = []
        with open(csv_file_path, 'r') as file:
            csv_reader = csv.reader(file)
            headers = next(csv_reader)

            for row in csv_reader:
                date = row[0]
                for i, price in enumerate(row[1:], start=1):
                    commodity = headers[i]
                    commodity_id = commodity_ids.get(commodity.upper())
                    date_id = date_ids.get(date)

                    if commodity_id is not None and date_id is not None and price:
                        transactions_info.append({
                            'date': date,
                            'commodity_id': commodity_id,
                            'price': price
                        })
                        # print(f"saved {commodity_id}, {date}, {price}")
    
        # Prepare data for insert and insert into DAILY_TRANSACTIONS table
        self.daily_transactions.insert_daily_transactions(transactions_info)

        print(f"Inserted commodity prices into the DAILY_TRANSACTIONS table")

    def __del__(self):
        self.script_time_tracker.track_time(self.__class__.__name__)   