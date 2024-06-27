import os
import re
import pandas as pd

# Folder path containing the text files
folder_path = '/Users/sebastie.reynaud1/Documents/ALGO Assistant/challenge/pipeline/data/ehyd_messstellen_all_gw/Grundwasserstand-Monatsmittel/'
pattern = r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})\s*;\s*([\d,]+)\s*;\s*'
filename_pattern = re.compile(r'.*-(\d+)\.csv')

# List to store DataFrames
data = []

# List to store extracted numbers
file_numbers = []

# Iterate over files in the folder
for filename in sorted(os.listdir(folder_path)):
    dates = []
    values = []
    if filename.endswith('.csv'):  # Ensure we only process CSV files
        # Extract the number before .csv using regex
        match = filename_pattern.match(filename)
        if match:
            file_number = int(match.group(1))
            file_numbers.append(file_number)

            file_path = os.path.join(folder_path, filename)
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
            data.append(df)

# Print the list of file numbers
print(file_numbers)

# Example usage: accessing the DataFrame of the first file
if data:
    print(data[0].head())

# Now 'data' contains all the DataFrames, and 'file_numbers' contains the extracted numbers
