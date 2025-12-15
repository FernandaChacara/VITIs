import xarray as xr
import pandas as pd
import numpy as np

# Open the two real NetCDF files extracted from the ZIP
ds_inst = xr.open_dataset("../original_data/data_stream-oper_stepType-instant.nc")
ds_acc  = xr.open_dataset("../original_data/data_stream-oper_stepType-accum.nc")

# Merge instant + accumulated variables
ds = xr.merge([ds_inst, ds_acc])

# Choose a point in Alentejo
lat = 38.5
lon = -7.9

# Select nearest grid point
point = ds.sel(latitude=lat, longitude=lon, method="nearest")

# Convert to DataFrame
df = point.to_dataframe().reset_index()

# Convert temperatures from Kelvin to Celsius
if "t2m" in df.columns:
    df["t2m"] = df["t2m"] - 273.15
if "d2m" in df.columns:
    df["d2m"] = df["d2m"] - 273.15

# Compute Relative Humidity if possible
if {"t2m", "d2m"}.issubset(df.columns):
    df["rh"] = 100 * (
        np.exp((17.625 * df["d2m"]) / (243.04 + df["d2m"])) /
        np.exp((17.625 * df["t2m"]) / (243.04 + df["t2m"]))
    )

# Save CSV
df.to_csv("../processed_data/era5_alentejo_full.csv", index=False)

print("CSV created: processed_data/era5_alentejo_full.csv")
