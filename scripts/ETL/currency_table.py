'''
This file will load the currency table in our database. Using an api for the newest exchange rates and codes, and a 
csv to attach a country and other info to those codes from the api. This is done to not have to pay for a premium api.

api: https://www.exchangerate-api.com/
'''

import os
import csv
import requests
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
API_KEY = os.getenv('currencyapikey')

# Make a request to the API
url = f'https://v6.exchangerate-api.com/v6/{API_KEY}/latest/USD'
response = requests.get(url)
api_data = response.json()

# Open the CSV file and read the data
script_dir = os.path.dirname(os.path.realpath(__file__))
csv_file_path = os.path.join(script_dir, 'codes-all.csv')
with open(csv_file_path, 'r') as file:
    csv_data = csv.DictReader(file)
    countries_data = []
    for row in csv_data:
        country_data = {
            'name': row['Entity'],
            'currency': row['Currency'],
            'code': row['AlphabeticCode'],
            'numeric_code': row['NumericCode'],
            'minor_unit': row['MinorUnit'],
            'withdrawal_date': row['WithdrawalDate'],
            'exchange_rate_usd': api_data['conversion_rates'].get(row['AlphabeticCode'], None)
        }
        countries_data.append(country_data)


print(countries_data[0])
print("-----------------------------------------------------------------------")
print(countries_data[1])
print("-----------------------------------------------------------------------")
print(countries_data[2])

