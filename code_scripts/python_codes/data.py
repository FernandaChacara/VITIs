import pandas as pd

# =========================================================
# Paths
# =========================================================

NDVI_PATH = "processed_data/ndvi_alentejo_2023_structured.csv"
CLIMATE_PATH = "processed_data/era5_alentejo_structured.csv"
PARCEL_PATH = "original_data/parcel.csv"

# =========================================================
# Data loading
# =========================================================

def load_ndvi_data():
    return pd.read_csv(
        NDVI_PATH,
        parse_dates=["observation_date"]
    )


def load_climate_data():
    df = pd.read_csv(
        CLIMATE_PATH,
        parse_dates=["observation_time"]
    )

    df["air_temperature_c"] = pd.to_numeric(
        df["air_temperature_c"], errors="coerce"
    )
    df["precipitation_m"] = pd.to_numeric(
        df["precipitation_m"], errors="coerce"
    )

    df["date"] = df["observation_time"].dt.date

    return (
        df.groupby(["parcel_id", "date"], as_index=False)
        .agg(
            air_temperature_c=("air_temperature_c", "mean"),
            precipitation_m=("precipitation_m", "sum"),
        )
    )


def load_parcel_data():
    return pd.read_csv(PARCEL_PATH)