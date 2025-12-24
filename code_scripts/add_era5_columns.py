import pandas as pd

# Load ERA5 data
era5 = pd.read_csv("../processed_data/era5_alentejo.csv")

# Load parcels and data sources
parcels = pd.read_csv("../original_data/parcel.csv")
sources = pd.read_csv("../original_data/data_source.csv")

# Get all parcel IDs
parcel_ids = parcels["id"].tolist()

# Get ERA5 source_id
era5_source_id = sources.loc[
    sources["name"].str.contains("ERA5", case=False),
    "id"
].iloc[0]

# Replicate ERA5 data for each parcel
era5_expanded = pd.concat(
    [era5.assign(parcel_id=pid, source_id=era5_source_id) for pid in parcel_ids],
    ignore_index=True
)

# Rename columns to match database schema
era5_expanded = era5_expanded.rename(columns={
    "observation_time": "observation_time",
    "air_temperature_c": "air_temperature_c",
    "dewpoint_temperature_c": "dewpoint_temperature_c",
    "wind_u_10m": "wind_u_10m",
    "wind_v_10m": "wind_v_10m",
    "precipitation": "precipitation_m",
    "solar_radiation": "solar_radiation_jm2",
    "evaporation": "evaporation_m"
})

# Ensure datetime format
era5_expanded["observation_time"] = pd.to_datetime(
    era5_expanded["observation_time"]
)

# Reorder columns exactly as in SQL table (excluding id)
era5_expanded = era5_expanded[
    [
        "parcel_id",
        "source_id",
        "observation_time",
        "air_temperature_c",
        "dewpoint_temperature_c",
        "relative_humidity_pct" if "relative_humidity_pct" in era5_expanded.columns else None,
        "precipitation_m",
        "solar_radiation_jm2",
        "wind_u_10m",
        "wind_v_10m",
        "evaporation_m"
    ]
].dropna(axis=1, how="all")

# Save structured CSV
era5_expanded.to_csv(
    "../processed_data/era5_alentejo_structured.csv",
    index=False
)