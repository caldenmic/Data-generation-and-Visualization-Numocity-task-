import unittest
import pandas as pd
import numpy as np
import os
import sys

sys.path.append(os.getcwd())
from summariser_functions import *

class TestSummariser(unittest.TestCase):
    def test_dataframe_after_cleaning_not_empty(self):
        filename = f'test\\test_1.csv'
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
    
        filename = f'test\\test_1.csv'
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

    def delete_summary_file(self, file_name):
        try:
            os.remove(f"test\\{file_name}.csv")
        except:
            pass

    def create_summary(self, file_name, summary_function):
        try:
            os.remove(f"test\\{file_name}.csv")
        except:
            pass

        for i in range(1, 32):
            try:
                df_temp = pd.read_csv(f'test\\test_{i}.csv')
            except:
                break

            df_temp = get_cleaned_DataFrame(df_temp)

            summary = summary_function(df_temp)

            append_to_csv(f'test\\{file_name}.csv', summary)

    def test_create_charge_point_and_station_point_summary(self):
        self.create_summary('test_charge_point_and_station_summary', get_charge_point_and_station_summary)
        self.assertTrue(os.path.exists('test\\test_charge_point_and_station_summary.csv'))
        self.delete_summary_file('test_charge_point_and_station_summary')

    def test_create_charge_station_summary(self):
        self.create_summary('test_charge_station_summary', get_charge_station_summary)
        self.assertTrue(os.path.exists('test\\test_charge_station_summary.csv'))
        self.delete_summary_file('test_charge_station_summary')

    def test_create_charge_point_summary(self):
        self.create_summary('test_charge_point_summary', get_charge_point_summary)
        self.assertTrue(os.path.exists('test\\test_charge_point_summary.csv'))
        self.delete_summary_file('test_charge_point_summary')

    def test_weekend_and_weekday_summary(self):
        self.create_summary('test_weekend_and_weekday_summary', get_weekend_and_weekday_summary)
        self.assertTrue(os.path.exists('test\\test_weekend_and_weekday_summary.csv'))
        self.delete_summary_file('test_weekend_and_weekday_summary')

    def test_charge_point_and_station_summary_expected_columns(self):
        expected_columns = ['txn.chargeStationCity', 'txn.chargePointId', 'date', 'day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']
        self.create_summary('test_charge_point_and_station_summary', get_charge_point_and_station_summary)
        summary = pd.read_csv('test\\test_charge_point_and_station_summary.csv')
        summary_columns = summary.columns
        self.assertEqual(set(summary_columns), set(expected_columns))
        self.delete_summary_file('test_charge_point_and_station_summary')

    def test_charge_station_summary_expected_columns(self):
        expected_columns = ['txn.chargeStationCity', 'date', 'day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']
        self.create_summary('test_charge_station_summary', get_charge_station_summary)
        summary = pd.read_csv('test\\test_charge_station_summary.csv')
        summary_columns = summary.columns
        self.assertEqual(set(summary_columns), set(expected_columns))
        self.delete_summary_file('test_charge_station_summary')

    def test_charge_point_summary_expected_columns(self):
        expected_columns = ['txn.chargePointId', 'date', 'day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']
        self.create_summary('test_charge_point_summary', get_charge_point_summary)
        summary = pd.read_csv('test\\test_charge_point_summary.csv')
        summary_columns = summary.columns
        self.assertEqual(set(summary_columns), set(expected_columns))
        self.delete_summary_file('test_charge_point_summary')

    def test_weekend_and_weekday_expected_columns(self):
        expected_columns = ['day_of_the_week', 'Total_amount_charged', 'txn.deliveredWh']
        self.create_summary('test_weekend_and_weekday_summary', get_weekend_and_weekday_summary)
        summary = pd.read_csv('test\\test_weekend_and_weekday_summary.csv')
        summary_columns = summary.columns
        self.assertEqual(set(summary_columns), set(expected_columns))
        self.delete_summary_file('test_weekend_and_weekday_summary')

    def test_charge_point_and_station_summary_values(self):
        self.create_summary('test_charge_point_and_station_summary', get_charge_point_and_station_summary)

        df_test = pd.DataFrame()
        for i in range(1, 32):
            df_temp = pd.DataFrame()
            try:
                df_temp = pd.read_csv(f'test\\test_{i}.csv')
            except:
                pass

            df_test = pd.concat([df_test, df_temp])

        df_test = get_cleaned_DataFrame(df_test)

        summary = get_charge_point_and_station_summary(df_test)
        summary = summary.sort_values('date').reset_index().drop(columns=['index'])
        summary = summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})

        expected_summary = pd.read_csv("test\\test_charge_point_and_station_summary.csv")
        expected_summary = expected_summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})

        self.assertTrue(summary.equals(expected_summary))

        self.delete_summary_file("test_charge_point_and_station_summary")

    def test_charge_station_summary_values(self):
        self.create_summary('test_charge_station_summary', get_charge_station_summary)

        df_test = pd.DataFrame()
        for i in range(1, 32):
            df_temp = pd.DataFrame()
            try:
                df_temp = pd.read_csv(f'test\\test_{i}.csv')
            except:
                pass

            df_test = pd.concat([df_test, df_temp])

        df_test = get_cleaned_DataFrame(df_test)

        summary = get_charge_station_summary(df_test)
        summary = summary.sort_values('date').reset_index().drop(columns=['index'])
        summary = summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})

        expected_summary = pd.read_csv("test\\test_charge_station_summary.csv")
        expected_summary = expected_summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})

        self.assertTrue(summary.equals(expected_summary))

        self.delete_summary_file("test_charge_station_summary")

    def test_charge_point_summary_values(self):
        self.create_summary('test_charge_point_summary', get_charge_point_summary)

        df_test = pd.DataFrame()
        for i in range(1, 32):
            df_temp = pd.DataFrame()
            try:
                df_temp = pd.read_csv(f'test\\test_{i}.csv')
            except:
                pass

            df_test = pd.concat([df_test, df_temp])

        df_test = get_cleaned_DataFrame(df_test)

        summary = get_charge_point_summary(df_test)
        summary = summary.sort_values('date').reset_index().drop(columns=['index'])
        summary = summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})

        expected_summary = pd.read_csv("test\\test_charge_point_summary.csv")
        expected_summary = expected_summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})

        self.assertTrue(summary.equals(expected_summary))

        self.delete_summary_file("test_charge_point_summary")

    def test_weekend_and_weekday_summary_values(self):
        self.create_summary('test_weekend_and_weekday_summary', get_weekend_and_weekday_summary)

        df_test = pd.DataFrame()
        for i in range(1, 32):
            df_temp = pd.DataFrame()
            try:
                df_temp = pd.read_csv(f'test\\test_{i}.csv')
            except:
                pass

            df_test = pd.concat([df_test, df_temp])

        df_test = get_cleaned_DataFrame(df_test)

        summary = get_weekend_and_weekday_summary(df_test)
        summary = summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})

        expected_summary = pd.read_csv("test\\test_weekend_and_weekday_summary.csv")
        expected_summary = expected_summary.sort_values('day_of_the_week').reset_index().drop(columns=['index'])
        expected_summary = expected_summary.round({'Total_amount_charged': 10, 'txn.deliveredWh': 10})

        self.assertTrue(summary.equals(expected_summary))

        self.delete_summary_file("test_weekend_and_weekday_summary")

if __name__ == '__main__':
    unittest.main()




