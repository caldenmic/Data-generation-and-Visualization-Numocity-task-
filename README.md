# Data-generation-and-Visualization-Numocity-task-
Generate fake data on the charging summary given in the csv_summary_30.csv file and visualize the results

This project has two folders one which summarises data following a heirarchial file structure of year->month->day and the other folder which just summarises the files in the root directory.
- If data has to be generated run the data_generator.py
- To summarise the generated data run the csv_summariser.py
- The test runner and test data is contained in the "test" directory. Unit test are contained within the summariser_test.py executing this file will run all the unit tests


### NOTE: While summarising the data "createAtTime" is considered for now instead of "uploadAtTime" for the "date" column due to a special case which arises when the creationAtTime is close to approaching the next day which causes the uploadAtTime to go to the next day this results in duplicate rows for date in the summary csv files.