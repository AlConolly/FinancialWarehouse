import csv
import os
from scripts.ETL.utils.index_fund import Index_Fund_ETL_Util
from datetime import datetime

class VTI_ETL:
    def __init__(self, dw_interface, daily_transactions, script_time_tracker):
        self.dw_interface = dw_interface
        self.script_time_tracker = script_time_tracker
        self.daily_transactions = daily_transactions
        self.index_fund_etl_util = Index_Fund_ETL_Util(dw_interface)
        root_dir = os.path.dirname(os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        csv_file_paths = [os.path.join(root_dir, 'resources', 'data', 'index_fund', 'VangaurdTI.csv')]
        self.insert_index_fund_prices(csv_file_paths)

    def insert_index_fund_prices(self, csv_file_paths):
        index_fund_id = self.index_fund_etl_util.get_index_fund_id('VTI')
        print(index_fund_id)
        if index_fund_id is None:
            raise Exception("Index Fund ID not found for VTI")
        for csv_file_path in csv_file_paths:
            with open(csv_file_path, 'r') as file:
                csv_reader = csv.reader(file)
                next(csv_reader)
                transaction_infos = []
                for i, row in enumerate(csv_reader):
                    try:
                         date = datetime.strptime(row[0], '%m/%d/%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        try:
                            date = datetime.strptime(row[0], '%Y-%m-%d').strftime('%Y-%m-%d')
                        except ValueError:
                            raise ValueError("Date format not recognized for row: {}".format(row))
            
                        transaction_info = {
                        'date': date,
                        'price': float(row[1].replace(',', '')),
                        'symbol': 'VTI',
                        'open_price': float(row[2].replace(',', '')),
                        'high_price': float(row[3].replace(',', '')),
                        'low_price': float(row[4].replace(',', '')),
                        'index_fund_id': index_fund_id
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