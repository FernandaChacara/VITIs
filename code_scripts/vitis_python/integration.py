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