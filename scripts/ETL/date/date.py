import pandas as pd

class Date_ETL:
    def __init__(self, dw_interface):
      self.dw_interface = dw_interface
      self.create_dates()
    
    def create_dates(self):
        dates = pd.date_range(start='1990-01-01', end='2024-12-31')
        df = pd.DataFrame(dates, columns=['date_column'])

        # Convert dates to strings in the format 'DD-MON-YY'
        df['date_column'] = df['date_column'].dt.strftime('%d-%b-%y').str.upper()

        print(df)

        data = [tuple(x) for x in df['date_column'].to_numpy().reshape(-1, 1)]

        cursor = self.dw_interface.connection.cursor()
        cursor.executemany(
            "INSERT INTO DATE_RECORD (date_column) VALUES (:1)",
            data
        )

        self.dw_interface.connection.commit()  # Commit the transaction
        cursor.close()
        print(f"Inserted dates into the DATE_RECORD table")