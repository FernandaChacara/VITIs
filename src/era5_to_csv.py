import xarray as xr
import pandas as pd
import numpy as np

# Open extracted ERA5 NetCDF files
ds_inst = xr.open_dataset("../original_data/data_stream-oper_stepType-instant.nc")
ds_acc  = xr.open_dataset("../original_data/data_stream-oper_stepType-accum.nc")

# Merge instant and accumulated variables
ds = xr.merge([ds_inst, ds_acc])

# Fixed point in Alentejo
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

# Compute relative humidity
if {"t2m", "d2m"}.issubset(df.columns):
    df["rh"] = 100 * (
        np.exp((17.625 * df["d2m"]) / (243.04 + df["d2m"])) /
        np.exp((17.625 * df["t2m"]) / (243.04 + df["t2m"]))
    )

# Remove non-informative / redundant columns
df = df.drop(columns=["number", "expver", "latitude", "longitude"], errors="ignore")

# Rename columns to meaningful names
df = df.rename(columns={
    "valid_time": "observation_time",
    "t2m": "air_temperature_c",
    "d2m": "dewpoint_temperature_c",
    "u10": "wind_u_10m",
    "v10": "wind_v_10m",
    "tp": "precipitation_m",
    "ssrd": "solar_radiation_jm2",
    "e": "evaporation_m",
    "rh": "relative_humidity_pct"
})

# Save cleaned CSV ready for database import
df.to_csv("../processed_data/era5_alentejo.csv", index=False)

print("Clean CSV created: processed_data/era5_alentejo.csv")

