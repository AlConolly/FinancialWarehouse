import csv, os, json, datetime, pytz

class Currency_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', 'currency', 'Currencies relative to USD.csv')
      self.insert_currencyPrices(csv_file_path)

  def insert_currencyPrices(self, csv_file_path):
      with open(csv_file_path, 'r') as file:
          csv_reader = csv.reader(file)
          next(csv_reader)  # Skip the header row
          for row in csv_reader:
              Date,Country,Currency,Country_Currency_Description,Exchange,InverseExchangeRate,EffectiveDate,SourceLineNumber,FiscalYear,FiscalQuarter,Year,Quarter,Month,Day,currencyCode = row
              #Exchange is the exchange rate from USD to the currency. 
              self.insert_currencyPrice(currencyCode,Exchange, Country_Currency_Description, Country) #USD_AM is used to store the price and other columns are not used

  def insert_currencyPrice(self,currencyCode,exchangeRate, currencyName, country):
      cursor = self.dw_interface.connection.cursor()

      cursor.execute("SELECT COUNT(*) FROM currency WHERE code = :currencyCode", {'currencyCode': currencyCode})
      if cursor.fetchone()[0] > 0:
        print(f"currency with symbol {currencyCode} already exists in the database. Skipping row. Note that some countries use the same currencies")
        return
      cursor.execute(
          "INSERT INTO currency (name,country,code,exchange_rate) VALUES (:currencyName, :country, :currencyCode, :exchangeRate)",
          {'currencyName': currencyName, 'country': country, 'currencyCode': currencyCode, 'exchangeRate': exchangeRate}
      )

      self.dw_interface.connection.commit()  # Commit the transaction
      cursor.close()
      print(f"Inserted {currencyName} with Symbol {currencyCode} into the Currency table")

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)
