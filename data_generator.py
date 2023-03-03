# Importing the files
import pandas as pd
import numpy as np
import random
import datetime
from faker import Faker
from faker.providers.phone_number import Provider
import os

# Initializing the faker inctance
fake = Faker()

class IndiaPhoneNumberProvider(Provider):
    def india_phone_number(self):
        return f'{self.msisdn()[3:]}'

fake.add_provider(IndiaPhoneNumberProvider)

def generate_gstn():
    state_codes = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '96', '97']
    state_code = random.choice(state_codes)
    pan_number = generate_pan()
    check_digit = str(random.randint(0, 9))
    two_letters = fake.random_letters(length=2)
    gstn = state_code + pan_number + check_digit + "".join(two_letters).upper()
    return gstn

def generate_pan():
    five_letters = fake.random_letters(length=5)
    first_9_digits = "".join(five_letters).upper() + str(fake.random_number(digits=4))
    entity_types = ['P', 'C', 'F', 'L', 'T', 'N', 'R', 'E', 'J', 'G', 'H', 'K', 'A', 'B', 'Z', 'S', 'Y', 'D']
    entity_type = random.choice(entity_types)
    pan_number = first_9_digits + entity_type
    return pan_number

def get_random_time_of_the_day(day, month, year):
    fake_date = datetime.date(year, month, day)
    fake_time_str = fake.time()
    fake_time = datetime.datetime.strptime(fake_time_str, '%H:%M:%S').time()
    fake_datetime = datetime.datetime.combine(fake_date, fake_time)
    fake_datetime = fake_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return fake_datetime

def get_random_datetime():
    random_datetime = fake.date_time_this_year()
    datetime_string = random_datetime.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return datetime_string

def get_random_value(lower_limit, upper_limit, multiplier = 1, round_off_digits = 2):
    return round(random.uniform(lower_limit, upper_limit) * multiplier, round_off_digits)

def get_random_integer(lower_limit, upper_limit, multiplier = 1):
    return round(random.uniform(lower_limit, upper_limit) * multiplier)

def get_asset_id():
    five_letters = fake.random_letters(length=4)
    two_letters = fake.random_letters(length=2)
    five_numbers = str(fake.random.randint(10000, 100000))
    return '/' + "".join(five_letters).lower() + '/' + "".join(two_letters).lower() + five_numbers

def get_random_id_all_numbers(length = 5):
    return fake.random.randint(10**(length-1), 10**length)

def get_changed_time(date_and_time, minutes, seconds=0):
    dt = datetime.datetime.fromisoformat(date_and_time[:-1])
    dt += datetime.timedelta(minutes=minutes, seconds=seconds)
    changed_time_and_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'
    return changed_time_and_date

def get_invoice_identifier():
    company_abbreviation = 'NMC'
    five_digits = str(fake.random.randint(10000, 100000))
    eight_digits = str(fake.random.randint(10000000, 100000000))
    return company_abbreviation + "_" + five_digits + "_" + eight_digits

def get_type(item_list):
    item = random.choice(item_list)
    return item

# def get_charge_station_name():
#     three_letters = fake.random_letters(length=3)
#     return "".join(three_letters).lower() + str(random.randint(1, 10))

charge_point_to_station_map = {'/xlss/yt26932': 'sdg5', '/osrw/mq18481': 'hmk7', '/fews/qw23521': 'sft4', '/fhtl/uy26932': 'sdg5', '/lknr/op18481': 'hmk7', '/nsid/ga23521': 'sft4'}
charge_station_city_dict = {'sdg5': 'Mysore', 'hmk7': 'Chennai', 'sft4': 'Bangalore'}
charge_station_state_dict = {'Bangalore': 'Karnataka', 'Mysore': 'Karnataka', 'Chennai': 'Tamil Nadu'}


years = [2022]
months = ['Janurary', 'Feburary', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
month_map = {'Janurary': 1, 'Feburary': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6, 'July': 7, 'August': 8, 'September': 9, 'October': 10, 
    'November': 11, 'December': 12}


path = os.getcwd()

for year in years:
    year_directory = os.path.join(path, str(year))
    try: 
        os.mkdir(year_directory) 
    except OSError as error: 
        print(error)
    
    for month in months:
        month_directory = os.path.join(year_directory, month)
        try: 
            os.mkdir(month_directory) 
        except OSError as error: 
            print(error)
        
        for day in range(1, days[month_map[month] - 1] + 1):
            df = pd.read_csv('csv_summary_30.csv')
            for i in range(random.randint(10, 50)):
                txn_id = fake.uuid4()
                asset_id = get_type(['/xlss/yt26932', '/osrw/mq18481', '/fews/qw23521', '/fhtl/uy26932', '/lknr/op18481', '/nsid/ga23521'])
                auth_mode = random.choice(["RFID", "APP"])
                amount = get_random_value(1, 10, round_off_digits=2)
                charge_point_id = asset_id[6:]
                charge_station_address = fake.address()
                charge_station_name = charge_point_to_station_map[asset_id]
                charge_station_city = charge_station_city_dict[charge_station_name]
                charge_station_state = charge_station_state_dict[charge_station_city]
                bussiness_entity_address = get_type(['Banglore', 'Kolkata', 'Delhi', 'Chennai', 'Mumbai', 'Ranchi'])
                account_bussiness_entity_gstn = generate_gstn()
                account_bussiness_entity_pan = generate_pan()
                invoiced_end_meter = get_random_integer(1, 2, 1000)
                start_at_time = np.NaN
                connector_id = round(random.randint(1, 3))
                connector_type = get_type(['Type 1', 'Type 2'])
                creation_at_time = get_random_time_of_the_day(day, month_map[month], year)
                tags = np.NaN
                delivered_min = get_random_value(0.1, 0.2, 10, 2)
                delivered_wh = get_random_integer(0.5, 1, 2000)
                id_tag = get_type(['DEVA-TEST'])
                numo_type = asset_id[1:5]
                services_0_name = np.NaN
                services_0_currency = np.NaN
                services_0_type = get_type(['energyInkWh'])
                services_0_rate = get_random_integer(4, 8)
                services_0_taxinfo_0_value = 18 # 18% tax
                services_0_taxinfo_0_name = get_type(['GST'])
                services_0_taxinfo_0_tax_amount = get_random_value(0.5, 0.99, round_off_digits=3)
                services_0_taxinfo_1_value = np.NaN
                services_0_taxinfo_1_name = np.NaN
                services_0_taxinfo_1_tax_amount = np.NaN
                services_0_amount = amount
                services_0_tax_amount = services_0_amount * (services_0_taxinfo_0_value / 100)
                services_0_total = round(services_0_amount + services_0_tax_amount, 3)
                services_1_name = np.NaN
                services_1_currency = np.NaN
                services_1_type = get_type(["serviceFee"])
                services_1_rate = 0
                services_1_taxinfo_0_value = 18 # 18% tax
                services_1_taxinfo_0_name = get_type(['GST'])
                services_1_taxinfo_0_tax_amount = 0
                services_1_taxinfo_1_value = 0
                services_1_taxinfo_1_name = 0
                services_1_taxinfo_1_tax_amount = 0
                services_1_amount = 0
                services_1_tax_amount = services_1_amount * (services_1_taxinfo_0_value / 100)
                services_1_total = round(services_1_amount + services_1_tax_amount, 3)
                session_id = txn_id
                session_type = get_type(['charging'])
                station_bussiness_entity_GST = np.NaN
                station_bussiness_entity_PAN = np.NaN
                station_bussiness_entity_address = np.NaN
                support_email = fake.ascii_free_email()
                support_number = fake.india_phone_number()
                total_amount = services_0_amount + services_1_amount
                total_tax = services_0_tax_amount + services_1_tax_amount
                transaction_id = get_random_id_all_numbers(8)
                stop_at_time = get_changed_time(creation_at_time, 2)
                updated_at_time = get_changed_time(stop_at_time, 0, 1)
                stop_request_at_time = np.NaN
                stop_request_target = np.NaN
                stop_request_req = np.NaN
                stop_request_session_id = np.NaN
                stop_request_origin = np.NaN
                stop_request_reason = np.NaN
                stop_request_message_id = np.NaN
                charge_station_id = get_random_integer(1, 10)
                invoice_identifier = get_invoice_identifier()
                invoice_account_id = fake.uuid4()
                invoice_amount = np.NaN
                invoice_currency = get_type(['INR'])
                invoice_description = 'Charging Summary'
                invoice_entry_type = get_type(['debit'])
                invoice_username = fake.user_name()
                invoice_success = get_type(['success'])
                invoice_type = get_type(['chargeIntimation'])

                df.loc[len(df)] = [
                txn_id, asset_id, auth_mode, amount, charge_point_id, charge_station_address, charge_station_name, charge_station_city, charge_station_state,
                bussiness_entity_address, account_bussiness_entity_gstn, account_bussiness_entity_pan, invoiced_end_meter, start_at_time, connector_id, 
                connector_type, creation_at_time, tags, delivered_min, delivered_wh, id_tag, numo_type, services_0_name, services_0_currency, services_0_type, 
                services_0_rate, services_0_taxinfo_0_value, services_0_taxinfo_0_name, services_0_taxinfo_0_tax_amount, services_0_taxinfo_1_value,
                services_0_taxinfo_1_name, services_0_taxinfo_1_tax_amount, services_0_amount, services_0_tax_amount, services_0_total, services_1_name, 
                services_1_currency, services_1_type, services_1_rate, services_1_taxinfo_0_value, services_1_taxinfo_0_name, services_1_taxinfo_0_tax_amount, 
                services_1_taxinfo_1_value, services_1_taxinfo_1_name, services_1_taxinfo_1_tax_amount, services_1_amount, services_1_tax_amount,
                services_1_total, session_id, session_type, station_bussiness_entity_GST, station_bussiness_entity_PAN, station_bussiness_entity_address,
                support_email, support_number, total_amount, total_tax, transaction_id, updated_at_time, stop_at_time, stop_request_at_time, stop_request_target,
                stop_request_req, stop_request_session_id, stop_request_origin, stop_request_reason, stop_request_message_id, charge_station_id, invoice_identifier,
                invoice_account_id, invoice_amount, invoice_currency, invoice_description, invoice_entry_type, invoice_username, invoice_success, invoice_type
                ]

            # create csv file for the particular day

            df[1:].to_csv(f'{year}\{month}\day_{day}.csv', index=False)