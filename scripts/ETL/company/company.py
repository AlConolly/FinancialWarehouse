import csv
import os
from datetime import datetime

class Company_ETL:
  def __init__(self, dw_interface, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', 'company', 'company_sandp.csv')
      self.insert_companies(csv_file_path)

  def insert_companies(self, csv_file_path):
      with open(csv_file_path, 'r') as file:
          csv_reader = csv.reader(file)
          next(csv_reader)  # Skip the header row
          for row in csv_reader:
              Symbol, Security, GICS_Sector, GICS_Sub_Industry, Headquarters_Location, Date_added, CIK, Founded = row
              Founded = Founded.split(' ')[0]  # Keep only the part before the space
              self.insert_company(Security, Headquarters_Location, GICS_Sector, Date_added, Founded, Symbol)

  def insert_company(self, name, hq_address, sector, date_added, founded, symbol):
      cursor = self.dw_interface.connection.cursor()
      try:
          # Parse the original date format
          parsed_date = datetime.strptime(date_added, '%Y-%m-%d')
          # Convert it to the desired format
          date_added = parsed_date.strftime('%d-%b-%y')
      except ValueError:
          print(f"Date {date_added} does not match format 'YYYY-MM-DD'. Skipping row.")
          return

      # If founded is only a year, default to January 1st of that year
      if '/' in founded:
        founded = founded.split('/')[0]
      if len(founded) == 4 and founded.isdigit():
        founded = f"01-JAN-{founded}"

      cursor.execute("SELECT COUNT(*) FROM company WHERE symbol = :symbol", {'symbol': symbol})
      if cursor.fetchone()[0] > 0:
        print(f"Symbol {symbol} already exists in the database. Skipping row.")
        return

      cursor.execute(
          "INSERT INTO company (name, hq_address, sector, date_added, founded, symbol) VALUES (:name, :hq_address, :sector, TO_DATE(:date_added, 'DD-MON-YY'), TO_DATE(:founded, 'DD-MON-YYYY'), :symbol)",
          {'name': name, 'hq_address': hq_address, 'sector': sector, 'date_added': date_added, 'founded': founded, 'symbol': symbol}
      )
      self.dw_interface.connection.commit()  # Commit the transaction
      cursor.close()
      print(f"Inserted {name} into the company table")

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)