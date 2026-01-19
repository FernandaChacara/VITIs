import pandas as pd
from code_scripts.vitis_python.domain import VineyardParcel

# =========================================================
# Processing
# =========================================================

def build_parcels(df):
    return [VineyardParcel(pid, g) for pid, g in df.groupby("parcel_id")]


import pandas as pd


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