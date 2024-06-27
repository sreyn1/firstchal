import pandas as pd
import re
import matplotlib.pyplot as plt

# Path to your data file
file_path = '/Users/sebastie.reynaud1/Documents/ALGO Assistant/challenge/pipeline/data/ehyd_messstellen_all_nlv/NS-Tagessummen/NS-Tagessummen-100206.csv'
# Define a regular expression pattern to extract date and value
pattern = r'(\d{2}\.\d{2}\.\d{4} \d{2}:\d{2}:\d{2})\s*;\s*([\d,]+)\s*(?:;\s*)?'


# Initialize lists to store extracted data
dates = []
values = []

# Read data from file and extract using regex
with open(file_path, 'r', encoding='latin-1') as file:
    lines = file.readlines()
    for line in lines:
        match = re.search(pattern, line)
        if match:
            dates.append(match.group(1))
            values.append(float(match.group(2).replace(',', '.')))  # Replace comma with dot for float conversion

# Create a DataFrame
df = pd.DataFrame({
    'Timestamp': pd.to_datetime(dates, format='%d.%m.%Y %H:%M:%S'),
    'Value': values
})

# Display the DataFrame
plt.plot(df['Timestamp'], df['Value'], marker='o', linestyle='-', color='b', label='Value')
plt.show()