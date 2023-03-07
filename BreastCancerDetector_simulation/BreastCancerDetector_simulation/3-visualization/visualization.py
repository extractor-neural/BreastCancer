import os
from datetime import datetime

import pandas as pd
import numpy as np 
import matplotlib
matplotlib.use('TkAgg', force=True)
import matplotlib.pyplot as plt
import seaborn as sns 
import tkinter as tk


# A dictionary of menu options
menu_options = {
    1: "Display diagnosis count - internal control",
    2: "Display correlation heatmap",
    3: "Exit"
    }


def main():
    
    while(True):
        print_menu()
        option = ''
        try:
            option = int(input('Enter your choice: '))
        except:
            print('Wrong input. Please enter a number ...')
        #Check what choice was entered and act accordingly
        if option == 1:
            display_diagnosis_count()
        elif option == 2:
            display_correlation_heatmap()
        elif option == 3:
            print('Thanks message before exiting')
            exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

def print_menu():
    for key in menu_options.keys():
        print (key, '--', menu_options[key] )

def display_diagnosis_count():
    """Displays the count of benign and malignant diagnosis."""
    request_table = load_rdbms_requests_table()
    fig, ax = plt.subplots(figsize=(8, 5))
    request_table.diagnosis.value_counts().plot(kind="bar", width=0.1, color=["lightgreen", "cornflowerblue"], legend=1, ax=ax)
    ax.set_xlabel("(0 = Benign) (1 = Malignant)", fontsize=12)
    ax.set_ylabel("Count", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.legend(["Benign"], fontsize=12)
    plt.show()

def display_correlation_heatmap():
    """Displays the correlation heatmap."""
    with ScreenDimensions() as sd:
        width= sd.width
        height = sd.height

    # Load and analyze data
    request_table = load_rdbms_requests_table()
    correlation_table = correlation(request_table, 0.8)

    # Plot heatmap if correlation table is not empty
    if not correlation_table.empty:
        px = 1/plt.rcParams['figure.dpi']  # Compute pixel size based on matplotlib DPI setting
        dims = (width*px, height*px)
        fig, ax = plt.subplots(figsize=dims)
        sns.heatmap(correlation_table.corr(), cmap='RdYlBu')
        plt.show()

#def option3():

class ScreenDimensions:
    def __enter__(self):
        # Initialize the object and get the screen dimensions
        self.root = tk.Tk()  # Create a Tk object
        self.width = self.root.winfo_screenwidth()  # Get screen width in pixels
        self.height = self.root.winfo_screenheight()  # Get screen height in pixels
        return self  # Return the ScreenDimensions object to the caller
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Clean up the object when the with statement is exited
        self.root.destroy()  # Destroy the Tk object to free up resources
        
def load_rdbms_requests_table():
    module_path = os.path.dirname(__file__)
    filename = os.path.join(module_path, "../operational_rdbms/requests_table.csv")
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File {filename} not found")
    data = pd.read_csv(filename, sep=",")
    return data


def correlation(dataset, threshold):
#Computes the correlation matrix of the dataset and removes highly correlated columns.
    """Args:
        dataset (pandas.DataFrame): the input dataset.
        threshold (float): the correlation threshold to use for column removal.
    Returns:
        pandas.DataFrame: the dataset with highly correlated columns removed.
    """
    col_corr = set() # Set of all the names of deleted columns
    corr_matrix = dataset.corr()
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if (corr_matrix.iloc[i, j] >= threshold) and (corr_matrix.columns[j] not in col_corr):
                colname = corr_matrix.columns[i] # getting the name of column
                col_corr.add(colname)
                if colname in dataset.columns:
                    del dataset[colname] # deleting the column from the dataset
    return(dataset)



if __name__ == "__main__":
    main()

