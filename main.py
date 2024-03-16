import os, click, json, datetime
from dotenv import load_dotenv
from pathlib import Path

from oracle.connection import DW_Interface
from scripts.ETL.utils.script_time_tracker import ScriptTimeTracker

# ETL Classes
from scripts.ETL.currency.currency import Currency_ETL
from scripts.ETL.company.company import Company_ETL
from scripts.ETL.commodity.gold import Commodity_Gold_ETL
from scripts.ETL.commodity.oil import Commodity_Oil_ETL

# ETL Class Mapping
script_classes = {
    'Currency': Currency_ETL,
    'Company': Company_ETL,
    'Commodity_Gold': Commodity_Gold_ETL,
    'Commodity_Oil': Commodity_Oil_ETL
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
        if len([p for p in path.parent.glob('*') if p.is_file() and p.stem != '__init__']) > 1 else path.stem.capitalize()
        for path in Path(startpath).rglob('*')
        if path.is_file() and path.stem != '__init__' and 'utils' not in path.parts and '__pycache__' not in path.parts
    ]

@click.command()
def run_script():
    print("-----------------------")
    print("Financial Warehouse ETL")
    print("-----------------------")
    scripts = list_files('scripts/ETL')
    with open('script_history.json', 'r') as file:
        data = json.load(file)
    for i, script in enumerate(scripts, start=1):
      last_run = data.get(f"{script}_ETL", 'Never executed')
      if last_run != 'Never executed':
          last_run = last_run[:19]  # Keep only the date and time, remove the microseconds
      print(f"{i}. {script} (Last executed: {last_run})")
    print()  # Print a blank line
    choice = click.prompt(
        'Enter the number of the ETL script you want to run', type=int) - 1
    script = scripts[choice]
    script_class = script_classes[script]
    script_class(DW_Interface, Script_Tracker)

if __name__ == '__main__':
    run_script()
