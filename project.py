"""
VITIS – AI-driven vineyard stress analysis
Introduction to Python | MSc Green Data Science | ISA
"""

import pandas as pd
from pathlib import Path


# ========================
# Main execution function
# ========================

def main():
    ndvi_data = load_ndvi_data()
    climate_data = load_climate_data()
    dms_data = load_dms_exports()

    validate_ndvi_data(ndvi_data)
    validate_climate_data(climate_data)
    validate_dms_data(dms_data)

    integrated_data = integrate_data(ndvi_data, climate_data, dms_data)
    validated_data = validate_integration(integrated_data)

    parcels = build_parcels(validated_data)
    results = process_parcels(parcels)

    results_table = aggregate_results(results)
    summary_metrics = compute_global_metrics(results_table)

    export_results(results_table, summary_metrics)


# ========================
# Data loading functions
# ========================

def load_ndvi_data():
    file_path = Path("processed_data/ndvi_alentejo_2023_structured.csv")
    if not file_path.exists():
        raise FileNotFoundError("NDVI processed file not found.")

    df = pd.read_csv(file_path)

    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    df["ndvi_mean"] = pd.to_numeric(df["ndvi_mean"], errors="coerce")

    return df[["parcel_id", "observation_date", "ndvi_mean"]]


def load_climate_data():
    file_path = Path("processed_data/era5_alentejo_structured.csv")
    if not file_path.exists():
        raise FileNotFoundError("Climate (ERA5) processed file not found.")

    df = pd.read_csv(file_path)

    df["observation_time"] = pd.to_datetime(df["observation_time"], errors="coerce")
    df["air_temperature_c"] = pd.to_numeric(df["air_temperature_c"], errors="coerce")
    df["precipitation_m"] = pd.to_numeric(df["precipitation_m"], errors="coerce")

    return df[[
        "parcel_id",
        "observation_time",
        "air_temperature_c",
        "precipitation_m"
    ]]


def load_dms_exports():
    parcels_file = Path("original_data/parcel.csv")
    if not parcels_file.exists():
        raise FileNotFoundError("Parcel table not found.")

    return {
        "parcels": pd.read_csv(parcels_file)
    }


# ========================
# Validation functions
# ========================

def validate_ndvi_data(ndvi_data):
    required = {"parcel_id", "observation_date", "ndvi_mean"}
    if not required.issubset(ndvi_data.columns):
        raise ValueError("NDVI missing required columns.")

    if ndvi_data.isnull().any().any():
        raise ValueError("NDVI data contains null values.")

    if (ndvi_data["ndvi_mean"] < -1).any() or (ndvi_data["ndvi_mean"] > 1).any():
        raise ValueError("NDVI values outside [-1, 1].")


def validate_climate_data(climate_data):
    required = {
        "parcel_id",
        "observation_time",
        "air_temperature_c",
        "precipitation_m"
    }

    if not required.issubset(climate_data.columns):
        raise ValueError("Climate data missing required columns.")

    # Critical fields must not be null
    if climate_data["parcel_id"].isnull().any():
        raise ValueError("Climate data contains null parcel_id.")

    if climate_data["observation_time"].isnull().any():
        raise ValueError("Climate data contains null observation_time.")

    # Climate variables may have gaps (acceptable in ERA5)
    temp = climate_data["air_temperature_c"]
    prec = climate_data["precipitation_m"]

    if temp.dropna().lt(-30).any() or temp.dropna().gt(60).any():
        raise ValueError("Temperature outside plausible range.")

    if prec.dropna().lt(0).any():
        raise ValueError("Negative precipitation detected.")


def validate_dms_data(dms_data):
    parcels = dms_data["parcels"]

    if "id" not in parcels.columns:
        raise ValueError("parcels table missing id column.")

    if parcels["id"].isnull().any():
        raise ValueError("parcels table contains null id values.")

    if parcels["id"].duplicated().any():
        raise ValueError("Duplicate parcel ids detected.")

def validate_integration(integrated_data):
    if integrated_data.empty:
        raise ValueError("Integrated dataset is empty.")

    if integrated_data.duplicated(
        subset=["parcel_id", "observation_date"]
    ).any():
        raise ValueError("Duplicate parcel-date combinations.")

    return integrated_data


# ========================
# Integration
# ========================

def integrate_data(ndvi_data, climate_data, dms_data):
    merged = pd.merge(
        ndvi_data,
        climate_data,
        left_on=["parcel_id", "observation_date"],
        right_on=["parcel_id", "observation_time"],
        how="left"
    )

    valid_parcels = dms_data["parcels"]["id"].unique()
    return merged[merged["parcel_id"].isin(valid_parcels)]


# ========================
# Domain model
# ========================

class VineyardParcel:
    def __init__(self, parcel_id, ndvi_series, climate_series):
        self.parcel_id = parcel_id
        self.ndvi_series = ndvi_series
        self.climate_series = climate_series

    def compute_vigor(self):
        return self.ndvi_series["ndvi_mean"].mean()

    def compute_water_stress(self):
        mean_ndvi = self.ndvi_series["ndvi_mean"].mean()
        mean_temp = self.climate_series["air_temperature_c"].mean()
        return (1 - mean_ndvi) * (mean_temp / 30)

    def classify_status(self):
        stress = self.compute_water_stress()
        if stress < 0.3:
            return "low"
        elif stress < 0.6:
            return "medium"
        return "high"


# ========================
# Analysis
# ========================

def build_parcels(validated_data):
    parcels = []
    for pid, group in validated_data.groupby("parcel_id"):
        parcels.append(
            VineyardParcel(
                pid,
                group[["observation_date", "ndvi_mean"]],
                group[[
                    "observation_time",
                    "air_temperature_c",
                    "precipitation_m"
                ]],
            )
        )
    return parcels


def process_parcels(parcels):
    return [
        {
            "parcel_id": p.parcel_id,
            "vigor": p.compute_vigor(),
            "water_stress": p.compute_water_stress(),
            "status": p.classify_status(),
        }
        for p in parcels
    ]


# ========================
# Outputs
# ========================

def aggregate_results(results):
    return pd.DataFrame(results)


def compute_global_metrics(results_table):
    return pd.DataFrame(
        [{
            "total_parcels": results_table["parcel_id"].nunique(),
            "mean_water_stress": results_table["water_stress"].mean(),
        }]
    )


def export_results(results_table, summary_metrics):
    Path("outputs").mkdir(exist_ok=True)
    results_table.to_csv("outputs/results_parcels.csv", index=False)
    summary_metrics.to_csv("outputs/summary_metrics.csv", index=False)


# ========================
# Entry point
# ========================

if __name__ == "__main__":
    main()