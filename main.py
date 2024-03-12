import os
from data_warehouse.connection import DW_Interface
from scripts.ETL.company_table import Company_ETL
from scripts.ETL.oil_table import Oil_ETL
from dotenv import load_dotenv

load_dotenv()
config_dir = os.getenv('CONFIG_DIR')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
dsn = os.getenv('DSN')
wallet_location = os.getenv('WALLET_LOCATION')
wallet_password = os.getenv('WALLET_PASSWORD')

DW_Interface = DW_Interface(config_dir, user, password, dsn, wallet_location, wallet_password)
Company_ETL = Company_ETL(DW_Interface)
Oil_ETL = Oil_ETL(DW_Interface)
