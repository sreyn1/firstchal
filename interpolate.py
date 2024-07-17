import numpy as np
import pandas as pd

from utils import get_data_from_csv
import darts
import os
from darts import TimeSeries
from darts.dataprocessing.transformers import Scaler
from darts.utils.statistics import plot_ccf
import matplotlib.pyplot as plt

print("helllo")
# Dictionnaries for the data

GrundwasserstandMonatsmittel_dict = {}
GrundwassertemperaturMonatsmittel = {}

# Load data from all folders
folder="ehyd_messstellen_all_gw"
print(os.path.isdir(os.path.join("data", folder)))
if os.path.isdir(os.path.join("data", folder)):
    GrundwasserstandMonatsmittel_dict = get_data_from_csv(
        os.path.join("data", folder, "Grundwasserstand-Monatsmittel"))


bad_keys_count = 0

for key in GrundwasserstandMonatsmittel_dict:
    try:
        GrundwasserstandMonatsmittel_dict[key] = darts.TimeSeries.from_dataframe(GrundwasserstandMonatsmittel_dict[key],
                                                                                 'Timestamp', 'Value',
                                                                                 fill_missing_dates=True, freq='MS')
    except ValueError:
        print(f"Cannot infer the frequency for {key} with GrundwasserstandMonatsmittel_dict")
        bad_keys_count += 1

ts1= GrundwasserstandMonatsmittel_dict[304063]

ts2=GrundwasserstandMonatsmittel_dict[303925]


ts1.plot()
ts2.plot()
plt.show()
# Find the common time range
common_start = max(ts1.start_time(), ts2.start_time())
common_end = min(ts1.end_time(), ts2.end_time())

# Truncate both series to the common time range
ts1_common = ts1.slice(common_start, common_end)
ts2_common = ts2.slice(common_start, common_end)

plot_ccf(ts1_common,ts2_common)
plt.show()
# def compute_correlation_matrix(series_dict):
#     keys = list(series_dict.keys())
#     n = len(keys)
#     corr_matrix = pd.DataFrame(np.zeros((n, n)), index=keys, columns=keys)
#
#     for i in range(n):
#         for j in range(i, n):
#             if i == j:
#                 corr = 1.0
#             else:
#                 series1 = series_dict[keys[i]]
#                 series2 = series_dict[keys[j]]
#                 corr = pearsonr(series1, series2)
#             corr_matrix.iloc[i, j] = corr
#             corr_matrix.iloc[j, i] = corr
#
#     return corr_matrix