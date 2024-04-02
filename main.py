import os, click, json, textwrap
from dotenv import load_dotenv
from pathlib import Path

# Oracle Connection
from oracle.connection import DW_Interface

# ETL Utils
from scripts.ETL.utils.script_time_tracker import ScriptTimeTracker
from scripts.ETL.utils.daily_transactions import Daily_Transactions_ETL

# ETL Classes
from scripts.ETL.currency.currency import Currency_ETL
from scripts.ETL.company.company import Company_ETL
from scripts.ETL.commodity.gold import Commodity_Gold_ETL
from scripts.ETL.commodity.oil import Commodity_Oil_ETL
from scripts.ETL.commodity.silver import Commodity_Silver_ETL
from scripts.ETL.commodity.many import Commodity_Many_ETL
from scripts.ETL.stock.stock import Stock_ETL
from scripts.ETL.date.date import Date_ETL
from scripts.ETL.index_fund.sp_500 import SP_500_ETL
from scripts.ETL.bond.bond import Bond_ETL

#machine_learning
from machine_learning.sklearn_test import sklearn_test
from machine_learning.sklearn_test_MLP import sklearn_test_MLP

# Visualization Utils
from scripts.Visualization.Visualization import Visualization
import pandas as pd
from scripts.ETL.index_fund.vti import VTI_ETL
from scripts.ETL.utils.aggerate_value import Aggerate_Value_ETL

# ETL Class Mapping
script_classes = {
    'Currency': Currency_ETL,
    'Company': Company_ETL,
    'Commodity_Gold': Commodity_Gold_ETL,
    'Commodity_Oil': Commodity_Oil_ETL,
    'Commodity_Silver': Commodity_Silver_ETL,
    'Commodity_Many': Commodity_Many_ETL,
    'Stock': Stock_ETL,
    'Date': Date_ETL,
    'Sp_500': SP_500_ETL,
    'Bond': Bond_ETL,
    'Index_fund_Vti': VTI_ETL,
    'Commodity_Silver': Commodity_Silver_ETL,
    'Commodity_Many': Commodity_Many_ETL,
    'Stock': Stock_ETL,
    'Date': Date_ETL,
    'Sp_500': SP_500_ETL,
    'Aggerate_value': Aggerate_Value_ETL
}

load_dotenv()
config_dir = os.getenv('CONFIG_DIR')
user = os.getenv('USER')
password = os.getenv('PASSWORD')
dsn = os.getenv('DSN')
wallet_location = os.getenv('WALLET_LOCATION')
wallet_password = os.getenv('WALLET_PASSWORD')
DW_Interface = DW_Interface(config_dir, user, password, dsn, wallet_location, wallet_password)

Script_Tracker = ScriptTimeTracker()

def list_files(startpath):
    return [
        f"{path.parent.stem.capitalize()}_{path.stem.capitalize()}"
        if len([p for p in path.parent.glob('*') if p.is_file() and p.stem != '__init__' and p.suffix != '.txt']) > 1 else path.stem.capitalize()
        for path in Path(startpath).rglob('*')
        if path.is_file() and path.stem != '__init__' and 'utils' not in path.parts and '__pycache__' not in path.parts and path.suffix != '.txt'
    ]

@click.command()
def run_script():
    print("-----------------------")
    print("Financial Warehouse ETL")
    print("-----------------------")
    scripts = list_files('scripts/ETL')
    with open('script_history.json', 'r') as file:
        data = json.load(file)
    completed_scripts = []
    available_scripts = []
    counter = 1
    for script in scripts:
        complete = data.get(f"{script}_ETL", False)
        first_run = data.get(f"{script}_ETL_First", 'Never executed')
        last_run = data.get(f"{script}_ETL_Last", 'Never executed')
        if first_run != 'Never executed':
            # Keep only the date and time, remove the microseconds
            first_run = first_run[:19]
        if last_run != 'Never executed':
            # Keep only the date and time, remove the microseconds
            last_run = last_run[:19]
        if complete:
            completed_scripts.append(script)
            print(f"   {script}")
        else:
            available_scripts.append(script)
            print(f"{counter}. {script}")
            counter += 1
        print(textwrap.indent(f"First executed: {first_run}", '   '))
        print(textwrap.indent(f"Last executed: {last_run}", '   '))
        print(textwrap.indent(f"Completed: {'Yes' if complete else 'No'}", '   '))
        print()
    print()  # Print a blank line
    choice = click.prompt(
        'Enter the number of the ETL script you want to run', type=int) - 1
    script = available_scripts[choice]
    script_class = script_classes[script]
    print("Grabbing measures for our ETL scripts...")
    Daily_Transactions_ETL_Instance = Daily_Transactions_ETL(DW_Interface)
    print("Measures grabbed!")
    script_class(DW_Interface, Daily_Transactions_ETL_Instance, Script_Tracker)

if __name__ == '__main__':
    #sklearn_test(DW_Interface)
    run_script()
