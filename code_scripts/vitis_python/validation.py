import pandas as pd

# =========================================================
# Validation
# =========================================================

def validate_ndvi_data(df):
    if not {"parcel_id", "observation_date", "ndvi_mean"}.issubset(df.columns):
        raise ValueError("NDVI missing required columns.")


def validate_climate_data(df):
    if not {"parcel_id", "date", "air_temperature_c", "precipitation_m"}.issubset(df.columns):
        raise ValueError("Climate data missing required columns.")

    df.loc[df["air_temperature_c"] < -30, "air_temperature_c"] = pd.NA
    df.loc[df["air_temperature_c"] > 60, "air_temperature_c"] = pd.NA
    df.loc[df["precipitation_m"] < 0, "precipitation_m"] = pd.NA


def validate_parcel_data(df):
    if "id" not in df.columns:
        raise ValueError("Parcel table missing id column.")