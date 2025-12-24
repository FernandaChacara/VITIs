# Database Design

## Overview

This document describes the relational database design developed for the Data Management System focused on vineyard monitoring in the Alentejo region. The database integrates structural, observational, and analytical entities to support data storage, integrity, and SQL-based analysis.

The design follows the principles of the Third Normal Form (3NF), ensuring data consistency, minimisation of redundancy, and clear separation between raw data and derived analytical results.

---

## Design principles

The database design is guided by the following principles:

- Clear separation between structural, observational, and analytical entities
- Use of primary and foreign keys to ensure referential integrity
- Avoidance of redundant data storage
- Support for reproducible SQL-based data analysis
- Compatibility with MySQL/MariaDB DBMS

---

## Entity overview

The database is composed of the following entity groups:

- **Structural entities**: `user`, `parcel`, `data_source`
- **Observational entities**: `weather_observation`, `vegetation_index`, `irrigation_log`
- **Analytical entities**: `analysis_result`

Each entity is described in detail below.

---

## Structural entities

### Table: user

The `user` table represents individuals or entities associated with vineyard parcels.

| Column | Description |
|------|------------|
| id | Unique identifier of the user (PK) |
| name | User name |
| email | Contact email |
| phone | Contact phone number |
| affiliation | Organisational affiliation |

---

### Table: parcel

The `parcel` table represents vineyard parcels located in the Alentejo region and provides spatial context for all observational and analytical data.

| Column | Description |
|------|------------|
| id | Unique parcel identifier (PK) |
| user_id | Reference to the associated user (FK) |
| name | Parcel name |
| region | Administrative region |
| latitude | Latitude coordinate |
| longitude | Longitude coordinate |
| area_ha | Parcel area in hectares |

---

### Table: data_source

The `data_source` table documents the provenance of datasets used in the system.

| Column | Description |
|------|------------|
| id | Unique data source identifier (PK) |
| name | Name of the data source |
| provider | Data provider organisation |
| licence | Data usage licence |

---

## Observational entities

### Table: weather_observation

The `weather_observation` table stores climate variables derived from ERA5 reanalysis data and associated with parcels.

| Column | Description |
|------|------------|
| id | Unique weather observation identifier (PK) |
| parcel_id | Reference to the parcel (FK) |
| source_id | Reference to the data source (FK) |
| observation_time | Date and time of observation |
| air_temperature_c | Air temperature (°C) |
| dewpoint_temperature_c | Dew point temperature (°C) |
| relative_humidity_pct | Relative humidity (%) |
| precipitation_m | Total precipitation (m) |
| solar_radiation_jm2 | Surface solar radiation (J/m²) |
| wind_u_10m | Zonal wind component (m/s) |
| wind_v_10m | Meridional wind component (m/s) |
| evaporation_m | Evaporation (m) |

---

### Table: vegetation_index

The `vegetation_index` table stores NDVI observations derived from Copernicus satellite products. Values represent regional vegetation conditions and are associated with parcels for analytical purposes.

| Column | Description |
|------|------------|
| id | Unique NDVI record identifier (PK) |
| parcel_id | Reference to the parcel (FK) |
| source_id | Reference to the data source (FK) |
| observation_date | Date of observation |
| ndvi_mean | Mean NDVI value |

---

### Table: irrigation_log

The `irrigation_log` table stores simulated irrigation events representing vineyard management practices.

| Column | Description |
|------|------------|
| id | Unique irrigation event identifier (PK) |
| parcel_id | Reference to the parcel (FK) |
| irrigation_time | Date and time of irrigation |
| volume_liters | Applied irrigation volume (litres) |
| method | Irrigation method |
| notes | Additional notes |

---

## Analytical entities

### Table: analysis_result

The `analysis_result` table stores **derived analytical outputs** generated during the data use phase of the project. This table is not populated from external datasets or CSV files, but is instead filled using SQL queries over existing observational data.

It materialises vegetation vigor classifications and stress indicators derived from NDVI values, allowing analytical results to be stored and reused.

| Column | Description |
|------|------------|
| id | Unique analysis result identifier (PK) |
| parcel_id | Reference to the analysed parcel (FK) |
| observation_time | Date associated with the NDVI observation |
| vigor_class | Vegetation vigor classification (Low, Moderate, High) |
| stress_flag | Boolean indicator of potential vegetation stress |
| notes | Description of the analytical method |

### Data origin

- Type: Derived data
- Source: SQL-based queries over the `vegetation_index` table
- Population stage: Data use phase

---

## Referential integrity and constraints

- All tables use surrogate primary keys (`id`)
- Foreign key constraints enforce valid relationships between entities
- Observational and analytical records cannot exist without corresponding parcel references
- Data provenance is ensured through the `data_source` table

---

## Design compliance

The database design complies with:

- Third Normal Form (3NF)
- Course requirements for a relational Data Management System
- Separation of raw, processed, and derived data
- Reproducible and transparent analytical workflows

This design provides a robust foundation for data loading, analysis, and reporting within the scope of the project.
