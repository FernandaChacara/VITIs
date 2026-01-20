"""
VITIS — Precision Water-Stress Intelligence for Mediterranean Vineyards
Introduction to Python | MSc Green Data Science | ISA

Decision Support System (DSS)
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from code_scripts.python_codes.data import load_climate_data, load_ndvi_data, load_parcel_data
from code_scripts.python_codes.validation import validate_climate_data, validate_ndvi_data, validate_parcel_data
from code_scripts.python_codes.alert_maps import generate_alert, generate_spatial_risk_map

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)

# =========================================================
# Integration
# =========================================================

def integrate_data(ndvi, climate, parcels):
    """
    Integrate NDVI, climate, and parcel datasets.
    Supports both real and synthetic schemas.
    """

    ndvi = ndvi.copy()
    climate = climate.copy()
    parcels = parcels.copy()

    # --- NDVI date handling ---
    if "observation_date" in ndvi.columns:
        ndvi["date"] = pd.to_datetime(ndvi["observation_date"], errors="coerce")
    elif "date" in ndvi.columns:
        ndvi["date"] = pd.to_datetime(ndvi["date"], errors="coerce")
    else:
        raise KeyError(
            "NDVI dataset must contain 'observation_date' or 'date' column"
        )

    # --- Climate date handling ---
    if "date" in climate.columns:
        climate["date"] = pd.to_datetime(climate["date"], errors="coerce")
    else:
        raise KeyError("Climate dataset must contain 'date' column")

    # --- Merge NDVI + climate ---
    merged = ndvi.merge(
        climate,
        on=["parcel_id", "date"],
        how="left"
    )

    # --- Attach parcel metadata ---
    merged = merged.merge(
        parcels,
        left_on="parcel_id",
        right_on="id",
        how="left"
    )

    return merged

# =========================================================
# Processing
# =========================================================

def build_parcels(df):
    return [VineyardParcel(pid, g) for pid, g in df.groupby("parcel_id")]


def process_parcels(vineyard_parcels):
    """
    Process VineyardParcel objects and return DSS indicators per parcel,
    including short-term forecast.
    """

    records = []

    for parcel in vineyard_parcels:
        ndvi_mean = parcel.compute_vigor()
        water_stress = parcel.compute_water_stress()

        if water_stress is None:
            status = None
            forecast_7d = None
        else:
            status = parcel.classify_status(water_stress)
            forecast_7d = parcel.forecast_7d()

        records.append({
            "parcel_id": parcel.parcel_id,
            "ndvi_mean": ndvi_mean,
            "water_stress": water_stress,
            "forecast_7d": forecast_7d,
            "status": status
        })

    return pd.DataFrame.from_records(records)

# =========================================================
# Domain model
# =========================================================

class VineyardParcel:
    def __init__(self, parcel_id, df):
        self.parcel_id = parcel_id
        self.df = df

    def compute_vigor(self):
        return self.df["ndvi_mean"].mean()

    def compute_water_stress(self):
        ndvi = self.df["ndvi_mean"].mean()
        temp = self.df["air_temperature_c"].mean()

        if pd.isna(ndvi) or pd.isna(temp):
            return None

        return (1 - ndvi) * (temp / 30)

    def forecast_7d(self):
        ws = self.compute_water_stress()
        if ws is None:
            return None
        return min(ws + 0.05, 1.2)

    def classify_status(self, ws):
        if ws < 0.3:
            return "low"
        elif ws < 0.6:
            return "medium"
        return "high"
    
 # =========================================================
# CLI
# =========================================================

def decision_support_interface(results):
    while True:
        print("\nVITIS — DSS MENU")
        print("1. View all parcels")
        print("2. Analyze single parcel")
        print("3. Generate alert reports (all parcels)")
        print("4. Exit")

        choice = input("Option: ").strip()

        if choice == "1":
            print(results)

        elif choice == "2":
            pid = int(input("Parcel ID: "))
            row = results[results["parcel_id"] == pid].iloc[0]
            generate_alert(row)
            print(f"Alert generated for parcel {pid}.")

        elif choice == "3":
            for _, row in results.iterrows():
                generate_alert(row)
            print("All alerts generated.")

        elif choice == "4":
            break
 
# =========================================================
# Main
# =========================================================

def main():
    ndvi = load_ndvi_data()
    climate = load_climate_data()
    parcels = load_parcel_data()

    validate_ndvi_data(ndvi)
    validate_climate_data(climate)
    validate_parcel_data(parcels)

    integrated = integrate_data(ndvi, climate, parcels)
    vineyard_parcels = build_parcels(integrated)
    results = process_parcels(vineyard_parcels)

    results = results.merge(
        parcels[["id", "name"]],
        left_on="parcel_id",
        right_on="id",
        how="left"
    ).rename(columns={"name": "parcel_name"}).drop(columns=["id"])

    results.to_csv(OUTPUT_DIR / "vitis_results.csv", index=False)

    generate_spatial_risk_map(results, parcels)
    decision_support_interface(results)


if __name__ == "__main__":
    main()