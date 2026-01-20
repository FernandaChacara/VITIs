"""
VITIS — Tests
Introduction to Python | MSc Green Data Science | ISA
"""

import pytest
import pandas as pd

from project import (
    integrate_data,
    build_parcels,
    process_parcels,
    VineyardParcel
)

# =========================================================
# FIXTURES
# =========================================================

@pytest.fixture
def test_data():
    """Synthetic and deterministic test data for VITIS pipeline."""

    dates = pd.to_datetime([
        "2024-07-01", "2024-07-02",
        "2024-07-01", "2024-07-02"
    ])

    ndvi = pd.DataFrame({
        "parcel_id": [1, 1, 2, 2],
        "date": dates,
        "ndvi_mean": [0.70, 0.68, 0.45, 0.43]
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
# UNIT TESTS — CORE FUNCTIONS
# =========================================================

def test_integrate_data(test_data):
    ndvi, climate, parcels = test_data
    integrated = integrate_data(ndvi, climate, parcels)

    assert not integrated.empty
    assert set(["parcel_id", "ndvi_mean", "air_temperature_c"]).issubset(
        integrated.columns
    )


def test_build_parcels(test_data):
    ndvi, climate, parcels = test_data
    integrated = integrate_data(ndvi, climate, parcels)
    vineyard_parcels = build_parcels(integrated)

    assert len(vineyard_parcels) == 2
    assert all(isinstance(p, VineyardParcel) for p in vineyard_parcels)


def test_process_parcels(test_data):
    ndvi, climate, parcels = test_data
    integrated = integrate_data(ndvi, climate, parcels)
    vineyard_parcels = build_parcels(integrated)
    results = process_parcels(vineyard_parcels)

    assert "status" in results.columns
    assert "forecast_7d" in results.columns
    assert results["forecast_7d"].notna().any()


# =========================================================
# UNIT TESTS — DOMAIN MODEL (CLASS METHODS)
# =========================================================

def test_compute_vigor(test_data):
    ndvi, climate, parcels = test_data
    integrated = integrate_data(ndvi, climate, parcels)
    parcel = build_parcels(integrated)[0]

    vigor = parcel.compute_vigor()
    assert 0 < vigor < 1


def test_compute_water_stress_sensitivity(test_data):
    ndvi, climate, parcels = test_data
    integrated = integrate_data(ndvi, climate, parcels)
    vineyard_parcels = build_parcels(integrated)

    ws_low = vineyard_parcels[0].compute_water_stress()
    ws_high = vineyard_parcels[1].compute_water_stress()

    assert ws_high > ws_low


def test_classify_status_thresholds():
    parcel = VineyardParcel(1, pd.DataFrame({
        "ndvi_mean": [0.9],
        "air_temperature_c": [20]
    }))

    assert parcel.classify_status(0.2) == "low"
    assert parcel.classify_status(0.4) == "medium"
    assert parcel.classify_status(0.8) == "high"


def test_missing_data_returns_none():
    parcel = VineyardParcel(1, pd.DataFrame({
        "ndvi_mean": [pd.NA],
        "air_temperature_c": [30]
    }))

    assert parcel.compute_water_stress() is None


# =========================================================
# FUNCTIONAL TEST 
# =========================================================

def test_vitis_pipeline(test_data):
    ndvi, climate, parcels = test_data
    integrated = integrate_data(ndvi, climate, parcels)
    vineyard_parcels = build_parcels(integrated)
    results = process_parcels(vineyard_parcels)

    stress_p1 = results.loc[
        results["parcel_id"] == 1, "water_stress"
    ].values[0]

    stress_p2 = results.loc[
        results["parcel_id"] == 2, "water_stress"
    ].values[0]

    assert stress_p2 > stress_p1
    print("VITIS end-to-end pipeline test passed successfully.")
