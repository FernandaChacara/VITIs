# Metadata – Weather observations (ERA5)

## Dataset overview

This dataset contains daily weather observations derived from the ERA5 reanalysis for a selected location in the Alentejo region, Portugal. The data were prepared to support the development of a Data Management System focused on viticulture and agro‑environmental analysis.

---

## Source information

* **Organisation:** Copernicus Climate Change Service (C3S)
* **Dataset:** ERA5 Reanalysis – Single Levels
* **Access method:** Copernicus Climate Data Store (CDS) API
* **Licence:** Copernicus Licence (free and open use)
* **Domain:** Climate and meteorology

---

## Spatial coverage

* **Region:** Alentejo, Portugal
* **Method:** Data extracted for a single ERA5 grid point
* **Coordinates:** Latitude 38.5, Longitude −7.9

---

## Temporal coverage

* **Period:** January 2023 – December 2023
* **Temporal resolution:** Daily observations at 12:00 UTC

---

## Original data format

* **Format:** NetCDF (.nc), compressed
* **Structure:** Multidimensional (time × latitude × longitude)
* **Variables:** Meteorological variables provided at single levels

---

## Data processing and transformation

The following steps were applied to prepare the data for database import:

1. Download of ERA5 data using the CDS API.
2. Extraction of NetCDF files from compressed archives.
3. Spatial subsetting to a single grid point representative of the study area.
4. Conversion from NetCDF to tabular CSV format.
5. Removal of non‑informative metadata variables (e.g. `number`, `expver`).
6. Conversion of temperature variables from Kelvin to degrees Celsius.
7. Calculation of relative humidity from air temperature and dew point temperature.
8. Semantic harmonisation of column names to improve clarity and interpretability.

All transformations were performed programmatically using Python to ensure reproducibility.

---

## Data dictionary

### Table: `weather_observation`

| Column name            | Description                            | Unit         | Source  |
| ---------------------- | -------------------------------------- | ------------ | ------- |
| observation_time       | Date and time of observation           | UTC datetime | ERA5    |
| air_temperature_c      | Air temperature at 2 metres            | °C           | ERA5    |
| dewpoint_temperature_c | Dew point temperature at 2 metres      | °C           | ERA5    |
| relative_humidity_pct  | Relative humidity                      | %            | Derived |
| precipitation_m        | Total precipitation                    | m            | ERA5    |
| solar_radiation_jm2    | Surface solar radiation downwards      | J/m²         | ERA5    |
| wind_u_10m             | Zonal wind component at 10 metres      | m/s          | ERA5    |
| wind_v_10m             | Meridional wind component at 10 metres | m/s          | ERA5    |
| evaporation_m          | Evaporation                            | m            | ERA5    |

---

## Derived variables

* **Relative humidity:** Calculated from air temperature and dew point temperature using standard meteorological equations.

---

## Notes

* Numeric values may appear in scientific notation depending on the software used for visualisation.
* The dataset is intended for analytical and educational purposes within the scope of the DMS and FADS projects.
