import os

class Stock_ETL:
  def __init__(self, dw_interface, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      # root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      # csv_file_path = os.path.join(root_dir, 'resources', 'data', '<folder name>', '<etl file name>')
      # self.insert_currencyPrices(csv_file_path)
  
  # def insert_currencyPrices(self, csv_file_path):
  #   # Write your ETL script here

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)