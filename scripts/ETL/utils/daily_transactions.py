


from datetime import datetime


class Daily_Transactions_ETL:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface


  def insert_daily_transaction(self, transaction_info):
    pass
      # stock_id = transaction_info['stock_id']
      # date = transaction_info['date'] #YY-MM-DD
      # commodity_id = transaction_info['commodity_id']
      # index_fund_id = transaction_info['index_fund_id']
      # bond_id = transaction_info['bond_id']
      # currency_code = transaction_info['currency_code']
      # price = transaction_info['price']
      # volume = transaction_info['volume']
      # symbol = transaction_info['symbol']
      # open_price = transaction_info['open_price']
      # high_price = transaction_info['high_price']
      # low_price = transaction_info['low_price']

      # date_id = self.get_date_id(date)
      # price_sandp = self.get_sandp_price(date_id)
      # price_gold = self.get_gold_price(date_id)
      # price_oil = self.get_oil_price(date_id)
      # currency_id = self.get_currency_id(currency_code)

      # cursor = self.dw_interface.connection.cursor()
      # cursor.execute(
      #     "INSERT INTO daily_transactions (stock_id, date_id, commodity_id, index_fund_id, bond_id, currency_id, price, volume, symbol, open_price, high_price, low_price, sandp_price, gold_price, oil_price) VALUES (:stock_id, :date_id, :commodity_id, :index_fund_id, :bond_id, :currency_id, :price, :volume, :symbol, :open_price, :high_price, :low_price, :sandp_price, :gold_price, :oil_price)",
      #     {'stock_id': stock_id, 'date_id': date_id, 'commodity_id': commodity_id, 'index_fund_id': index_fund_id, 'bond_id': bond_id, 'currency_id': currency_id, 'price': price, 'volume': volume, 'symbol': symbol, 'open_price': open_price, 'high_price': high_price, 'low_price': low_price, 'sandp_price': price_sandp, 'gold_price': price_gold, 'oil_price': price_oil}
      # )
      # self.dw_interface.connection.commit()
      # cursor.close()

  def get_sandp_price(self, date_id):
    pass

  def get_gold_price(self, date_id):
    pass

  def get_oil_price(self, date_id):
    pass

  def get_currency_id(self, currency_code):
    pass


  # Parameter Date is in 'YYYY-MM-DD' format
  def get_date_id(self, date):
      cursor = self.dw_interface.connection.cursor()
      date_obj = datetime.strptime(date, '%Y-%m-%d')
      day, month, year = date_obj.day, date_obj.month, date_obj.year
      cursor.execute("""
          SELECT id FROM date_record
          WHERE EXTRACT(DAY FROM date_column) = :day_var
          AND EXTRACT(MONTH FROM date_column) = :month_var
          AND EXTRACT(YEAR FROM date_column) = :year_var
      """, {'day_var': day, 'month_var': month, 'year_var': year})
      date_id = cursor.fetchone()[0]
      cursor.close()
      return date_id
