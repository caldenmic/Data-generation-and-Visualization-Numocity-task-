# Importing the files
import pandas as pd
import numpy as np
import os
from summariser_functions import *

# Initially delete the existing summarised csv files
try:
    os.remove("charge_point_and_station_summary.csv")
    os.remove("charge_point_summary.csv")
    os.remove("charge_station_summary.csv")
    os.remove("weekend_and_weekday_summary.csv")
except:
    pass

# Process all the files one by one
for i in range(1, 32):
    # Load datasets one at a time by their day
    try:
        df_temp = pd.read_csv(f'day_{i}.csv')
    except:
        break

    # Clean the data frame
    df_temp = get_cleaned_DataFrame(df_temp)

    # Create multiple dataframes suitable for plotting different columns
    charge_point_and_station = get_charge_point_and_station_summary(df_temp)
    charge_station_summary = get_charge_station_summary(df_temp)
    charge_point_summary = get_charge_point_summary(df_temp)
    df_weekend_and_weekday = get_weekend_and_weekday_summary(df_temp)

    # Generate summarised csv files
    append_to_csv('charge_point_and_station_summary.csv', charge_point_and_station)
    append_to_csv('charge_point_summary.csv', charge_point_summary)
    append_to_csv('charge_station_summary.csv', charge_station_summary)
    append_to_csv('weekend_and_weekday_summary.csv', df_weekend_and_weekday)