import math
import os
import re

import pandas as pd

path_snow = '/Users/sebastie.reynaud1/Documents/ALGO Assistant/challenge/pipeline/data/ehyd_messstellen_all_nlv/NS-Tagessummen'
path_rain = '/Users/sebastie.reynaud1/Documents/ALGO Assistant/challenge/pipeline/data/ehyd_messstellen_all_nlv/N-Tagessummen'


def get_closest_niederschalgs_df(gw_id : int, max_dist : float) :

    rain_df_list, rain_id = get_data_from_csv_list(path_rain)
    snow_df_list, snow_id = get_data_from_csv_list(path_snow)
    rain_df_list_filtered, snow_df_list_filtered  = [],[]
    rain_id_filtered, snow_id_filtered = [], []
    for (ix, id) in enumerate(rain_id):
        if distance(gw_id, id) < max_dist:
            rain_df_list_filtered.append(rain_df_list[ix])
            rain_id_filtered.append(id)

    for (ix, id) in enumerate(snow_id):
        if distance(gw_id, id) < max_dist:
            snow_df_list_filtered.append(rain_df_list[ix])
            snow_id_filtered.append(id)

    return (rain_df_list_filtered, rain_id_filtered, snow_df_list_filtered, snow_id_filtered)


def getxy(id,messtype):
    if messtype=="groundwater":
        file_path = '/Users/sebastie.reynaud1/Documents/ALGO Assistant/challenge/pipeline/data/ehyd_messstellen_all_gw/messstellen_alle.csv'
    if messtype == "precipitation" :
        file_path = '/Users/sebastie.reynaud1/Documents/ALGO Assistant/challenge/pipeline/data/ehyd_messstellen_all_nlv/messstellen_alle.csv'

    xlist = []
    ylist = []
    with open(file_path, 'r', encoding='latin-1') as file:
        next(file)
        found = False
        for line in file:
            # Split the line into columns based on semicolons
            columns = line.strip().split(';')

            # Check if there are at least four columns and the fourth column matches x
            xlist.append(float(columns[0].replace(',', '.')))
            ylist.append(float(columns[1].replace(',', '.')))
            if int(columns[3]) == id:
                found_line = line.strip()
                found = True
                break
        if found:
            return (float(columns[0].replace(',', '.')),float(columns[1].replace(',', '.')))
        else:
            print(f"'{id}' not found in any line.")
        return None, None

def get_data_from_csv_list(path):

    # Define a regular expression pattern to extract date and value
    pattern = r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})\s*;\s*([\d,]+)\s*(?:;\s*)?'
    filename_pattern = re.compile(r'.*-(\d+)\.csv')
    # List to store DataFrames
    df_list = []

    # List to store extracted numbers
    file_numbers = []

    # Iterate over files in the folder
    for filename in sorted(os.listdir(path)):
        dates = []
        values = []
        if filename.endswith('.csv'):  # Ensure we only process CSV files
            # Extract the number before .csv using regex
            match = filename_pattern.match(filename)
            if match:
                file_number = int(match.group(1))
                file_numbers.append(file_number)

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
                df_list.append(df)
    return  df_list, file_numbers

def distance(id_gw, id_ns):
    x_gw, y_gw = getxy(id_gw, "groundwater")
    x_ns, y_ns = getxy(id_ns, "precipitation")
    return math.sqrt((x_gw-x_ns)**2+(y_ns-y_gw)**2)


raindf, rainid, snowdf, snowid = get_closest_niederschalgs_df(300012,1e4)

print(rainid, snowid)