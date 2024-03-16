import os

class Visualization:
  def __init__(self, dw_interface):
      self.dw_interface = dw_interface
      print(self.get_data())

  def get_data(self):
      cursor = self.dw_interface.connection.cursor()
      cursor.execute("SELECT from DATE_RECORD where date_column = '01-JAN-90'")
      data = cursor.fetchall()
      cursor.close()
      return data




     
     
      
