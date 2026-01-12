"""
VITIS — Precision Water-Stress Intelligence for Mediterranean Vineyards
Introduction to Python | MSc Green Data Science | ISA

Decision Support System (DSS)
"""

import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


# =========================================================
# Paths
# =========================================================

NDVI_PATH = "processed_data/ndvi_alentejo_2023_structured.csv"
CLIMATE_PATH = "processed_data/era5_alentejo_structured.csv"
PARCEL_PATH = "original_data/parcel.csv"

OUTPUT_DIR = Path("outputs")
OUTPUT_DIR.mkdir(exist_ok=True)


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


# =========================================================
# Integration
# =========================================================

def integrate_data(ndvi, climate, parcels):
    ndvi = ndvi.rename(columns={"observation_date": "date"})
    ndvi["date"] = ndvi["date"].dt.date

    merged = ndvi.merge(
        climate,
        on=["parcel_id", "date"],
        how="left"
    )

    valid_ids = parcels["id"].unique()
    return merged[merged["parcel_id"].isin(valid_ids)]


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
# Processing
# =========================================================

def build_parcels(df):
    return [VineyardParcel(pid, g) for pid, g in df.groupby("parcel_id")]


def process_parcels(parcels):
    records = []

    for p in parcels:
        ws = p.compute_water_stress()
        forecast = p.forecast_7d()
        status = p.classify_status(ws)

        decision = (
            "NO ACTION REQUIRED"
            if status == "low"
            else "MONITOR CONDITIONS"
            if status == "medium"
            else "SCHEDULE IRRIGATION"
        )

        records.append(
            {
                "parcel_id": p.parcel_id,
                "mean_ndvi": round(p.compute_vigor(), 3),
                "water_stress": round(ws, 3),
                "forecast_7d": round(forecast, 3),
                "stress_level": status,
                "confidence": 1.0,
                "recommendation": decision,
            }
        )

    return pd.DataFrame(records)


# =========================================================
# Alert report (Markdown + graph)
# =========================================================

def generate_alert(parcel_row):
    pid = parcel_row["parcel_id"]
    pname = parcel_row["parcel_name"]

    fig, ax = plt.subplots(figsize=(5, 3))
    ax.bar(
        ["Current", "7-day forecast"],
        [parcel_row["water_stress"], parcel_row["forecast_7d"]],
        color=["orange", "red"],
    )
    ax.set_ylabel("Water Stress Index")
    ax.set_title(f"Parcel {pid} — Stress Outlook")

    img_path = OUTPUT_DIR / f"parcel_{pid}_stress.png"
    plt.tight_layout()
    plt.savefig(img_path, dpi=200)
    plt.close()

    md = f"""# VITIS — Decision Support Alert

## Vineyard Parcel Assessment

**Parcel ID:** {pid}  
**Parcel Name:** {pname}

---

## 1. Vegetative Condition
- **Mean NDVI:** {parcel_row['mean_ndvi']:.3f}

---

## 2. Water Stress Assessment
- **Current Water Stress Index:** {parcel_row['water_stress']:.3f}
- **7-day Forecast Water Stress Index:** {parcel_row['forecast_7d']:.3f}
- **Stress Classification:** {parcel_row['stress_level']}

---

## 3. Decision Support Recommendation
**{parcel_row['recommendation']}**

---

## 4. Model Confidence
- **Decision confidence score:** {parcel_row['confidence']:.2f}

---

## 5. Stress Outlook Visualization
![Water stress forecast](parcel_{pid}_stress.png)

---

*Automatically generated by the VITIS Decision Support System.*
"""

    out_path = OUTPUT_DIR / f"parcel_{pid}_alert.md"
    out_path.write_text(md, encoding="utf-8")


# =========================================================
# Spatial risk map 
# =========================================================

def generate_spatial_risk_map(results_df, parcels_df):
    df = results_df.merge(
        parcels_df,
        left_on="parcel_id",
        right_on="id",
        how="left"
    )

    fig, ax = plt.subplots(figsize=(8, 6))

    scatter = ax.scatter(
        df["longitude"],
        df["latitude"],
        c=df["water_stress"],
        cmap="RdYlGn_r",
        s=120,
        edgecolor="black"
    )

    for _, row in df.iterrows():
        ax.text(
            row["longitude"],
            row["latitude"],
            str(int(row["parcel_id"])),
            fontsize=8,
            ha="center",
            va="center",
            color="black",
            weight="bold"
        )

    ax.set_title("VITIS — Spatial Water Stress Risk Map")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label("Water Stress Index")

    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "vitis_risk_map.png", dpi=300)
    plt.close()


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

    # >>> NOVO: adicionar nome da parcela aos resultados
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


