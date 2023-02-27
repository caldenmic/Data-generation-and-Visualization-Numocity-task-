# Importing the files
import numpy as np
import os
from summariser_functions import *

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd

pd.reset_option('all')

years = [2022]
months = ['Janurary', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month_map = {'Janurary': 1, 'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 
    'November': 11, 'December': 12}

path = os.getcwd()

# Summary file names
charge_point_and_station_summary_file_name = 'charge_point_and_station_summary'
weekend_and_weekday_summary_file_name = 'weekend_and_weekday_summary'

for year in years:
    year_directory = os.path.join(path, str(year))
    for month in months:
        month_directory = os.path.join(year_directory, month)
        
        if not os.path.exists(month_directory):
            print(f"{month} directory not present")
            continue
        
        # Initially remove the existing summarised csv files
        try:
            summary_file = pd.read_csv(f"{year}\{month}\{charge_point_and_station_summary_file_name}_{year}_{month}.csv")
            day_to_start_processing = int(summary_file['date'].iloc[-1].split('-')[-1]) + 1
            print(day_to_start_processing)
        except:
            day_to_start_processing = 1
            print(day_to_start_processing)
        
        for day in range(day_to_start_processing, days[month_map[month] - 1] + 1):

            # Load datasets one at a time by their day
            try:
                df_temp = pd.read_csv(f'{year}\{month}\day_{day}.csv')
            except:
                # number_of_days holds the number of daily csv files present in a month's directory excluding the number of summary_files
                number_days_data = len(os.listdir(f'{year}\{month}')) - 2
                print(f"{month} directory has {number_days_data} day/days data")
                break

            # Get cleaned Data Frame
            df_temp = get_cleaned_DataFrame(df_temp)

            # Create multiple summary files
            get_summary(df_temp, get_charge_point_and_station_summary, charge_point_and_station_summary_file_name, year, month)
            get_summary(df_temp, get_weekend_and_weekday_summary, weekend_and_weekday_summary_file_name, year, month, append_weekday_and_weekend_summary_to_csv)