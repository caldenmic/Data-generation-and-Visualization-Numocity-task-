# Importing the files
import warnings
import pandas as pd
import numpy as np
import os

def append_to_csv(file_path, current_summary_data):
    """
    append_to_csv appends the data frame to the csv file if it exists otherwise it creates a new csv file

    :file_path: name of the csv file
    :current_summary_data: Data Frame to be appended to the csv file
    :return: returns nothing
    """ 

    if not os.path.exists(file_path):
        current_summary_data.to_csv(file_path, mode='a', index=False)
    else:
        current_summary_data.to_csv(file_path, mode='a', index=False, header=False)

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

    df['Total_amount_charged'] = df['txn.totalAmount'] - df['txn.totalTax']
    
    df['date'] = df['txn.createdAtTime'].apply(lambda x: x[:10])
    # df['date'] = df['txn.updatedAtTime'].apply(lambda x: x[:10])
    
    df['day_of_the_week'] = pd.to_datetime(df['date']).dt.strftime('%A')
    
    df['txn.deliveredkWh'] = df['txn.deliveredWh'] / 1000
    df.drop(columns=['txn.deliveredWh'], inplace=True)

    return df

def get_charge_point_and_station_summary(df):
    """
    get_charge_point_and_station_summary creates a dataframe which gives the charge point and station summary

    :df: Data Frame to be processed
    :return: returns the charge station and the charge point summary
    """ 

    df = df.groupby(['txn.chargeStationCity', 'txn.chargePointId', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredkWh': 'sum'}).reset_index()
    return df

def get_charge_station_summary(df):
    """
    get_charge_station_summary creates a dataframe which gives the charge station summary

    :df: Data Frame to be processed
    :return: returns the charge station summary
    """ 

    df = df.groupby(['txn.chargeStationCity', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredkWh': 'sum'}).reset_index()
    return df

def get_charge_point_summary(df):
    """
    get_charge_point_summary creates a dataframe which gives the charge point summary

    :df: Data Frame to be processed
    :return: returns the charge point summary
    """ 

    df = df.groupby(['txn.chargePointId', 'date', 'day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredkWh': 'sum'}).reset_index()
    return df

def get_weekend_and_weekday_summary(df):
    """
    get_weekend_and_weekday_summary creates a dataframe which gives the weekend and weekday summary

    :df: Data Frame to be processed
    :return: returns the weekend and weekday summary
    """ 

    df = df.groupby(['day_of_the_week']).agg({'Total_amount_charged': 'sum', 'txn.deliveredkWh': 'sum'}).reset_index()
    return df

def append_weekday_and_weekend_summary_to_csv(file_path, current_summary_data):
    """
    append_weekday_and_weekend_summary_to_csv re-calculates the Total_amount_charges and txn.deliveredkWh for each day of the week
    based on the current day's summary that is given

    :file_path: path of the weekend and weekday trends csv file
    :current_summary_data: Current day's summary data
    :return: returns nothing
    """ 

    if not os.path.exists(file_path):
        current_summary_data.to_csv(file_path, mode='a', index=False)
    else:
        previous_summary_data = pd.read_csv(file_path)

        for i, row in current_summary_data.iterrows():
            if row['day_of_the_week'] in previous_summary_data['day_of_the_week'].values:
                previous_summary_data.loc[previous_summary_data['day_of_the_week'] == row['day_of_the_week'], ['Total_amount_charged', 'txn.deliveredkWh']] += row[['Total_amount_charged', 'txn.deliveredkWh']]
            else:
                with warnings.catch_warnings():
                    warnings.filterwarnings("ignore", category=FutureWarning)
                    previous_summary_data = previous_summary_data.append(row, ignore_index=True)
        previous_summary_data.to_csv(file_path, index=False)

def get_summary(df, summariser_function, summary_file_name, year, month, appending_function):
    """
    get_summary it acts as a general intermediate function to get the summary that is required

    :df: it is the data frame whose summary has to be generated
    :summariser_function: it is a function which takes data frame as the argument and creates summary for that data frame  
    :summary_file_name: gives the name of the summary file
    :year: gives the name of the year's directory
    :month: gives the name of the month's directory
    :appending_function: it is a function used to append data to the summarised csv file
    :return: returns nothing
    """ 

    summarised_data = summariser_function(df)
    appending_function(f'{year}\{month}\{summary_file_name}_{year}_{month}.csv', summarised_data)