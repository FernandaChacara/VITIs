Data Management System for Vineyard Monitoring
Documentation and Implementation Guide
1. Project Overview

This project implements a Data Management System (DMS) to support the exploratory analysis of vineyard vegetation conditions, climatic context, and irrigation practices in the Alentejo region (Portugal).

The system integrates remote sensing indicators, climate observations, and management data within a relational database, enabling structured data storage and SQL-based analysis. The project is aligned with the Fundamentals of Agro-Environmental Data Science (FADS) project, ensuring consistency across assignments.

2. Problem Definition

The objective of this data management system is to support the analysis of vegetation conditions and irrigation practices at parcel level, within a regional environmental context.

The system is designed to answer the following guiding questions:

How do regional vegetation conditions (NDVI) vary over time in the context of vineyard parcels?

Are there differences in NDVI values associated with different parcels?

What climatic conditions are associated with periods of low vegetation vigor?

How frequently are irrigation events applied across parcels?

How do irrigation practices relate to observed NDVI patterns?

The focus of this project is data integration and exploratory analysis, not prediction or causal inference.

3. Data Identification and Collection

The project integrates data from multiple sources, both real and simulated.

3.1 Copernicus NDVI

Organisation: Copernicus Programme (European Commission)

Licence: Open Access

Domain: Remote sensing / vegetation indices

Description: NDVI time series at regional scale (Alentejo), used as an indicator of vegetation vigor.

Format: CSV (processed from original satellite products)

Note: NDVI data represents regional vegetation conditions, not parcel-level measurements.

3.2 ERA5 Climate Data

Organisation: ECMWF (Copernicus Climate Data Store)

Licence: CDS Licence

Domain: Climate and meteorology

Description: Reanalysis data including temperature, precipitation, evaporation, and wind variables.

Format: NetCDF (converted to CSV after processing)

3.3 Irrigation Records (Simulated)

Organisation: Project-generated

Licence: Internal / academic use

Domain: Agricultural management

Description: Simulated irrigation events representing plausible irrigation practices at parcel level.

Format: CSV

3.4 Structural Data

Additional tables (user, parcel, data_source) were created to represent administrative and relational entities required to support the database design.

4. Data Cleaning and Transformation

Raw data from external sources was not directly suitable for database import. The following steps were performed:

Conversion of raw data into structured CSV files

Normalisation of column names and units

Conversion and standardisation of date and time formats

Selection and aggregation of relevant variables

Preparation of intermediate datasets for SQL import

All cleaning and transformation steps were implemented using Python scripts, and the resulting files are stored in the processed_data/ directory.

5. Database Design

The database was designed as a relational schema compliant with the Third Normal Form (3NF).

Main entities include:

user

parcel

data_source

weather_observation

vegetation_index

irrigation_log

analysis_result

Primary keys, foreign keys, and referential integrity constraints were defined to ensure data consistency. The DBMS used is MySQL/MariaDB.

The schema was implemented using SQL and documented in the script create_tables.sql.

6. Database Implementation

Database implementation followed a reproducible workflow:

Creation of the database schema (create_tables.sql)

Import of cleaned and structured data using SQL (load_data.sql)

Validation of imported data using record counts and sample queries

All data imports were performed using SQL statements, in accordance with the assignment requirements.

7. Data Use and Analysis

Data exploration and analysis are performed using SQL queries contained in data_use.sql.

These queries support:

Temporal inspection of NDVI values

Spatial comparison between parcels

Integration of NDVI with climate variables

Analysis of irrigation frequency and volume

Exploratory assessment of NDVI variability and irrigation context

The queries are intended to demonstrate the analytical capability of the data management system, rather than to produce predictive or causal results.

8. Limitations

NDVI data represents regional vegetation conditions and was associated with parcels for exploratory purposes only.

Parcel-level NDVI extraction would require spatial intersection between parcel geometries and satellite pixels, which is outside the scope of this project.

Irrigation data is simulated and intended for methodological demonstration.

9. How to Run the Project from Scratch

Create the database schema:

SOURCE sql_scripts/create_tables.sql;


Load all data into the database:

SOURCE sql_scripts/load_data.sql;


Run data exploration queries:

SOURCE data_use_scripts/data_use.sql;

10. Project Structure
project_root/
 ├── original_data/
 ├── processed_data/
 ├── sql_scripts/
 │    ├── create_tables.sql
 │    └── load_data.sql
 ├── data_use_scripts/
 │    └── data_use.sql
 ├── documentation/
 │    └── README.md
 └── database_dump/

11. Final Remarks

This documentation provides all necessary information to understand, implement, and use the data management system. The project demonstrates the full data lifecycle, from data acquisition to data use, in accordance with the requirements of the Data Management Systems assignment.