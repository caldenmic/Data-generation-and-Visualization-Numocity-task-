# Importing the files
import pandas as pd
import numpy as np
import os


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

            # Drop unwanted columns
            df_temp.drop(columns=['txn.identifier', 'txn.assetIdentifier', 'txn.authMode', 'txn.amount',
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

            df_temp['Total_amount_charged'] = df_temp['txn.totalAmount'] + df_temp['txn.totalTax']
            df_temp['date'] = df_temp['txn.updatedAtTime'].apply(lambda x: x[:10])
            df_temp['day_of_the_week'] = pd.to_datetime(df_temp['date']).dt.strftime('%A')
            # df_temp['txn.deliveredWh'] = df_temp['txn.deliveredWh'] / 1000

            # Create multiple dataframes suitable for plotting different columns
            charge_point_and_station = df_temp.groupby(['txn.chargeStationCity', 'txn.chargePointId', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
            charge_station_summary = df_temp.groupby(['txn.chargeStationCity', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
            charge_point_summary = df_temp.groupby(['txn.chargePointId', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
            df_weekend_and_weekday = df_temp.groupby(['day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()

            if not os.path.exists(f'{year}\{month}\charge_point_and_station_summary_{year}_{month}.csv'):
                charge_point_and_station.to_csv(f'{year}\{month}\charge_point_and_station_summary_{year}_{month}.csv', mode='a', index=False)
            else:
                charge_point_and_station.to_csv(f'{year}\{month}\charge_point_and_station_summary_{year}_{month}.csv', mode='a', index=False, header=False)
            
            if not os.path.exists(f'{year}\{month}\charge_point_summary_{year}_{month}.csv'):
                charge_point_summary.to_csv(f'{year}\{month}\charge_point_summary_{year}_{month}.csv', mode='a', index=False)
            else:
                charge_point_summary.to_csv(f'{year}\{month}\charge_point_summary_{year}_{month}.csv', mode='a', index=False, header=False)
            
            if not os.path.exists(f'{year}\{month}\charge_station_summary_{year}_{month}.csv'):
                charge_station_summary.to_csv(f'{year}\{month}\charge_station_summary_{year}_{month}.csv', mode='a', index=False)
            else:
                charge_station_summary.to_csv(f'{year}\{month}\charge_station_summary_{year}_{month}.csv', mode='a', index=False, header=False)

            if not os.path.exists(f'{year}\{month}\weekend_and_weekday_summary_{year}_{month}.csv'):
                df_weekend_and_weekday.to_csv(f'{year}\{month}\weekend_and_weekday_summary_{year}_{month}.csv', mode='a', index=False)
            else:
                df_weekend_and_weekday.to_csv(f'{year}\{month}\weekend_and_weekday_summary_{year}_{month}.csv', mode='a', index=False, header=False)