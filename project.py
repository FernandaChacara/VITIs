"""
VITIS – AI-driven vineyard stress analysis
Introduction to Python | MSc Green Data Science | ISA
"""

# ========================
# Imports (a definir depois)
# ========================
import pandas as pd
from pathlib import Path

# ========================
# Main execution function
# ========================

def main():
    """
    Orchestrates the full VITIS data processing pipeline.
    """

    # Step 1: Load data
    ndvi_data = load_ndvi_data()
    climate_data = load_climate_data()
    dms_data = load_dms_exports()

    # Step 2: Validate inputs
    validate_ndvi_data(ndvi_data)
    validate_climate_data(climate_data)
    validate_dms_data(dms_data)

    # Step 3: Integrate datasets
    integrated_data = integrate_data(
        ndvi_data,
        climate_data,
        dms_data
    )

    validated_data = validate_integration(integrated_data)

    # Step 4: Build domain objects
    parcels = build_parcels(validated_data)

    # Step 5: Analytical processing
    results = process_parcels(parcels)

    # Step 6: Aggregation and outputs
    results_table = aggregate_results(results)
    summary_metrics = compute_global_metrics(results_table)

    export_results(results_table, summary_metrics)


# ========================
# Data loading functions
# ========================

def load_ndvi_data():
    """
    Loads processed NDVI data from file.
    """
     file_path = Path("data/ndvi/ndvi_sample.csv")

    if not file_path.exists():
        raise FileNotFoundError("NDVI data file not found.")

    ndvi_data = pd.read_csv(file_path)

    return ndvi_data
    pass


def load_climate_data():
    """
    Loads aggregated climate data from file.
    """
  file_path = Path("data/climate/climate_sample.csv")

    if not file_path.exists():
        raise FileNotFoundError("Climate data file not found.")

    climate_data = pd.read_csv(file_path)

    return climate_data
    pass


def load_dms_exports():
    """
    Loads exported tables from the DMS database.
    """
 base_path = Path("data/dms")

    parcels_file = base_path / "parcels.csv"

    if not parcels_file.exists():
        raise FileNotFoundError("DMS parcels export file not found.")

    parcels = pd.read_csv(parcels_file)

    dms_data = {
        "parcels": parcels
    }

    return dms_data
    pass


# ========================
# Validation functions
# ========================

def validate_ndvi_data(ndvi_data):
    """
    Validates NDVI values and structure.
    """
    required_columns = {"parcel_id", "date", "ndvi"}

    # Check required columns
    if not required_columns.issubset(ndvi_data.columns):
        missing = required_columns - set(ndvi_data.columns)
        raise ValueError(f"Missing required NDVI columns: {missing}")

    # Check for null values
    if ndvi_data["ndvi"].isnull().any():
        raise ValueError("NDVI column contains null values.")

    if ndvi_data["parcel_id"].isnull().any():
        raise ValueError("parcel_id column contains null values.")

    if ndvi_data["date"].isnull().any():
        raise ValueError("date column contains null values.")

    # Check NDVI physical limits
    if (ndvi_data["ndvi"] < -1).any() or (ndvi_data["ndvi"] > 1).any():
        raise ValueError("NDVI values outside physical range [-1, 1].")

    return True
    pass


def validate_climate_data(climate_data):
    """
    Validates climate data ranges and consistency.
    """
    required_columns = {"date", "temperature", "precipitation"}

    # Check required columns
    if not required_columns.issubset(climate_data.columns):
        missing = required_columns - set(climate_data.columns)
        raise ValueError(f"Missing required climate columns: {missing}")

    # Check for null values in critical fields
    if climate_data["temperature"].isnull().any():
        raise ValueError("Temperature column contains null values.")

    if climate_data["precipitation"].isnull().any():
        raise ValueError("Precipitation column contains null values.")

    if climate_data["date"].isnull().any():
        raise ValueError("Date column contains null values.")

    # Check physical plausibility
    if (climate_data["temperature"] < -30).any() or (climate_data["temperature"] > 60).any():
        raise ValueError("Temperature values outside plausible physical range.")

    if (climate_data["precipitation"] < 0).any():
        raise ValueError("Negative precipitation values detected.")

    return True
    pass


def validate_dms_data(dms_data):
    """
    Validates database exports integrity.
    """
if "parcels" not in dms_data:
        raise ValueError("DMS data must contain a 'parcels' table.")

    parcels = dms_data["parcels"]

    # Check required column
    if "parcel_id" not in parcels.columns:
        raise ValueError("parcels table must contain 'parcel_id' column.")

    # Check for null parcel_id
    if parcels["parcel_id"].isnull().any():
        raise ValueError("parcels table contains null parcel_id values.")

    # Check primary key uniqueness
    if parcels["parcel_id"].duplicated().any():
        raise ValueError("Duplicate parcel_id values detected in parcels table.")

    return True
    pass


def validate_integration(integrated_data):
    """
    Validates the integrated dataset after merging.
    """
     if integrated_data.empty:
        raise ValueError("Integrated dataset is empty.")

    required_columns = {
        "parcel_id",
        "date",
        "ndvi",
        "temperature",
        "precipitation"
    }

    # Check required columns
    if not required_columns.issubset(integrated_data.columns):
        missing = required_columns - set(integrated_data.columns)
        raise ValueError(f"Missing required columns after integration: {missing}")

    # Check for null values in critical fields
    for column in required_columns:
        if integrated_data[column].isnull().any():
            raise ValueError(f"Null values detected in column '{column}' after integration.")

    # Check for unexpected duplicates
    if integrated_data.duplicated(subset=["parcel_id", "date"]).any():
        raise ValueError("Duplicate parcel_id and date combinations detected after integration.")

    return integrated_data
    pass


# ========================
# Integration functions
# ========================

def integrate_data(ndvi_data, climate_data, dms_data):
    """
    Integrates NDVI, climate, and DMS datasets.
    """
     # Ensure date columns are datetime
    ndvi_data["date"] = pd.to_datetime(ndvi_data["date"])
    climate_data["date"] = pd.to_datetime(climate_data["date"])

    # Merge NDVI with climate data on date
    merged = pd.merge(
        ndvi_data,
        climate_data,
        on="date",
        how="left"
    )

    # Keep only parcels that exist in DMS
    valid_parcels = dms_data["parcels"]["parcel_id"].unique()
    merged = merged[merged["parcel_id"].isin(valid_parcels)]

    return merged
    pass


# ========================
# Domain model
# ========================

class VineyardParcel:
    """
    Represents a vineyard parcel and its analytical logic.
    """

    def __init__(self, parcel_id, ndvi_series, climate_series, metadata=None):
        self.parcel_id = parcel_id
        self.ndvi_series = ndvi_series
        self.climate_series = climate_series
        self.metadata = metadata

    def compute_vigor(self):
        """
        Computes vigor metrics for the parcel.
        """
          if self.ndvi_series.empty:
        return None

    return self.ndvi_series["ndvi"].mean()
        pass

    def compute_water_stress(self):
        """
        Computes water stress index.
        """
         if self.ndvi_series.empty or self.climate_series.empty:
        return None

    mean_ndvi = self.ndvi_series["ndvi"].mean()
    mean_temp = self.climate_series["temperature"].mean()

    stress = (1 - mean_ndvi) * (mean_temp / 30)

    return stress
        pass

    def classify_status(self):
        """
        Classifies parcel stress status.
        """
  stress = self.compute_water_stress()

    if stress is None:
        return None

    if stress < 0.3:
        return "low"
    elif stress < 0.6:
        return "medium"
    else:
        return "high"
        pass


# ========================
# Analytical functions
# ========================

def build_parcels(validated_data):
    """
    Builds VineyardParcel objects from validated data.
    """
parcels = []

    grouped = validated_data.groupby("parcel_id")

    for parcel_id, group in grouped:
        ndvi_series = group[["date", "ndvi"]].copy()
        climate_series = group[["date", "temperature", "precipitation"]].copy()

        parcel = VineyardParcel(
            parcel_id=parcel_id,
            ndvi_series=ndvi_series,
            climate_series=climate_series
        )

        parcels.append(parcel)

    return parcels
    pass


def process_parcels(parcels):
    """
    Processes all parcels and computes analytical results.
    """

    results = []

    for parcel in parcels:
        vigor = parcel.compute_vigor()
        stress = parcel.compute_water_stress()
        status = parcel.classify_status()

        results.append({
            "parcel_id": parcel.parcel_id,
            "vigor": vigor,
            "water_stress": stress,
            "status": status
        })

    return results
    pass


# ========================
# Aggregation and outputs
# ========================

def aggregate_results(results):
    """
    Aggregates parcel-level results into a final table.
    """
if not results:
        raise ValueError("No parcel results to aggregate.")

    results_table = pd.DataFrame(results)

    return results_table
    pass


def compute_global_metrics(results_table):
    """
    Computes global summary metrics.
    """
 total_parcels = results_table["parcel_id"].nunique()

    parcels_with_status = results_table["status"].notnull().sum()

    summary = {
        "total_parcels": total_parcels,
        "parcels_with_status": parcels_with_status,
        "percentage_with_status": (
            parcels_with_status / total_parcels * 100 if total_parcels > 0 else 0
        )
    }

    summary_metrics = pd.DataFrame([summary])

    return summary_metrics
    pass


def export_results(results_table, summary_metrics):
    """
    Exports final outputs to files.
    """
    
    output_dir = Path("outputs")
    output_dir.mkdir(exist_ok=True)

    results_path = output_dir / "results_parcels.csv"
    summary_path = output_dir / "summary_metrics.csv"

    results_table.to_csv(results_path, index=False)
    summary_metrics.to_csv(summary_path, index=False)
    pass


# ========================
# Entry point
# ========================

if __name__ == "__main__":
    main()
