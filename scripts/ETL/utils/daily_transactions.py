class Daily_Transactions_ETL:
    def __init__(self, dw_interface):
        self.dw_interface = dw_interface
        self.date_ids = self.load_date_ids()
        self.prices = self.load_prices()
        self.currency_ids = self.load_currency_ids()

    def load_date_ids(self):
        cursor = self.dw_interface.connection.cursor()
        cursor.execute(
            "SELECT TO_CHAR(date_column, 'YYYY-MM-DD'), id FROM date_record")
        date_ids = {date: id for date, id in cursor}
        cursor.close()
        print("Date_ID loaded successfully")
        return date_ids

    def load_prices(self):
        cursor = self.dw_interface.connection.cursor()
        cursor.execute(
            "SELECT date_id, price_gold, price_oil, price_sp500 FROM measure_helper")
        prices = {date_id: (price_gold, price_oil, price_sp500)
                  for date_id, price_gold, price_oil, price_sp500 in cursor}
        cursor.close()
        print("Numerical measures loaded successfully")
        return prices

    def load_currency_ids(self):
        cursor = self.dw_interface.connection.cursor()
        cursor.execute("SELECT id, code FROM currency")
        currency_ids = {code: id for id, code in cursor}
        cursor.close()
        print("Currency_ID loaded successfully")
        return currency_ids

    def insert_daily_transactions(self, transactions_info):
        print("Inserting Daily Transactions")
        cursor = self.dw_interface.connection.cursor()
        data = self.prepare_data_for_insert(transactions_info)
        cursor.executemany(
            "INSERT INTO daily_transactions (stock_id, date_id, commodity_id, index_fund_id, bond_id, currency_id, price, volume, symbol, open_price, high_price, low_price, price_sp500, price_gold, price_oil) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)",
            data
        )
        self.dw_interface.connection.commit()
        cursor.close()
        print("Daily Transactions Batch inserted successfully")

    def prepare_data_for_insert(self, transactions_info):
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

            date_id = self.date_ids[date]
            price_gold, price_oil, price_sp500 = self.prices.get(date_id, (0, 0, 0))
            currency_id = self.currency_ids.get(
                currency_code, 57)  # Default to USD if not found
            data.append((stock_id, date_id, commodity_id, index_fund_id, bond_id, currency_id, price,
                        volume, symbol, open_price, high_price, low_price, price_sp500, price_gold, price_oil))
            print(data[0])
        print("Data prepared for insert successfully")
        return data
