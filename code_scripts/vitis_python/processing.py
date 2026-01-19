import pandas as pd
from code_scripts.vitis_python.domain import VineyardParcel

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