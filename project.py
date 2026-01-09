"""
VITIs — Precision Water-Stress Intelligence for Mediterranean Vineyards
Introduction to Python | MSc Green Data Science | ISA
"""

import os
import sys
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches


# =========================================================
# Paths
# =========================================================

NDVI_PATH = "processed_data/ndvi_alentejo_2023_structured.csv"
CLIMATE_PATH = "processed_data/era5_alentejo_structured.csv"
IRRIGATION_PATH = "original_data/irrigation_log.csv"
OUTPUT_DIR = "outputs"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# =========================================================
# Data loading
# =========================================================

def load_ndvi_data():
    return pd.read_csv(NDVI_PATH)


def load_climate_data():
    return pd.read_csv(CLIMATE_PATH)


def load_irrigation_data():
    return pd.read_csv(IRRIGATION_PATH)


# =========================================================
# Validation
# =========================================================

def validate_ndvi_data(df):
    if not {"parcel_id", "ndvi_mean"}.issubset(df.columns):
        sys.exit("NDVI file missing required columns")


def validate_climate_data(df):
    if not {"parcel_id", "air_temperature_c"}.issubset(df.columns):
        sys.exit("Climate file missing required columns")


def validate_irrigation_data(df):
    if not {"parcel_id", "irrigation_time"}.issubset(df.columns):
        sys.exit("Irrigation file missing required columns")


# =========================================================
# Processing
# =========================================================

def integrate_data(ndvi, climate):
    climate = climate.copy()

    climate["air_temperature_c"] = pd.to_numeric(
        climate["air_temperature_c"], errors="coerce"
    )

    ndvi["ndvi_mean"] = pd.to_numeric(
        ndvi["ndvi_mean"], errors="coerce"
    )

    return ndvi.merge(climate, on="parcel_id", how="inner")


def build_parcels_df(data, irrigation):
    irrigation_sum = irrigation.groupby("parcel_id").size().reset_index(name="irrigation_events")
    return data.merge(irrigation_sum, on="parcel_id", how="left").fillna({"irrigation_events": 0})


# =========================================================
# Class (USER DEFINED)
# =========================================================

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


# =========================================================
# Risk computation (batch)
# =========================================================

def compute_parcel_metrics(df):
    records = []

    for parcel_id, group in df.groupby("parcel_id"):
        parcel = VineyardParcel(parcel_id, group)

        stress = parcel.compute_water_stress()
        status = parcel.classify_status()
        vigor = parcel.compute_vigor()

        records.append(
            {
                "parcel_id": parcel_id,
                "mean_ndvi": round(vigor, 3),
                "mean_temperature": round(group["air_temperature_c"].mean(), 2),
                "water_stress_index": None if stress is None else round(stress, 3),
                "stress_level": status,
                "irrigation_events": int(group["irrigation_events"].iloc[0]),
            }
        )

    return pd.DataFrame(records)


# =========================================================
# Visualization
# =========================================================

def generate_stress_map(results, filename="outputs/vitis_stress_map.png"):
    fig, ax = plt.subplots(figsize=(12, 8))

    lat = 38.58 + results["parcel_id"] * 0.001
    lon = -7.90 + (results["parcel_id"] % 10) * 0.002

    scatter = ax.scatter(
        lon,
        lat,
        s=600,
        c=results["water_stress_index"],
        cmap="RdYlGn_r",
        edgecolors="black",
        linewidth=2,
        alpha=0.85,
    )

    ax.set_title("VITIs Water Stress Map — Alentejo Vineyards (2023)")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")
    ax.grid(True, alpha=0.3)

    cbar = plt.colorbar(scatter, ax=ax, shrink=0.8)
    cbar.set_label("Water Stress Index", rotation=270, labelpad=20)

    plt.tight_layout()
    plt.savefig(filename, dpi=300)
    plt.close()


# =========================================================
# Outputs
# =========================================================

def export_results(results):
    results.to_csv("outputs/vitis_results_2023.csv", index=False)

    results[results["stress_level"] == "high"].to_csv(
        "outputs/vitis_alerts_high_stress.csv", index=False
    )

    summary = {
        "total_parcels": len(results),
        "high_stress_parcels": int((results["stress_level"] == "high").sum()),
        "mean_ndvi": round(results["mean_ndvi"].mean(), 3),
        "mean_temperature": round(results["mean_temperature"].mean(), 2),
        "mean_stress_index": round(results["water_stress_index"].mean(), 3),
    }

    pd.DataFrame([summary]).to_csv("outputs/vitis_summary.csv", index=False)

    generate_stress_map(results)

    print("\nAutomatic outputs generated")
    print(" - outputs/vitis_results_2023.csv")
    print(" - outputs/vitis_alerts_high_stress.csv")
    print(" - outputs/vitis_summary.csv")
    print(" - outputs/vitis_stress_map.png")


# =========================================================
# Dashboard (USER VIEW)
# =========================================================

def display_risk_dashboard(results, title="PARCEL STATUS"):
    print("\n" + "=" * 70)
    print(f"RISK DASHBOARD — {title}")
    print("=" * 70)

    for _, row in results.iterrows():
        level = row["stress_level"]
        indicator = "🔴" if level == "high" else "🟡" if level == "medium" else "🟢"

        print(f"\nPARCEL {row['parcel_id']}")
        print(f"{indicator} Stress level: {level}")
        print(f"Mean NDVI: {row['mean_ndvi']}")
        print(f"Mean temperature: {row['mean_temperature']} °C")
        print(f"Water stress index: {row['water_stress_index']}")
        print(f"Irrigation events: {row['irrigation_events']}")

# =========================================================
# CLI
# =========================================================

def get_user_parcel_selection(available):
    raw = input("Enter parcel IDs (comma-separated): ").strip()
    try:
        parcels = [int(p.strip()) for p in raw.split(",")]
        return [p for p in parcels if p in available]
    except ValueError:
        return []


def decision_support_interface(results):
    available_parcels = sorted(results["parcel_id"].unique())

    while True:
        print("\n" + "-" * 60)
        print("MAIN MENU")
        print("1. Analyze selected parcels")
        print("2. View all parcels")
        print("3. Analyze single parcel")
        print("4. Exit")

        choice = input("Select option (1–4): ").strip()

        if choice == "1":
            selected = get_user_parcel_selection(available_parcels)
            if selected:
                subset = results[results["parcel_id"].isin(selected)]
                display_risk_dashboard(subset, "SELECTED PARCELS")

        elif choice == "2":
            display_risk_dashboard(results, "ALL PARCELS")

        elif choice == "3":
            pid = input("Parcel ID: ").strip()
            if pid.isdigit() and int(pid) in available_parcels:
                subset = results[results["parcel_id"] == int(pid)]
                display_risk_dashboard(subset, f"PARCEL {pid}")

        elif choice == "4":
            print("Application terminated.")
            break

# =========================================================
# Main
# =========================================================

def main():
    print("VITIs — Precision Water-Stress Intelligence")
    print("=" * 60)

    ndvi = load_ndvi_data()
    climate = load_climate_data()
    irrigation = load_irrigation_data()

    validate_ndvi_data(ndvi)
    validate_climate_data(climate)
    validate_irrigation_data(irrigation)

    data = integrate_data(ndvi, climate)
    data = build_parcels_df(data, irrigation)

    results = compute_parcel_metrics(data)

    export_results(results)
    decision_support_interface(results)
  


if __name__ == "__main__":
    main()

