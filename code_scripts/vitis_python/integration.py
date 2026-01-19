import pandas as pd

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