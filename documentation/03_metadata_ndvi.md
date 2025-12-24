# NDVI Metadata and Description

## Data Source Identification

- **Data name:** Normalized Difference Vegetation Index (NDVI)
- **Source programme:** Copernicus Programme
- **Providing organisation:** European Commission
- **Licence:** Open Access
- **Domain:** Remote sensing / vegetation monitoring
- **Spatial coverage:** Alentejo region, Portugal
- **Temporal coverage:** One-year period

The NDVI data used in this project was obtained from the Copernicus programme and represents a regional-scale vegetation indicator for the Alentejo region.

---

## Data Description

NDVI (Normalized Difference Vegetation Index) is a widely used remote sensing indicator that provides information on vegetation vigor and greenness. It is derived from satellite reflectance measurements in the red and near-infrared spectral bands.

In this project, NDVI values are used as an indicator of **regional vegetation conditions** over time. The dataset consists of NDVI observations aggregated at regional scale, rather than measurements extracted for individual agricultural parcels.

Each NDVI observation includes:
- observation date
- mean NDVI value for the region

---

## Spatial Resolution and Interpretation

The NDVI product used has a spatial resolution that does not allow direct attribution of values to individual vineyard parcels. As a result, NDVI values were **not calculated at parcel level**, but instead represent regional vegetation conditions for the Alentejo area.

For the purposes of this Data Management System, NDVI values were associated with parcels to provide **contextual environmental information**, enabling exploratory analysis within a unified relational structure.

This association does **not** imply that the NDVI values represent parcel-level vegetation measurements.

---

## Data Processing and Transformation

Prior to database import, the NDVI data underwent the following processing steps:

- Conversion from original Copernicus data format to CSV
- Selection of relevant temporal observations
- Standardisation of column names and data types
- Formatting of observation dates to ensure compatibility with SQL
- Creation of structured files suitable for relational database import

Processed NDVI data files are stored in the `processed_data/` directory.

---

## Data Structure in the Database

Within the database, NDVI data is stored in the table `vegetation_index`, with the following key attributes:

- `parcel_id`: identifier used to associate NDVI observations with parcels for contextual analysis
- `source_id`: reference to the data source (Copernicus NDVI)
- `observation_date`: date of the NDVI observation
- `ndvi_mean`: mean NDVI value for the region

Foreign key constraints ensure consistency between NDVI records and the corresponding reference tables.

---

## Intended Use

NDVI data in this project is intended to support:

- inspection of temporal patterns in regional vegetation conditions
- comparison of NDVI values associated with different parcels
- exploratory integration with climatic variables
- contextual analysis of irrigation practices

The use of NDVI in this project is **exploratory and descriptive**, aiming to demonstrate the analytical capabilities of the data management system rather than to provide parcel-level biophysical assessment.

---

## Limitations

- NDVI values represent regional vegetation conditions and do not capture within-region spatial variability.
- Parcel-level NDVI extraction would require spatial intersection between parcel geometries and satellite pixels.
- High-resolution or parcel-specific NDVI products were outside the scope of this assignment.

These limitations are acknowledged and explicitly considered in the interpretation of analysis results.
