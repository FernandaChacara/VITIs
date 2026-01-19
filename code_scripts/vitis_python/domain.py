import pandas as pd

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