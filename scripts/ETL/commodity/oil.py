import csv
import os
from datetime import datetime

class Commodity_Oil_ETL:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface
      script_dir = os.path.dirname(os.path.realpath(__file__))
      csv_file_path = os.path.join(script_dir, 'BrentOilPrices.csv')
      self.insert_oilPrices(csv_file_path)

  def insert_oilPrices(self, csv_file_path):
      with open(csv_file_path, 'r') as file:
          csv_reader = csv.reader(file)
          next(csv_reader)  # Skip the header row
          for row in csv_reader:
              Date,Price = row
              self.insert_oilPrice(Date,Price)

  def insert_oilPrice(self,input_date,price):
      cursor = self.dw_interface.connection.cursor()
      try:
          # Parse the original date format
          parsed_date = datetime.strptime(input_date, '%d-%b-%y')

          commodity_date = parsed_date.strftime('%d-%b-%y')
      except ValueError:
          try:
            parsed_date = datetime.strptime(input_date, '%b-%d-%Y')

            commodity_date = parsed_date.strftime('%d-%b-%y')
          except ValueError:
            print(f"Date {input_date} does not match format 'DD-Mon-YY' or 'Mon DD, YYYY'. Skipping row.")
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
        print(f"Oil Price at date {commodity_date} already exists in the database. Skipping row.")
        return

      # Create a bind variable for an integer
      new_id2 = cursor.var(int)

      cursor.execute(
          "INSERT INTO commodity (name, unit_of_measure,type) VALUES (:name, :price, :type) RETURNING id INTO :new_id",
          {'name': f"Oil Price on {parsed_date}", 'price': price, 'type': "oil", 'new_id': new_id2}
      )
      oil_id = new_id2.getvalue()[0]

      cursor.execute(
          "INSERT INTO daily_transactions (commodity_id,date_id,price) VALUES (:oil_id, :date_id, :price)",
          {'oil_id': oil_id, "date_id": date_id , 'price': price}
      )


      self.dw_interface.connection.commit()  # Commit the transaction
      cursor.close()
      print(f"Inserted Oil Price from {commodity_date} into the Dailty_Transaction and Commodity table")