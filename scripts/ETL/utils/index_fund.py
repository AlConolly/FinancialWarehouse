class Index_Fund_ETL_Util:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface

  def insert_index_funds(self, index_funds):
      cursor = self.dw_interface.connection.cursor()
      cursor.executemany(
          "INSERT INTO index_fund (name, management_company, net_asset_value, yield, type) VALUES (:name, :management_company, :net_asset_value, :yield, :type)",
          index_funds
      )
      self.dw_interface.connection.commit()
      cursor.close()
      print("1000 Index Funds inserted successfully")

  def get_max_index_fund_id(self):
      cursor = self.dw_interface.connection.cursor()
      cursor.execute("SELECT MAX(id) FROM index_fund")
      max_id = cursor.fetchone()[0]
      cursor.close()
      return max_id if max_id is not None else 0
