# Metadata – Vegetation observations (NDVI)

## Dataset overview
This dataset contains Normalized Difference Vegetation Index (NDVI) observations derived from Copernicus satellite products for the Alentejo region, Portugal. The data were prepared to support the development of a Data Management System focused on vineyard monitoring and agro-environmental analysis.

## Source information
- Organisation: Copernicus Programme (European Commission)
- Dataset: Copernicus NDVI product
- Access method: Copernicus data services
- Licence: Open Access
- Domain: Remote sensing / vegetation monitoring

## Spatial coverage
- Region: Alentejo, Portugal
- Method: Regional aggregation of satellite observations
- Spatial resolution: Medium resolution (regional scale)

## Temporal coverage
- Period: January 2023 – December 2023
- Temporal resolution: Discrete observation dates

## Original data format
- Format: Satellite-derived product (processed to CSV)
- Structure: Tabular time series
- Variables: Vegetation index metrics

## Data processing and transformation
The following steps were applied to prepare the NDVI data for database import:

- Extraction of NDVI values from Copernicus products
- Selection of observations corresponding to the study period
- Aggregation of NDVI values at regional scale
- Conversion of data to CSV format
- Standardisation of column names and data types
- Formatting of observation dates to ensure compatibility with SQL

All transformations were performed programmatically using Python to ensure reproducibility.

## Data dictionary
**Table:** vegetation_index

| Column name      | Description                                            | Unit          | Source     |
|------------------|--------------------------------------------------------|---------------|------------|
| parcel_id        | Identifier used to associate NDVI values with parcels  | –             | Internal   |
| source_id        | Reference to data source                               | –             | Internal   |
| observation_date | Date of NDVI observation                               | Date          | Copernicus |
| ndvi_mean        | Mean NDVI value for the region                         | Dimensionless | Copernicus |

## Derived variables
No additional derived variables were calculated for this dataset.

## Notes
- NDVI values represent **regional vegetation conditions** and do not correspond to parcel-level measurements.
- Association of NDVI values with parcels is intended to provide environmental context for exploratory analysis.
- Parcel-level NDVI extraction would require spatial intersection between parcel geometries and satellite pixels, which is outside the scope of this project.

The dataset is intended for analytical and educational purposes within the scope of the DMS and FADS projects.

