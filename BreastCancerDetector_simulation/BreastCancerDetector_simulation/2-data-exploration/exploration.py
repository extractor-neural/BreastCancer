import os
from datetime import datetime, timedelta

import pandas as pd
import numpy as np



def main():
    while True:
        print_menu()
        option = get_option_choice()
        #Check what choice was entered and act accordingly
        options = {
            1: option1,
            2: option2,
            3: option3,
            4: option4,
            5: exit_program
        }
        if option in options:
            options[option]()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

def print_menu():
    menu_options = {
        1: 'Check for Null Values',
        2: 'Check for Missing Values',
        3: 'Check for Duplicates',
        4: 'Check number of new pacients',
        5: 'Exit'
    }
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def option1():
     request_table = load_rdbms_requests_table()
     print('\nNULL VALUES:\n',request_table.isnull().sum(),'\n')

def option2():
    request_table = load_rdbms_requests_table()
    print("\nMissing Values:\n", request_table.isna().sum(),'\n')

def option3():
    request_table = load_rdbms_requests_table()
    print("\nDuplicated:\n", request_table.duplicated().sum(),'\n')

def option4():
    request_table =  load_rdbms_requests_table()
    request_table['open_date'] = pd.to_datetime(request_table['open_date'], format = '%Y-%m-%d')
    end_date = request_table['open_date'].iloc[-1]
    #Subtract one week from the last_entry datetime object
    start_date = end_date - timedelta(weeks=1)
    
    # Filter the dataframe to include rows only between the start and end dates
    filtered_table = request_table[(request_table['open_date'] >= start_date) & (request_table['open_date'] <= end_date)]

    # Count the number of rows in the filtered dataframe
    num_cases = len(filtered_table)

    print("\nNumber pacients between ",start_date,' and ', end_date, 'is: ',num_cases,'\n')

def exit_program():
    print('Thanks message before exiting')
    exit()

def get_option_choice():
    while True:
        try:
            option = int(input('Enter your choice: '))
            return option
        except ValueError:
            print('Wrong input. Please enter a number ...')

def load_rdbms_requests_table():
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../operational_rdbms/requests_table.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    data = pd.read_csv(filename, sep=",")
    return data


if __name__ == "__main__":
    main()