"""
VITIS — Precision Water-Stress Intelligence for Mediterranean Vineyards
Introduction to Python | MSc Green Data Science | ISA

Decision Support System (DSS)
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from code_scripts.vitis_python.data import load_ndvi_data, load_climate_data, load_parcel_data
from code_scripts.vitis_python.validation import validate_climate_data, validate_ndvi_data, validate_parcel_data
from code_scripts.vitis_python.integration import integrate_data
from code_scripts.vitis_python.processing import build_parcels, process_parcels
from code_scripts.vitis_python.alerts_maps import generate_alert, generate_spatial_risk_map

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


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


