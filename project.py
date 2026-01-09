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
# Data loading
# ========================

def load_ndvi_data():
    path = Path("processed_data/ndvi_alentejo_2023_structured.csv")
    if not path.exists():
        raise FileNotFoundError("NDVI file not found.")

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    df["observation_date"] = pd.to_datetime(df["observation_date"], errors="coerce")
    df["ndvi_mean"] = pd.to_numeric(df["ndvi_mean"], errors="coerce")

    return df[["parcel_id", "observation_date", "ndvi_mean"]]


def load_climate_data():
    path = Path("processed_data/era5_alentejo_structured.csv")
    if not path.exists():
        raise FileNotFoundError("ERA5 file not found.")

    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()

    df["observation_time"] = pd.to_datetime(df["observation_time"], errors="coerce")
    df["air_temperature_c"] = pd.to_numeric(df["air_temperature_c"], errors="coerce")
    df["precipitation_m"] = pd.to_numeric(df["precipitation_m"], errors="coerce")

    # 🔑 CRÍTICO: reduzir ERA5 a escala diária
    df["date"] = df["observation_time"].dt.date

    daily = (
        df.groupby(["parcel_id", "date"], as_index=False)
          .agg({
              "air_temperature_c": "mean",
              "precipitation_m": "sum"
          })
    )

    return daily


def load_dms_exports():
    path = Path("original_data/parcel.csv")
    if not path.exists():
        raise FileNotFoundError("Parcel table not found.")

    return {"parcels": pd.read_csv(path)}


# ========================
# Validation
# ========================

def validate_ndvi_data(df):
    required = {"parcel_id", "observation_date", "ndvi_mean"}
    if not required.issubset(df.columns):
        raise ValueError("NDVI missing required columns.")

    if df[["parcel_id", "observation_date"]].isnull().any().any():
        raise ValueError("NDVI contains null parcel_id or date.")

    if df["ndvi_mean"].lt(-1).any() or df["ndvi_mean"].gt(1).any():
        raise ValueError("NDVI values outside [-1, 1].")


def validate_climate_data(df):
    required = {
        "parcel_id",
        "date",
        "air_temperature_c",
        "precipitation_m",
    }

    if not required.issubset(df.columns):
        missing = required - set(df.columns)
        raise ValueError(f"Climate data missing required columns: {missing}")

    if df["parcel_id"].isnull().any():
        raise ValueError("Climate data contains null parcel_id.")

    if df["date"].isnull().any():
        raise ValueError("Climate data contains null date.")

    temp = df["air_temperature_c"].dropna()
    prec = df["precipitation_m"].dropna()

    if temp.lt(-30).any() or temp.gt(60).any():
        raise ValueError("Temperature outside plausible range.")

    if prec.lt(0).any():
        raise ValueError("Negative precipitation detected.")


def validate_dms_data(dms_data):
    parcels = dms_data["parcels"]
    if "id" not in parcels.columns:
        raise ValueError("Parcel table missing id column.")

    if parcels["id"].isnull().any():
        raise ValueError("Parcel table contains null id.")


def validate_integration(df):
    if df.empty:
        raise ValueError("Integrated dataset is empty.")

    required = {
        "parcel_id",
        "date",
        "ndvi_mean",
        "air_temperature_c",
        "precipitation_m",
    }

    if not required.issubset(df.columns):
        raise ValueError("Integrated dataset missing required columns.")

    return df


# ========================
# Integration
# ========================

def integrate_data(ndvi, climate, dms):
    ndvi = ndvi.rename(columns={"observation_date": "date"})
    ndvi["date"] = pd.to_datetime(ndvi["date"]).dt.date

    merged = pd.merge(
        ndvi,
        climate,
        on=["parcel_id", "date"],
        how="left"
    )

    valid_parcels = dms["parcels"]["id"].unique()
    return merged[merged["parcel_id"].isin(valid_parcels)]


# ========================
# Domain model
# ========================

class VineyardParcel:
    def __init__(self, parcel_id, df):
        self.parcel_id = parcel_id
        self.df = df

    def compute_vigor(self):
        return self.df["ndvi_mean"].mean()

    def compute_water_stress(self):
        mean_ndvi = self.df["ndvi_mean"].mean()
        mean_temp = self.df["air_temperature_c"].mean()

        if pd.isna(mean_ndvi) or pd.isna(mean_temp):
            return None

        return (1 - mean_ndvi) * (mean_temp / 30)

    def classify_status(self):
        stress = self.compute_water_stress()
        if stress is None:
            return None
        if stress < 0.3:
            return "low"
        elif stress < 0.6:
            return "medium"
        return "high"


# ========================
# Analysis
# ========================

def build_parcels(df):
    parcels = []
    for pid, group in df.groupby("parcel_id"):
        parcels.append(VineyardParcel(pid, group))
    return parcels


def process_parcels(parcels):
    results = []
    for p in parcels:
        results.append({
            "parcel_id": p.parcel_id,
            "vigor": p.compute_vigor(),
            "water_stress": p.compute_water_stress(),
            "status": p.classify_status(),
        })
    return results


# ========================
# Outputs
# ========================

def aggregate_results(results):
    return pd.DataFrame(results)


def compute_global_metrics(results_table):
    return pd.DataFrame([{
        "total_parcels": results_table["parcel_id"].nunique(),
        "mean_water_stress": results_table["water_stress"].mean(),
    }])


def export_results(results_table, summary_metrics):
    Path("outputs").mkdir(exist_ok=True)
    results_table.to_csv("outputs/results_parcels.csv", index=False)
    summary_metrics.to_csv("outputs/summary_metrics.csv", index=False)


# ========================
# Entry point
# ========================

if __name__ == "__main__":
    main()