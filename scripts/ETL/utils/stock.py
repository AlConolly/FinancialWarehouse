class Stock_ETL_Util:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface

  def insert_stock(self, company_id, market_cap, exchange_market, yield_value):
    insert_query = """
    INSERT INTO STOCK (company_id, market_cap, exchange_market, yield)
    VALUES (:1, :2, :3, :4)
    """
    with self.dw_interface.connection.cursor() as cursor:
        cursor.execute(insert_query, (company_id, market_cap, exchange_market, yield_value))
    self.dw_interface.connection.commit()
    return
  
  def get_stock_id_by_company_id(self, company_id):
    query = "SELECT id FROM STOCK WHERE company_id = :1"
    with self.dw_interface.connection.cursor() as cursor:
        cursor.execute(query, (company_id,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None

  def get_company_id_by_symbol(self, symbol):
    query = "SELECT id FROM COMPANY WHERE symbol = :1"
    with self.dw_interface.connection.cursor() as cursor:
        cursor.execute(query, (symbol,))
        result = cursor.fetchone()
        if result is not None:
            return result[0]
        else:
            return None
