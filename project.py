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
    file_path = Path("data/ndvi/ndvi_sample.csv")
    if not file_path.exists():
        raise FileNotFoundError("NDVI data file not found.")
    return pd.read_csv(file_path)


def load_climate_data():
    file_path = Path("data/climate/climate_sample.csv")
    if not file_path.exists():
        raise FileNotFoundError("Climate data file not found.")
    return pd.read_csv(file_path)


def load_dms_exports():
    base_path = Path("data/dms")
    parcels_file = base_path / "parcels.csv"

    if not parcels_file.exists():
        raise FileNotFoundError("DMS parcels export file not found.")

    return {"parcels": pd.read_csv(parcels_file)}


# ========================
# Validation functions
# ========================

def validate_ndvi_data(ndvi_data):
    required_columns = {"parcel_id", "date", "ndvi"}

    if not required_columns.issubset(ndvi_data.columns):
        raise ValueError("NDVI missing required columns.")

    if ndvi_data["ndvi"].isnull().any():
        raise ValueError("NDVI column contains null values.")

    if (ndvi_data["ndvi"] < -1).any() or (ndvi_data["ndvi"] > 1).any():
        raise ValueError("NDVI values outside [-1, 1].")


def validate_climate_data(climate_data):
    required_columns = {"date", "temperature", "precipitation"}

    if not required_columns.issubset(climate_data.columns):
        raise ValueError("Climate data missing required columns.")

    if climate_data.isnull().any().any():
        raise ValueError("Climate data contains null values.")

    if (climate_data["temperature"] < -30).any() or (climate_data["temperature"] > 60).any():
        raise ValueError("Temperature outside plausible range.")

    if (climate_data["precipitation"] < 0).any():
        raise ValueError("Negative precipitation detected.")


def validate_dms_data(dms_data):
    parcels = dms_data["parcels"]

    if "parcel_id" not in parcels.columns:
        raise ValueError("parcels table missing parcel_id.")

    if parcels["parcel_id"].duplicated().any():
        raise ValueError("Duplicate parcel_id detected.")


def validate_integration(integrated_data):
    if integrated_data.empty:
        raise ValueError("Integrated dataset is empty.")

    required = {"parcel_id", "date", "ndvi", "temperature", "precipitation"}
    if not required.issubset(integrated_data.columns):
        raise ValueError("Integrated data missing required columns.")

    if integrated_data.duplicated(subset=["parcel_id", "date"]).any():
        raise ValueError("Duplicate parcel_id-date combinations.")

    return integrated_data


# ========================
# Integration
# ========================

def integrate_data(ndvi_data, climate_data, dms_data):
    ndvi_data["date"] = pd.to_datetime(ndvi_data["date"])
    climate_data["date"] = pd.to_datetime(climate_data["date"])

    merged = pd.merge(ndvi_data, climate_data, on="date", how="left")

    valid_parcels = dms_data["parcels"]["parcel_id"].unique()
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
        return self.ndvi_series["ndvi"].mean()

    def compute_water_stress(self):
        mean_ndvi = self.ndvi_series["ndvi"].mean()
        mean_temp = self.climate_series["temperature"].mean()
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
                group[["date", "ndvi"]],
                group[["date", "temperature", "precipitation"]],
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
