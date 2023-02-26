import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.getcwd())
from summariser_functions import *

years = [2022]
months = ['Janurary', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month_map = {'Janurary': 1, 'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 
    'November': 11, 'December': 12}

path = os.getcwd()

class TestSummariser(unittest.TestCase):
    def test_dataframe_after_cleaning_not_empty(self):
        filename = f'test\{years[0]}\{months[0]}\\test_1.csv'
        try:
            df_temp = pd.read_csv(filename)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError:
            print(f"Error: Unable to read file '{filename}'.")
        except Exception as e:
            print(f"Error: {e}")

        df_temp = get_cleaned_DataFrame(df_temp)

        self.assertTrue(not df_temp.empty)

    def test_dataframe_columns_after_cleaning(self):
        expected_columns = ['txn.chargePointId', 'txn.chargeStationAddress', 'txn.chargeStationName', 'txn.chargeStationCity', 
                            'txn.chargeStationState', 'txn.accountBusinessEntity.address', 'txn.invoicedEndMeter', 'txn.connectorType', 
                            'txn.createdAtTime', 'txn.deliveredMin', 'txn.deliveredWh', 'txn.totalAmount', 'txn.totalTax', 
                            'txn.updatedAtTime', 'txn.stop.atTime', 'inv.amount', 'Total_amount_charged', 'date', 'day_of_the_week']
    
        filename = f'test\{years[0]}\{months[0]}\\test_1.csv'
        try:
            df_temp = pd.read_csv(filename)
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
        except IOError:
            print(f"Error: Unable to read file '{filename}'.")
        except Exception as e:
            print(f"Error: {e}")

        df_temp = get_cleaned_DataFrame(df_temp)

        columns_after_cleaning = df_temp.columns

        self.assertEqual(set(columns_after_cleaning), set(expected_columns))

    def delete_summary_file(self, file_name, year, month):
        try:
            os.remove(f"test\{year}\{month}\{file_name}.csv")
        except:
            pass

    def create_summary(self, file_name, year, month, summary_function):
        try:
            os.remove(f"test\{year}\{month}\{file_name}.csv")
        except:
            pass

        for day in range(1, days[month_map[month] - 1] + 1):
            try:
                df_temp = pd.read_csv(f'test\{year}\{month}\\test_{day}.csv')
            except:
                continue

            df_temp = get_cleaned_DataFrame(df_temp)

            summary = summary_function(df_temp)

            append_to_csv(f'test\{year}\{month}\{file_name}.csv', summary)

    def test_create_charge_station_and_charge_point_summary(self):
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)

                self.create_summary('test_charge_point_and_station_summary', year, month, get_charge_point_and_station_summary)
                self.assertTrue(os.path.exists(f'test\{year}\{month}\\test_charge_point_and_station_summary.csv'))
                self.delete_summary_file('test_charge_point_and_station_summary', year, month)

    def test_create_charge_station_summary(self):
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)

                self.create_summary('test_charge_station_summary', year, month, get_charge_station_summary)
                self.assertTrue(os.path.exists(f'test\{year}\{month}\\test_charge_station_summary.csv'))
                self.delete_summary_file('test_charge_station_summary', year, month)

    def test_create_charge_point_summary(self):
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)

                self.create_summary('test_charge_point_summary', year, month, get_charge_point_summary)
                self.assertTrue(os.path.exists(f'test\{year}\{month}\\test_charge_point_summary.csv'))
                self.delete_summary_file('test_charge_point_summary', year, month)

    def test_create_weekend_and_weekday_summary(self):
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)

                self.create_summary('test_weekend_and_weekday_summary', year, month, get_weekend_and_weekday_summary)
                self.assertTrue(os.path.exists(f'test\{year}\{month}\\test_weekend_and_weekday_summary.csv'))
                self.delete_summary_file('test_weekend_and_weekday_summary', year, month)

    def test_charge_point_and_station_summary_expected_columns(self):
        expected_columns = ['txn.chargeStationCity', 'txn.chargePointId', 'date', 'day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']
        
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)

                self.create_summary('test_charge_point_and_station_summary', year, month, get_charge_point_and_station_summary)
                summary = pd.read_csv(f'test\{year}\{month}\\test_charge_point_and_station_summary.csv')
                summary_columns = summary.columns
                self.assertEqual(set(summary_columns), set(expected_columns))
                self.delete_summary_file('test_charge_point_and_station_summary', year, month)

    def test_charge_station_summary_expected_columns(self):
        expected_columns = ['txn.chargeStationCity', 'date', 'day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']
        
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)

                self.create_summary('test_charge_station_summary', year, month, get_charge_station_summary)
                summary = pd.read_csv(f'test\{year}\{month}\\test_charge_station_summary.csv')
                summary_columns = summary.columns
                self.assertEqual(set(summary_columns), set(expected_columns))
                self.delete_summary_file('test_charge_station_summary', year, month)

    def test_charge_point_summary_expected_columns(self):
        expected_columns = ['txn.chargePointId', 'date', 'day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)

                self.create_summary('test_charge_point_summary', year, month, get_charge_point_summary)
                summary = pd.read_csv(f'test\{year}\{month}\\test_charge_point_summary.csv')
                summary_columns = summary.columns
                self.assertEqual(set(summary_columns), set(expected_columns))
                self.delete_summary_file('test_charge_point_summary', year, month)

    def test_weekend_and_weekday_expected_columns(self):
        expected_columns = ['day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']
        
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)

                self.create_summary('test_weekend_and_weekday_summary', year, month, get_weekend_and_weekday_summary)
                summary = pd.read_csv(f'test\{year}\{month}\\test_weekend_and_weekday_summary.csv')
                summary_columns = summary.columns
                self.assertEqual(set(summary_columns), set(expected_columns))
                self.delete_summary_file('test_weekend_and_weekday_summary', year, month)

    def test_charge_point_and_station_summary_values(self):
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)
                
                self.create_summary('test_charge_point_and_station_summary', year, month, get_charge_point_and_station_summary)

                df_test = pd.DataFrame()
                for day in range(1, days[month_map[month] - 1] + 1):
                    df_temp = pd.DataFrame()
                    try:
                        df_temp = pd.read_csv(f"test\{year}\{month}\\test_{day}.csv")
                    except:
                        continue

                    df_test = pd.concat([df_test, df_temp])

                df_test = get_cleaned_DataFrame(df_test)

                summary = get_charge_point_and_station_summary(df_test)
                summary = summary.sort_values('date').reset_index().drop(columns=['index'])

                expected_summary = pd.read_csv(f"test\{year}\{month}\\test_charge_point_and_station_summary.csv")

                pd.testing.assert_frame_equal(left=summary, right=expected_summary)

                self.delete_summary_file("test_charge_point_and_station_summary", year, month)

    def test_charge_station_summary_values(self):
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)
                
                self.create_summary('test_charge_station_summary', year, month, get_charge_station_summary)

                df_test = pd.DataFrame()
                for day in range(1, days[month_map[month] - 1] + 1):
                    df_temp = pd.DataFrame()
                    try:
                        df_temp = pd.read_csv(f"test\{year}\{month}\\test_{day}.csv")
                    except:
                        continue

                    df_test = pd.concat([df_test, df_temp])

                df_test = get_cleaned_DataFrame(df_test)

                summary = get_charge_station_summary(df_test)
                summary = summary.sort_values('date').reset_index().drop(columns=['index'])

                expected_summary = pd.read_csv(f"test\{year}\{month}\\test_charge_station_summary.csv")

                pd.testing.assert_frame_equal(left=summary, right=expected_summary)

                self.delete_summary_file("test_charge_station_summary", year, month)

    def test_charge_point_summary_values(self):
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)
                
                self.create_summary('test_charge_point_summary', year, month, get_charge_point_summary)

                df_test = pd.DataFrame()
                for day in range(1, days[month_map[month] - 1] + 1):
                    df_temp = pd.DataFrame()
                    try:
                        df_temp = pd.read_csv(f"test\{year}\{month}\\test_{day}.csv")
                    except:
                        continue

                    df_test = pd.concat([df_test, df_temp])

                df_test = get_cleaned_DataFrame(df_test)

                summary = get_charge_point_summary(df_test)
                summary = summary.sort_values('date').reset_index().drop(columns=['index'])

                expected_summary = pd.read_csv(f"test\{year}\{month}\\test_charge_point_summary.csv")

                pd.testing.assert_frame_equal(left=summary, right=expected_summary)

                self.delete_summary_file("test_charge_point_summary", year, month)

    def test_weekend_and_weekday_summary_values(self):
        for year in years:
            year_directory = os.path.join(path, str(year))
            for month in months:
                month_directory = os.path.join(year_directory, month)
                
                self.create_summary('test_weekend_and_weekday_summary', year, month, get_weekend_and_weekday_summary)

                df_test = pd.DataFrame()
                for day in range(1, days[month_map[month] - 1] + 1):
                    df_temp = pd.DataFrame()
                    try:
                        df_temp = pd.read_csv(f"test\{year}\{month}\\test_{day}.csv")
                    except:
                        continue

                    df_test = pd.concat([df_test, df_temp])

                df_test = get_cleaned_DataFrame(df_test)

                summary = get_weekend_and_weekday_summary(df_test)

                expected_summary = pd.read_csv(f"test\{year}\{month}\\test_weekend_and_weekday_summary.csv")
                expected_summary = expected_summary.sort_values('day_of_the_week').reset_index().drop(columns=['index'])

                pd.testing.assert_frame_equal(left=summary, right=expected_summary)

                self.delete_summary_file("test_weekend_and_weekday_summary", year, month)

if __name__ == '__main__':
    unittest.main()