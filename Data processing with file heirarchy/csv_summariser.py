# Importing the files
import pandas as pd
import numpy as np
import os

def append_to_csv(file_name, df):
    if not os.path.exists(file_name):
        df.to_csv(file_name, mode='a', index=False)
    else:
        df.to_csv(file_name, mode='a', index=False, header=False)

def get_cleaned_DataFrame(df):
    # Drop unwanted columns
    df.drop(columns=['txn.identifier', 'txn.assetIdentifier', 'txn.authMode', 'txn.amount',
    'txn.accountBusinessEntity.gstn', 'txn.accountBusinessEntity.pan', 'txn.start.atTime', 'txn.connectorId', 'txn.tags','txn.idTag', 'txn.numotype',
    'txn.services.0.name', 'txn.services.0.currency', 'txn.services.0.type', 'txn.services.0.rate', 'txn.services.0.taxInfo.0.value',
    'txn.services.0.taxInfo.0.name', 'txn.services.0.taxInfo.0.taxAmount', 'txn.services.0.taxInfo.1.value', 'txn.services.0.taxInfo.1.name',
    'txn.services.0.taxInfo.1.taxAmount', 'txn.services.0.amount', 'txn.services.0.taxAmount', 'txn.services.0.total',
    'txn.services.1.name', 'txn.services.1.currency', 'txn.services.1.type', 'txn.services.1.rate', 'txn.services.1.taxInfo.0.value',
    'txn.services.1.taxInfo.0.name', 'txn.services.1.taxInfo.0.taxAmount', 'txn.services.1.taxInfo.1.value', 'txn.services.1.taxInfo.1.name',
    'txn.services.1.taxInfo.1.taxAmount', 'txn.services.1.amount', 'txn.services.1.taxAmount', 'txn.services.1.total', 'txn.sessionId',
    'txn.sessionType', 'txn.stationBusinessEntity.GST', 'txn.stationBusinessEntity.PAN', 'txn.stationBusinessEntity.Address',
    'txn.supportEmail', 'txn.supportNumber', 'txn.transactionId', 'txn.stopRequest.atTime', 'txn.stopRequest.target', 'txn.stopRequest.request', 
    'txn.stopRequest.sessionId', 'txn.stopRequest.origin', 'txn.stopRequest.reason', 'txn.stopRequest.messageId', 'txn.chargeStationId', 
    'inv.identifier', 'inv.accountId', 'inv.currency', 'inv.description', 'inv.entryType', 'inv.userName', 'inv.status', 'inv.invoiceType'], inplace=True)

    df['Total_amount_charged'] = df['txn.totalAmount'] + df['txn.totalTax']
    df['date'] = df['txn.updatedAtTime'].apply(lambda x: x[:10])
    df['day_of_the_week'] = pd.to_datetime(df['date']).dt.strftime('%A')
    # df['txn.deliveredWh'] = df['txn.deliveredWh'] / 1000

    return df

def get_charge_point_and_station_summary(df):
    df = df.groupby(['txn.chargeStationCity', 'txn.chargePointId', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
    return df

def get_charge_station_summary(df):
    df = df.groupby(['txn.chargeStationCity', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
    return df

def get_charge_point_summary(df):
    df = df.groupby(['txn.chargePointId', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
    return df

def get_weekend_and_weekday_summary(df):
    df = df.groupby(['day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
    return df

years = [2022]
months = ['Janurary', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month_map = {'Janurary': 1, 'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 
    'November': 11, 'December': 12}

path = os.getcwd()

for year in years:
    year_directory = os.path.join(path, str(year))
    for month in months:
        month_directory = os.path.join(year_directory, month)
        
        try:
            os.remove(f"{year}\{month}\charge_point_and_station_summary_{year}_{month}.csv")
            os.remove(f"{year}\{month}\charge_point_summary_{year}_{month}.csv")
            os.remove(f"{year}\{month}\charge_station_summary_{year}_{month}.csv")
            os.remove(f"{year}\{month}\weekend_and_weekday_summary_{year}_{month}.csv")

        except:
            pass
        
        for day in range(1, days[month_map[month] - 1] + 1):
            # Load datasets one at a time by their day
            try:
                df_temp = pd.read_csv(f'{year}\{month}\day_{day}.csv')
            except:
                # print(f'{day}, {month}')
                continue

            df_temp = get_cleaned_DataFrame(df_temp)

            # Create multiple dataframes suitable for plotting different columns
            charge_point_and_station = get_charge_point_and_station_summary(df_temp)
            charge_station_summary = get_charge_station_summary(df_temp)
            charge_point_summary = get_charge_point_summary(df_temp)
            df_weekend_and_weekday = get_weekend_and_weekday_summary(df_temp)

            append_to_csv(f'{year}\{month}\charge_point_and_station_summary_{year}_{month}.csv', charge_point_and_station)
            append_to_csv(f'{year}\{month}\charge_point_summary_{year}_{month}.csv', charge_point_summary)
            append_to_csv(f'{year}\{month}\charge_station_summary_{year}_{month}.csv', charge_station_summary)
            append_to_csv(f'{year}\{month}\weekend_and_weekday_summary_{year}_{month}.csv', df_weekend_and_weekday)