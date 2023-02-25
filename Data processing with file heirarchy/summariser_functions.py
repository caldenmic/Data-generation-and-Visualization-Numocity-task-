# Importing the files
import pandas as pd
import numpy as np
import os

def append_to_csv(file_name, df):
    """
    append_to_csv appends the data frame to the csv file if it exists otherwise it creates a new csv file

    :file_name: name of the csv file
    :df: Data Frame to be appended to the csv file
    :return: returns nothing
    """ 

    if not os.path.exists(file_name):
        df.to_csv(file_name, mode='a', index=False)
    else:
        df.to_csv(file_name, mode='a', index=False, header=False)

def get_cleaned_DataFrame(df):
    """
    get_cleaned_DataFrame removes unwanted columns from the dataframe and creates meaningful columns from the existing columns in the dataframe

    :df: Data Frame to be cleaned
    :return: returns the cleaned Data Frame
    """ 

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
    """
    get_charge_point_and_station_summary creates a dataframe which gives the charge point and station summary

    :df: Data Frame to be processed
    :return: returns the charge station and the charge point summary
    """ 

    df = df.groupby(['txn.chargeStationCity', 'txn.chargePointId', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
    return df

def get_charge_station_summary(df):
    """
    get_charge_station_summary creates a dataframe which gives the charge station summary

    :df: Data Frame to be processed
    :return: returns the charge station summary
    """ 

    df = df.groupby(['txn.chargeStationCity', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
    return df

def get_charge_point_summary(df):
    """
    get_charge_point_summary creates a dataframe which gives the charge point summary

    :df: Data Frame to be processed
    :return: returns the charge point summary
    """ 

    df = df.groupby(['txn.chargePointId', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
    return df

def get_weekend_and_weekday_summary(df):
    """
    get_weekend_and_weekday_summary creates a dataframe which gives the weekend and weekday summary

    :df: Data Frame to be processed
    :return: returns the weekend and weekday summary
    """ 

    df = df.groupby(['day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredWh': 'sum'}).reset_index()
    return df