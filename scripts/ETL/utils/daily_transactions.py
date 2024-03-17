from datetime import datetime

class Daily_Transactions_ETL:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface

  def get_sandp_price(self, date_id):
    pass

  def get_gold_price(self, date_id):
    pass

  def get_oil_price(self, date_id):
    pass

  def get_currency_id(self, currency_code):
    cursor = self.dw_interface.connection.cursor()
    cursor.execute("SELECT id FROM currency WHERE code = :code", {'code': currency_code})
    currency_id = cursor.fetchone()[0]
    cursor.close()
    return currency_id

  def insert_daily_transactions(self, transactions_info):
    cursor = self.dw_interface.connection.cursor()
    cursor.execute("SELECT TO_CHAR(date_column, 'YYYY-MM-DD'), id FROM date_record")
    date_ids = {date: id for date, id in cursor}

    # Prepare the data for the batch insert
    data = []
    for transaction_info in transactions_info:
        stock_id = transaction_info.get('stock_id')
        date = transaction_info.get('date')  # YY-MM-DD
        commodity_id = transaction_info.get('commodity_id')
        index_fund_id = transaction_info.get('index_fund_id')
        bond_id = transaction_info.get('bond_id')
        currency_code = transaction_info.get('currency_code')
        price = transaction_info.get('price')
        volume = transaction_info.get('volume')
        symbol = transaction_info.get('symbol')
        open_price = transaction_info.get('open_price')
        high_price = transaction_info.get('high_price')
        low_price = transaction_info.get('low_price')

        # Look up the date ID in the dictionary
        date_id = date_ids[date]
        price_sp500 = 0
        price_gold = 0
        price_oil = 0
        currency_id = 57

        data.append((stock_id, date_id, commodity_id, index_fund_id, bond_id, currency_id, price,
                    volume, symbol, open_price, high_price, low_price, price_sp500, price_gold, price_oil))

    # Execute the batch insert
    cursor.executemany(
        "INSERT INTO daily_transactions (stock_id, date_id, commodity_id, index_fund_id, bond_id, currency_id, price, volume, symbol, open_price, high_price, low_price, price_sp500, price_gold, price_oil) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)",
        data
    )

    self.dw_interface.connection.commit()
    cursor.close()
    print("1000 Daily Transactions inserted successfully")
