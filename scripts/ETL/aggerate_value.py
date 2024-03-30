import os

class Aggerate_Value_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.daily_transactions = daily_transactions
      # self.insert_aggerate_values_bonds()

  def insert_aggerate_values_stocks(self):
    with self.dw_interface.connection.cursor() as cur:
      cur.execute("SELECT DISTINCT stock_id FROM DAILY_TRANSACTIONS")
      stock_ids = cur.fetchall()

      for stock_id_tuple in stock_ids:
          stock_id = stock_id_tuple[0]
          if (stock_id != None):
            # Create a temporary table with the running averages
            cur.execute(f"""
                CREATE TABLE TEMP_AVG_PRICE AS
                SELECT dt1.stock_id, dt1.date_id, AVG(dt2.price) AS avg_price
                FROM DAILY_TRANSACTIONS dt1
                JOIN DAILY_TRANSACTIONS dt2 ON dt1.stock_id = dt2.stock_id AND TRUNC(dt2.date_id) <= TRUNC(dt1.date_id)
                WHERE dt1.stock_id = {stock_id}
                GROUP BY dt1.stock_id, dt1.date_id
            """)

            # Update the DAILY_TRANSACTIONS table using a join with the temporary table
            cur.execute("""
                UPDATE (
                  SELECT dt.AVG_PRICE_OVER_TIME, temp.avg_price
                  FROM DAILY_TRANSACTIONS dt
                  JOIN TEMP_AVG_PRICE temp ON dt.stock_id = temp.stock_id AND dt.date_id = temp.date_id
                ) t
                SET t.AVG_PRICE_OVER_TIME = t.avg_price
            """)

            # Drop the temporary table
            cur.execute("DROP TABLE TEMP_AVG_PRICE")

            # Commit the transaction
            self.dw_interface.connection.commit()

            print(f"Successfully updated AVG_PRICE_OVER_TIME for stock_id {stock_id}")

  def insert_aggerate_values_commodites(self):
    with self.dw_interface.connection.cursor() as cur:
        cur.execute("SELECT DISTINCT commodity_id FROM DAILY_TRANSACTIONS")
        commodity_ids = cur.fetchall()

        for commodity_id_tuple in commodity_ids:
            commodity_id = commodity_id_tuple[0]
            if commodity_id is not None:
                # Create a temporary table with the running averages
                cur.execute(f"""
                    CREATE TABLE TEMP_AVG_PRICE AS
                    SELECT dt1.commodity_id, dt1.date_id, AVG(dt2.price) AS avg_price
                    FROM DAILY_TRANSACTIONS dt1
                    JOIN DAILY_TRANSACTIONS dt2 ON dt1.commodity_id = dt2.commodity_id AND TRUNC(dt2.date_id) <= TRUNC(dt1.date_id)
                    WHERE dt1.commodity_id = {commodity_id}
                    GROUP BY dt1.commodity_id, dt1.date_id
                """)

                # Update the DAILY_TRANSACTIONS table using a join with the temporary table
                cur.execute("""
                    UPDATE (
                      SELECT dt.AVG_PRICE_OVER_TIME, temp.avg_price
                      FROM DAILY_TRANSACTIONS dt
                      JOIN TEMP_AVG_PRICE temp ON dt.commodity_id = temp.commodity_id AND dt.date_id = temp.date_id
                    ) t
                    SET t.AVG_PRICE_OVER_TIME = t.avg_price
                """)

                # Drop the temporary table
                cur.execute("DROP TABLE TEMP_AVG_PRICE")

                # Commit the transaction
                self.dw_interface.connection.commit()

                print(f"Successfully updated AVG_PRICE_OVER_TIME for commodity_id {commodity_id}")

  def insert_aggerate_values_index_fund(self):
    with self.dw_interface.connection.cursor() as cur:
        cur.execute("SELECT DISTINCT index_fund_id FROM DAILY_TRANSACTIONS")
        index_fund_ids = cur.fetchall()

        for index_fund_id_tuple in index_fund_ids:
            index_fund_id = index_fund_id_tuple[0]
            if index_fund_id is not None:
                # Create a temporary table with the running averages
                cur.execute(f"""
                    CREATE TABLE TEMP_AVG_PRICE AS
                    SELECT dt1.index_fund_id, dt1.date_id, AVG(dt2.price) AS avg_price
                    FROM DAILY_TRANSACTIONS dt1
                    JOIN DAILY_TRANSACTIONS dt2 ON dt1.index_fund_id = dt2.index_fund_id AND TRUNC(dt2.date_id) <= TRUNC(dt1.date_id)
                    WHERE dt1.index_fund_id = {index_fund_id}
                    GROUP BY dt1.index_fund_id, dt1.date_id
                """)

                # Update the DAILY_TRANSACTIONS table using a join with the temporary table
                cur.execute("""
                    UPDATE (
                      SELECT dt.AVG_PRICE_OVER_TIME, temp.avg_price
                      FROM DAILY_TRANSACTIONS dt
                      JOIN TEMP_AVG_PRICE temp ON dt.index_fund_id = temp.index_fund_id AND dt.date_id = temp.date_id
                    ) t
                    SET t.AVG_PRICE_OVER_TIME = t.avg_price
                """)

                # Drop the temporary table
                cur.execute("DROP TABLE TEMP_AVG_PRICE")

                # Commit the transaction
                self.dw_interface.connection.commit()

                print(f"Successfully updated AVG_PRICE_OVER_TIME for index_fund_id {index_fund_id}")

  def insert_aggerate_values_bonds(self):
    with self.dw_interface.connection.cursor() as cur:
        cur.execute("SELECT DISTINCT bond_id FROM DAILY_TRANSACTIONS")
        bond_ids = cur.fetchall()

        for bond_id_tuple in bond_ids:
            bond_id = bond_id_tuple[0]
            if bond_id is not None:
                # Create a temporary table with the running averages
                cur.execute(f"""
                    CREATE TABLE TEMP_AVG_PRICE AS
                    SELECT dt1.bond_id, dt1.date_id, AVG(dt2.price) AS avg_price
                    FROM DAILY_TRANSACTIONS dt1
                    JOIN DAILY_TRANSACTIONS dt2 ON dt1.bond_id = dt2.bond_id AND TRUNC(dt2.date_id) <= TRUNC(dt1.date_id)
                    WHERE dt1.bond_id = {bond_id}
                    GROUP BY dt1.bond_id, dt1.date_id
                """)

                # Update the DAILY_TRANSACTIONS table using a join with the temporary table
                cur.execute("""
                    UPDATE (
                      SELECT dt.AVG_PRICE_OVER_TIME, temp.avg_price
                      FROM DAILY_TRANSACTIONS dt
                      JOIN TEMP_AVG_PRICE temp ON dt.bond_id = temp.bond_id AND dt.date_id = temp.date_id
                    ) t
                    SET t.AVG_PRICE_OVER_TIME = t.avg_price
                """)

                # Drop the temporary table
                cur.execute("DROP TABLE TEMP_AVG_PRICE")

                # Commit the transaction
                self.dw_interface.connection.commit()

                print(f"Successfully updated AVG_PRICE_OVER_TIME for bond_id {bond_id}")
