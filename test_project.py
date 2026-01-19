"""
VITIS — Tests
Introduction to Python | MSc Green Data Science | ISA
"""

import pandas as pd

from project import (
    integrate_data,
    build_parcels,
    process_parcels,
    VineyardParcel
)


def create_test_data():
    dates = pd.to_datetime([
        "2024-07-01", "2024-07-02",
        "2024-07-01", "2024-07-02"
    ])

    ndvi = pd.DataFrame({
        "parcel_id": [1, 1, 2, 2],
        "date": dates,
        "ndvi_mean": [0.7, 0.68, 0.45, 0.43]
    })

    climate = pd.DataFrame({
        "parcel_id": [1, 1, 2, 2],
        "date": dates,
        "air_temperature_c": [25, 26, 32, 33]
    })

    parcels = pd.DataFrame({
        "id": [1, 2],
        "name": ["Test Parcel A", "Test Parcel B"]
    })

    return ndvi, climate, parcels


# =========================================================
# REQUIRED TESTS 
# =========================================================

def test_integrate_data():
    ndvi, climate, parcels = create_test_data()
    integrated = integrate_data(ndvi, climate, parcels)

    assert not integrated.empty
    assert "parcel_id" in integrated.columns


def test_build_parcels():
    ndvi, climate, parcels = create_test_data()
    integrated = integrate_data(ndvi, climate, parcels)
    vineyard_parcels = build_parcels(integrated)

    assert len(vineyard_parcels) == 2
    assert isinstance(vineyard_parcels[0], VineyardParcel)


def test_process_parcels():
    ndvi, climate, parcels = create_test_data()
    integrated = integrate_data(ndvi, climate, parcels)
    vineyard_parcels = build_parcels(integrated)
    results = process_parcels(vineyard_parcels)

    assert "forecast_7d" in results.columns
    assert results["forecast_7d"].notna().all()


# =========================================================
# FUNCTIONAL TEST 
# =========================================================

def test_vitis_pipeline():
    ndvi, climate, parcels = create_test_data()
    integrated = integrate_data(ndvi, climate, parcels)
    vineyard_parcels = build_parcels(integrated)
    results = process_parcels(vineyard_parcels)

    stress_p1 = results.loc[results["parcel_id"] == 1, "water_stress"].values[0]
    stress_p2 = results.loc[results["parcel_id"] == 2, "water_stress"].values[0]

    assert stress_p2 > stress_p1

