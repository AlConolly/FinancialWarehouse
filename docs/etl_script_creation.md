# ETL Script Creation

Here is an example of how to create a new ETL script for this project.

## Step 1: Find the directory for the new ETL script

The ETL scripts are located in the `ETL` directory of the project. Make a folder with the name of the dimension or fact table that you are creating the ETL script for.

## Step 2: Create the ETL script

Create a new Python file in the directory that you created in step 1. The name of the file should be the name of the table that you are creating the ETL script for.

## Step 3: Write the ETL script

Write the ETL script in the Python file that you created in step 2. The script look like this and follow the same naming convention as the other ETL scripts in the project:

```python
import os

class Currency_ETL:
  def __init__(self, dw_interface, daily_transactions, script_time_tracker):
      self.dw_interface = dw_interface
      self.script_time_tracker = script_time_tracker
      self.daily_transactions = daily_transactions
      root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
      csv_file_path = os.path.join(root_dir, 'resources', 'data', '<folder name>', '<etl file name>')
      self.insert_currencyPrices(csv_file_path)
  
  def insert_currencyPrices(self, csv_file_path):
    # Write your ETL script here

  def __del__(self):
    self.script_time_tracker.track_time(self.__class__.__name__)
```

Its important to note that the `__init__` method takes two parameters, `dw_interface` and `script_time_tracker`. The `dw_interface` is an instance of the `DWInterface` class, which is used to interact with the data warehouse. The `script_time_tracker` is an instance of the `ScriptTimeTracker` class, which is used to track the time that the ETL script ran at.

## Date Format

The date format for the ETL scripts should be in the format `YY-MM-DD`. This is the format that the data warehouse uses to store dates.

Ex: `21-01-01`, `89-04-19`