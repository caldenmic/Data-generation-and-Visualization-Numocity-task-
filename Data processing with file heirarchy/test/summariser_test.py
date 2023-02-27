import unittest
import numpy as np
import os
import sys
import pandas as pd

sys.path.append(os.getcwd())
from summariser_functions import *

path = os.getcwd()

# Summary file names
charge_point_and_station_summary_file_name = 'charge_point_and_station_summary'
weekend_and_weekday_summary_file_name = 'weekend_and_weekday_summary'

class TestSummariser(unittest.TestCase):

    def setUp(self):
        self.years = [2022]
        self.months = ['Janurary', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        self.days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        self.month_map = {'Janurary': 1, 'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 
            'November': 11, 'December': 12}

    def read_csv_file(self, file_path=None, file_name=None):
        if file_path:
            df_temp = pd.read_csv(file_path)
        elif file_name:
            df_temp = pd.read_csv(file_name)
        return df_temp
    
    def test_dataframe_after_cleaning_not_empty(self):
        file_path = f'test\{self.years[0]}\{self.months[0]}\\test_1.csv'
        
        df_temp = self.read_csv_file(file_path)

        df_temp = get_cleaned_DataFrame(df_temp)

        self.assertTrue(not df_temp.empty)

    def test_dataframe_columns_after_cleaning(self):
        expected_columns = ['txn.chargePointId', 'txn.chargeStationAddress', 'txn.chargeStationName', 'txn.chargeStationCity', 
                            'txn.chargeStationState', 'txn.accountBusinessEntity.address', 'txn.invoicedEndMeter', 'txn.connectorType', 
                            'txn.createdAtTime', 'txn.deliveredMin', 'txn.deliveredWh', 'txn.totalAmount', 'txn.totalTax', 
                            'txn.updatedAtTime', 'txn.stop.atTime', 'inv.amount', 'Total_amount_charged', 'date', 'day_of_the_week']
    
        file_path = f'test\{self.years[0]}\{self.months[0]}\\test_1.csv'
        
        df_temp = self.read_csv_file(file_path)

        df_temp = get_cleaned_DataFrame(df_temp)

        columns_after_cleaning = df_temp.columns

        self.assertEqual(set(columns_after_cleaning), set(expected_columns))

    def delete_summary_file(self, summary_name, year, month):
        try:
            os.remove(f"test\{year}\{month}\\test_{summary_name}_{year}_{month}.csv")
        except:
            pass

    def get_summary(self, df, summary_name):
        if summary_name == charge_point_and_station_summary_file_name:
            return get_charge_point_and_station_summary(df)
        elif summary_name == weekend_and_weekday_summary_file_name:
            return get_weekend_and_weekday_summary(df)
        else:
            raise ValueError(f"Invalid summary name: {summary_name}")

    def create_summary(self, summary_name, year, month, day_to_start_processing, appending_function):
        for day in range(day_to_start_processing, self.days[self.month_map[month] - 1] + 1):
            try:
                df_temp = self.read_csv_file(f'test\{year}\{month}\\test_{day}.csv')
            except:
                # print(f"{month} folder has only {day-1} day/days data")
                return

            df_temp = get_cleaned_DataFrame(df_temp)

            summary = self.get_summary(df_temp, summary_name)
            appending_function(f'test\{year}\{month}\\test_{summary_name}_{year}_{month}.csv', summary)

    def get_day_to_start_processing(self, year, month):
        try:
            summary_file = self.read_csv_file(f"test\{year}\{month}\\test_{charge_point_and_station_summary_file_name}_{year}_{month}.csv")
            day_to_start_processing = int(summary_file['date'].iloc[-1].split('-')[-1]) + 1
        except:
            day_to_start_processing = 1

        return day_to_start_processing
    
    def summary_expected_columns_test(self, summary_name_list, expected_columns_list, appending_function_list):
        for year in self.years:
            year_directory = os.path.join(path, str(year))
            for month in self.months:
                month_directory = os.path.join(year_directory, month)
                
                if not os.path.exists(month_directory):
                    print(f"{month} directory not present")
                    continue

                day_to_start_processing = self.get_day_to_start_processing(year, month)

                for i in range(len(summary_name_list)):
                    self.create_summary(summary_name_list[i], year, month, day_to_start_processing, appending_function_list[i])
                
                for i in range(len(summary_name_list)):
                    summary = pd.read_csv(f'test\{year}\{month}\\test_{summary_name_list[i]}_{year}_{month}.csv')
                    summary_columns = summary.columns
                    self.assertEqual(set(summary_columns), set(expected_columns_list[i]))
                    self.delete_summary_file(summary_name_list[i], year, month)

    def summary_creation_test(self, summary_name_list, appending_function_list):
        for year in self.years:
            year_directory = os.path.join(path, str(year))
            for month in self.months:
                month_directory = os.path.join(year_directory, month)
    
                if not os.path.exists(month_directory):
                    print(f"{month} directory not present")
                    continue
    
                day_to_start_processing = self.get_day_to_start_processing(year, month)

                for i in range(len(summary_name_list)):
                    self.create_summary(summary_name_list[i], year, month, day_to_start_processing, appending_function_list[i])
                
                for i in range(len(summary_name_list)):
                    self.assertTrue(os.path.exists(f'test\{year}\{month}\\test_{summary_name_list[i]}_{year}_{month}.csv'), msg=f"{summary_name_list[i]} created successfully")
                    self.delete_summary_file(summary_name_list[i], year, month)

    def test_summaries_creation(self):
        summary_name_list = [charge_point_and_station_summary_file_name, weekend_and_weekday_summary_file_name]
        appending_function_list = [append_to_csv, append_weekday_and_weekend_summary_to_csv]
        self.summary_creation_test(summary_name_list, appending_function_list)

    def test_summaries_expected_columns(self):
        summary_name_list = [charge_point_and_station_summary_file_name, weekend_and_weekday_summary_file_name]
        expected_columns = [['txn.chargeStationCity', 'txn.chargePointId', 'date', 'day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh'],
                            ['day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']]
        appending_function_list = [append_to_csv, append_weekday_and_weekend_summary_to_csv]
        self.summary_expected_columns_test(summary_name_list, expected_columns, appending_function_list)

    def check_summary_is_equal(self, expected_summary, summary_name, year, month):
        summary = self.read_csv_file(f'test\{year}\{month}\\test_{summary_name}_{year}_{month}.csv')
        summary = summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})
        expected_summary = expected_summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})
        self.assertTrue(summary.equals(expected_summary))
    
    def test_summaries_value(self):
        year = 2022
        month = 'Janurary'
        summary_name_list = [charge_point_and_station_summary_file_name, weekend_and_weekday_summary_file_name]
        appending_function_list = [append_to_csv, append_weekday_and_weekend_summary_to_csv]

        df = pd.DataFrame(data=[['uy26932', '', '', 'Mysore', 'Karnataka', '', '', '', '2022-01-01T03:06:51.000Z', 9, 1467, 3.6, 0.648, '', '', '', 2.952, '2022-01-01', 'Saturday'],
                                ['uy26932', '', '', 'Mysore', 'Karnataka', '', '', '', '2022-01-01T16:05:27.000Z', 9, 1372, 4.77, 0.8586, '', '', '', 3.9114, '2022-01-01', 'Saturday'],
                                ['qw23521', '', '', 'Bangalore', 'Karnataka', '', '', '', '2022-01-01T19:03:42.000Z', 9, 1455, 5.74, 1.0332, '', '', '', 4.7068, '2022-01-01', 'Saturday'],
                                ['uy26932', '', '', 'Mysore', 'Karnataka', '', '', '', '2022-01-02T19:03:42.000Z', 9, 1297, 8.31, 1.4958, '', '', '', 6.8142, '2022-01-02', 'Sunday'],
                                ['ga23521', '', '', 'Bangalore', 'Karnataka', '', '', '', '2022-01-02T19:03:42.000Z', 9, 1001, 2.06, 0.3708, '', '', '', 1.6892, '2022-01-02', 'Sunday'],
                                ['ga23521', '', '', 'Bangalore', 'Karnataka', '', '', '', '2022-01-02T19:03:42.000Z', 9, 1556, 4.47, 0.8046, '', '', '', 3.6654, '2022-01-02', 'Sunday'],
                                ['mq18481', '', '', 'Chennai', 'Tamil Nadu', '', '', '', '2022-01-03T19:03:42.000Z', 9, 1870, 9.69, 1.7442, '', '', '', 7.9458, '2022-01-03', 'Monday'],
                                ['uy26932', '', '', 'Bangalore', 'Karnataka', '', '', '', '2022-01-03T19:03:42.000Z', 9, 1191, 3.52, 0.6336, '', '', '', 2.8864, '2022-01-03', 'Monday']], 
                        columns=['txn.chargePointId', 'txn.chargeStationAddress', 'txn.chargeStationName', 'txn.chargeStationCity',
                        'txn.chargeStationState', 'txn.accountBusinessEntity.address', 'txn.invoicedEndMeter', 'txn.connectorType',
                        'txn.createdAtTime', 'txn.deliveredMin', 'txn.deliveredWh', 'txn.totalAmount', 'txn.totalTax', 
                        'txn.updatedAtTime', 'txn.stop.atTime', 'inv.amount', 'Total_amount_charged', 'date', 'day_of_the_week'])
        
        expected_charge_point_and_station_summary = pd.DataFrame(data=[['Bangalore','qw23521','2022-01-01','Saturday',4.7068,1455], 
                                                    ['Mysore','uy26932','2022-01-01','Saturday',6.8633999999999995,2839], 
                                                    ['Bangalore','ga23521','2022-01-02','Sunday',5.3546,2557],
                                                    ['Mysore','uy26932','2022-01-02','Sunday',6.8142000000000005,1297],
                                                    ['Chennai','mq18481','2022-01-03','Monday',7.9458,1870],
                                                    ['Mysore','uy26932','2022-01-03','Monday',2.8864,1191]], 
                                                    columns=['txn.chargeStationCity','txn.chargePointId','date','day_of_the_week','Total_amount_charged','txn.deliveredWh'])

        expected_weekend_and_weekday_summary = pd.DataFrame(data=[['Saturday',11.5702,4294],
                                                                ['Sunday',12.1688,3854],
                                                                ['Monday',10.8322,3061]],
                                                                columns=['day_of_the_week','Total_amount_charged','txn.deliveredWh'])
        
        day_to_start_processing = self.get_day_to_start_processing(year, month)
        
        for i in range(len(summary_name_list)):
            self.create_summary(summary_name_list[i], year, month, day_to_start_processing, appending_function_list[i])
        
        self.check_summary_is_equal(expected_charge_point_and_station_summary, charge_point_and_station_summary_file_name, year, month)
        self.check_summary_is_equal(expected_weekend_and_weekday_summary, weekend_and_weekday_summary_file_name, year, month)


if __name__ == '__main__':
    unittest.main()