# Bunch of useful functions for the project

import math
import os
import re

import pandas as pd

def get_data_from_csv(path):
    """
    params:
    path : str : path to the folder containing the CSV files
    returns:
    df_dict : dict : a dictionary containing the DataFrames extracted from the CSV files where the key is the number of the Austrian region
    
    """
    

    # Define a regular expression pattern to extract date and value
    pattern = r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})\s*;\s*([\d,]+)\s*(?:;\s*)?'
    filename_pattern = re.compile(r'.*-(\d+)\.csv')
    
    # Dict to store the dataframe DataFrames
    df_dict = {}
    # Iterate over files in the folder
    for filename in sorted(os.listdir(path)):
        dates = []
        values = []
        if filename.endswith('.csv'):  # Ensure we only process CSV files
            # Extract the number before .csv using regex
            match = filename_pattern.match(filename)
            if match:
                file_number = int(match.group(1))

                file_path = os.path.join(path, filename)
                with open(file_path, 'r', encoding='latin-1') as file:
                    lines = file.readlines()
                    for line in lines:
                        match = re.search(pattern, line)
                        if match:
                            dates.append(match.group(1))
                            values.append(float(match.group(2).replace(',', '.')))

                # Create a DataFrame with the extracted data
                df = pd.DataFrame({
                    'Timestamp': pd.to_datetime(dates, format='%d.%m.%Y %H:%M:%S'),
                    'Value': values
                })

                # Append the DataFrame to the list
                df_dict[file_number] = df
    return  df_dict
