import xarray as xr
import pandas as pd
import numpy as np

# Load the downloaded ERA5 NetCDF file
ds = xr.open_dataset("../original_data/era5_alentejo.nc")

# Choose the point inside the Alentejo bounding box
lat = 38.5
lon = -7.9

# Select nearest grid point
point = ds.sel(latitude=lat, longitude=lon, method="nearest")

# Convert to DataFrame
df = point.to_dataframe().reset_index()

# Convert temperature from Kelvin to Celsius
df["t2m"] = df["t2m"] - 273.15
df["d2m"] = df["d2m"] - 273.15

# Calculate Relative Humidity (RH) using T and dewpoint
df["rh"] = 100 * (
    np.exp((17.625 * df["d2m"]) / (243.04 + df["d2m"])) /
    np.exp((17.625 * df["t2m"]) / (243.04 + df["t2m"]))
)

# Save processed CSV
df.to_csv("../processed_data/era5_alentejo_full.csv", index=False)

print("CSV created: processed_data/era5_alentejo_full.csv")
