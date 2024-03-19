class Bond_ETL_Util:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface

  def get_bond_id(self, name):
    cursor = self.dw_interface.connection.cursor()
    cursor.execute("SELECT id FROM bond WHERE name = :name", {'name': name})
    id = cursor.fetchone()[0]
    cursor.close()
    return id if id is not None else None
