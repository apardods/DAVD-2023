import pandas as pd
import requests
import json

API_KEY = '0OYRW0GV8ZO17FE4'

def load_macro_data(value):
    value_api = value.replace(' ', '_').upper()
    # url = f'https://www.alphavantage.co/query?function={value_api}&interval=quarterly&apikey={API_KEY}'
    # r = requests.get(url)
    # data = r.json()
    # df = pd.DataFrame(data['data'])
    # df['date'] = pd.to_datetime(df['date'])
    # df = df.sort_values(by='date').set_index('date')
    # df['value'] = pd.to_numeric(df['value'], errors='coerce')
    with open(f'resources\\{value_api}.json') as json_file:
        data_json = json.load(json_file)
    df = pd.DataFrame(data_json['data'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').set_index('date')
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df

def load_target_data(value):
    # value_api = value.replace(' ', '_').upper()
    # url = f'https://www.alphavantage.co/query?function={value_api}&interval=yearly&apikey={API_KEY}'
    # r = requests.get(url)
    # data = r.json()
    # df = pd.DataFrame(data['data'])
    # df['date'] = pd.to_datetime(df['date'])
    # df = df.sort_values(by='date').set_index('date')
    # df_quarterly = df[df.index.month.isin([1, 4, 7, 10])]
    # df['value'] = pd.to_numeric(df['value'], errors='coerce')
    with open('resources\\WTI.json') as json_file:
        data_json = json.load(json_file)
    df = pd.DataFrame(data_json['data'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').set_index('date')
    df_quarterly = df[df.index.month.isin([1, 4, 7, 10])]
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    return df_quarterly