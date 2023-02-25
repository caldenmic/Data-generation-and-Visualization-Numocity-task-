# Importing the files
import pandas as pd
import numpy as np
import os
from summariser_functions import *

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
        
        # Initially remove the existing summarised csv files
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
                continue

            # Get cleaned Data Frame
            df_temp = get_cleaned_DataFrame(df_temp)

            # Create multiple dataframes suitable for plotting different columns
            charge_point_and_station = get_charge_point_and_station_summary(df_temp)
            charge_station_summary = get_charge_station_summary(df_temp)
            charge_point_summary = get_charge_point_summary(df_temp)
            df_weekend_and_weekday = get_weekend_and_weekday_summary(df_temp)

            # Generate csv files with summarise different types of data required
            append_to_csv(f'{year}\{month}\charge_point_and_station_summary_{year}_{month}.csv', charge_point_and_station)
            append_to_csv(f'{year}\{month}\charge_point_summary_{year}_{month}.csv', charge_point_summary)
            append_to_csv(f'{year}\{month}\charge_station_summary_{year}_{month}.csv', charge_station_summary)
            append_to_csv(f'{year}\{month}\weekend_and_weekday_summary_{year}_{month}.csv', df_weekend_and_weekday)