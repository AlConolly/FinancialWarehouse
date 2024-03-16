import os

class Visualization:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface
      print(self.get_data())

  def get_data(self):
      cursor = self.dw_interface.connection.cursor()
      cursor.execute("SELECT * from company")
      data = cursor.fetchall()
      cursor.close()
      return data




     
     
      
