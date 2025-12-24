# Metadata – Irrigation records

## Dataset overview
This dataset contains irrigation records associated with vineyard parcels in the Alentejo region, Portugal. The data were generated to support the development and testing of a Data Management System focused on viticulture and agro-environmental analysis.

The irrigation data represents **simulated management practices**, designed to be realistic and coherent with the climatic and vegetation context of the study area.

## Source information
- Organisation: Project-generated dataset
- Dataset: Simulated irrigation records
- Access method: Internal generation
- Licence: Academic use only
- Domain: Agricultural management / irrigation

## Spatial coverage
- Region: Alentejo, Portugal
- Unit of observation: Vineyard parcel
- Method: Irrigation events associated with parcel identifiers

## Temporal coverage
- Period: January 2023 – December 2023
- Temporal resolution: Event-based (irrigation occurrences)

## Original data format
- Format: CSV
- Structure: Event-based tabular data
- Variables: Irrigation date, volume, method and notes

## Data processing and transformation
The irrigation dataset was generated and prepared according to the following steps:

- Definition of a realistic irrigation calendar covering the growing season
- Simulation of irrigation frequency varying across parcels and months
- Assignment of irrigation volumes based on typical vineyard irrigation practices
- Generation of irrigation timestamps and event identifiers
- Formatting of the dataset into a structured CSV file compatible with SQL import
- Validation of referential integrity with existing parcel identifiers

All steps were performed programmatically to ensure internal consistency and reproducibility.

## Data dictionary
**Table:** irrigation_log

| Column name       | Description                                      | Unit        | Source   |
|-------------------|--------------------------------------------------|-------------|----------|
| parcel_id         | Identifier of the irrigated parcel               | –           | Internal |
| irrigation_time   | Date and time of irrigation event                | Datetime    | Simulated|
| volume_liters     | Volume of water applied                          | Liters      | Simulated|
| method            | Irrigation method                                | –           | Simulated|
| notes             | Additional contextual information                | –           | Simulated|

## Derived variables
No derived variables were calculated for this dataset.

## Notes
- Irrigation data is **simulated** and does not represent real management records.
- The dataset is intended to demonstrate data integration and analytical workflows.
- Irrigation events were generated to be temporally coherent with NDVI and climate observations.
- The data should be interpreted as illustrative rather than observational evidence.

The dataset is intended for analytical and educational purposes within the scope of the DMS and FADS projects.
