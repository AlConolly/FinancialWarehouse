import csv
import os
from datetime import datetime

class Commodity_Gold_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', 'commodity', 'LBMA-GOLD.csv')
      self.insert_goldPrices(csv_file_path)

  def insert_goldPrices(self, csv_file_path):
      with open(csv_file_path, 'r') as file:
          csv_reader = csv.reader(file)
          next(csv_reader)  # Skip the header row
          for row in csv_reader:
              Date,USD_AM,USD_PM,GBP_AM,GBP_PM,EURO_AM,EURO_PM = row
              self.insert_goldPrice(Date,USD_AM) #USD_AM is used to store the price and other columns are not used

  def insert_goldPrice(self,input_date,price):
      cursor = self.dw_interface.connection.cursor()
      try:
          # Parse the original date format
          parsed_date = datetime.strptime(input_date, '%Y-%m-%d')

          commodity_date = parsed_date.strftime('%d-%b-%y')
      except ValueError:
          print(f"Date {input_date} does not match format 'YYYY-MM-DD'. Skipping row.")
          return

      # Create a bind variable for an integer
      new_id = cursor.var(int)

      #create date row if it doesn't exist
      cursor.execute("SELECT COUNT(*) FROM date_record WHERE date_column = :commodity_date", {'commodity_date': commodity_date})
      if cursor.fetchone()[0]==0: #returns true if no record exists
        cursor.execute("INSERT INTO date_record (date_column) VALUES (:commodity_date) RETURNING id INTO :new_id",
                        {'commodity_date': commodity_date, 'new_id': new_id})
        #gets id of date just created
        date_id = new_id.getvalue()[0]
      else:
        # If the record already exists, fetch the ID directly
        cursor.execute("SELECT id FROM date_record WHERE date_column = :commodity_date", {'commodity_date': commodity_date})
        new_id.setvalue(0, cursor.fetchone()[0])  # Set the value of the bind variable
        #gets id of date
        date_id = new_id.getvalue()

      

      cursor.execute("SELECT COUNT(*) FROM daily_transactions WHERE date_id = :date_id AND commodity_id IS NOT NULL", {'date_id': date_id})
      if cursor.fetchone()[0] > 0:
        print(f"Gold Price at date {commodity_date} already exists in the database. Skipping row.")
        return

      # Create a bind variable for an integer
      new_id2 = cursor.var(int)

      cursor.execute(
          "INSERT INTO commodity (name, unit_of_measure,type) VALUES (:name, :price, :type) RETURNING id INTO :new_id",
          {'name': f"Gold Price on {parsed_date}", 'price': price, 'type': "gold", 'new_id': new_id2}
      )
      gold_id = new_id2.getvalue()[0]

      cursor.execute(
          "INSERT INTO daily_transactions (commodity_id,date_id,price) VALUES (:gold_id, :date_id, :price)",
          {'gold_id': gold_id, "date_id": date_id , 'price': price}
      )


      self.dw_interface.connection.commit()  # Commit the transaction
      cursor.close()
      print(f"Inserted Gold Price from {commodity_date} into the Daily_Transaction and Commodity table")

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)
