# Importing the files
import pandas as pd
import numpy as np
import os

try:
    os.remove("charge_point_and_station_summary.csv")
    os.remove("charge_point_summary.csv")
    os.remove("charge_station_summary.csv")
except:
    pass

# Process all the files in that month
for i in range(1, 32):
    # Load datasets one at a time by their day
    df_temp = pd.read_csv(f'day_{i}.csv')

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

    if not os.path.exists('charge_point_and_station_summary.csv'):
        charge_point_and_station.to_csv('charge_point_and_station_summary.csv', mode='a', index=False)
    else:
        charge_point_and_station.to_csv('charge_point_and_station_summary.csv', mode='a', index=False, header=False)
    
    if not os.path.exists('charge_point_summary.csv'):
        charge_point_summary.to_csv('charge_point_summary.csv', mode='a', index=False)
    else:
        charge_point_summary.to_csv('charge_point_summary.csv', mode='a', index=False, header=False)
    
    if not os.path.exists('charge_station_summary.csv'):
        charge_station_summary.to_csv('charge_station_summary.csv', mode='a', index=False)
    else:
        charge_station_summary.to_csv('charge_station_summary.csv', mode='a', index=False, header=False)

    if not os.path.exists('weekend_and_weekday_summary.csv'):
        charge_station_summary.to_csv('weekend_and_weekday_summary.csv', mode='a', index=False)
    else:
        charge_station_summary.to_csv('weekend_and_weekday_summary.csv', mode='a', index=False, header=False)