class Commodity_ETL_Util:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface

  def insert_commodities(self, commodities):
      cursor = self.dw_interface.connection.cursor()
      cursor.executemany(
          "INSERT INTO commodity (name, unit_of_measure, type) VALUES (:name, :unit_of_measure, :type)",
          commodities
      )
      self.dw_interface.connection.commit()
      cursor.close()
      print("1000 Commodities inserted successfully")

  def get_max_commodity_id(self):
      cursor = self.dw_interface.connection.cursor()
      cursor.execute("SELECT MAX(id) FROM commodity")
      max_id = cursor.fetchone()[0]
      cursor.close()
      return max_id if max_id is not None else 0
