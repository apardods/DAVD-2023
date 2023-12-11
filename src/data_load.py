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
    # df_quarterly = df[df.index.month.isin([1, 4, 7, 10])]
    # df_quarterly['value'] = pd.to_numeric(df_quarterly['value'], errors='coerce')
    # df_quarterly.rename(columns={'value':value}, inplace=True)
    with open(f'./resources/macro/{value_api}.json') as json_file:
        data_json = json.load(json_file)
    df = pd.DataFrame(data_json['data'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').set_index('date')
    df_filtered = df[df.index >= '1990-01-01']
    df_quarterly = df_filtered[df_filtered.index.month.isin([1, 4, 7, 10])]
    series = pd.to_numeric(df_quarterly['value'], errors='coerce')
    df_quarterly['value'] = series
    df_quarterly.rename(columns={'value':value}, inplace=True)
    return df_quarterly

def load_target_data(value):
    value_api = value.replace(' ', '_').upper()
    # url = f'https://www.alphavantage.co/query?function={value_api}&interval=monthly&apikey={API_KEY}'
    # r = requests.get(url)
    # data = r.json()
    # print(data)
    # df = pd.DataFrame(data['data'])
    # df['date'] = pd.to_datetime(df['date'])
    # df = df.sort_values(by='date').set_index('date')
    # df_quarterly = df[df.index.month.isin([1, 4, 7, 10])]
    # series = pd.to_numeric(df_quarterly['value'], errors='coerce')
    # df_quarterly['value'] = series
    # df_quarterly.rename(columns={'value':value}, inplace=True)
    with open(f'./resources/comm/{value_api}.json') as json_file:
        data_json = json.load(json_file)
    df = pd.DataFrame(data_json['data'])
    df['date'] = pd.to_datetime(df['date'])
    df = df.sort_values(by='date').set_index('date')
    df_filtered = df[df.index >= '1990-01-01']
    df_quarterly = df_filtered[df_filtered.index.month.isin([1, 4, 7, 10])]
    series = pd.to_numeric(df_quarterly['value'], errors='coerce')
    df_quarterly['value'] = series
    df_quarterly.rename(columns={'value':value}, inplace=True)
    return df_quarterly

def load_X(var1, var2, var3):
    df1 = load_macro_data(var1)
    df2 = load_macro_data(var2)
    df3 = load_macro_data(var3)
    X = pd.concat([df1, df2, df3], axis=1)
    return X