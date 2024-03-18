class Stock_ETL_Util:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface

  # def get_stock_id(self):
  #     cursor = self.dw_interface.connection.cursor()
  #     cursor.execute("SELECT MAX(id) FROM stock")
  #     max_id = cursor.fetchone()[0]
  #     cursor.close()
  #     return max_id if max_id is not None else 0
