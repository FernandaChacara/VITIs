# Project Overview

## Context

This project implements a Data Management System (DMS) designed to support agro-environmental analysis in a viticulture context. The system integrates vegetation, climate, irrigation, and structural data to enable exploratory analysis of vineyard conditions in the Alentejo region, Portugal.

The project is aligned with the objectives of the Data Management Systems course and is conceptually connected to the FADS project, allowing the reuse and integration of data sources and analytical perspectives.

## Problem context

Viticulture management increasingly relies on heterogeneous data sources, such as satellite-derived vegetation indices, climate reanalysis products, and field management records. These data are often stored separately, lack relational structure, and are not easily queried in an integrated manner.

The absence of a structured data management system limits the ability to:
- Analyse vegetation dynamics over time
- Relate vegetation conditions to climatic drivers
- Assess irrigation practices in relation to vegetation status
- Perform consistent, reproducible data analysis using SQL

This project addresses this gap by designing and implementing a relational database that consolidates these data sources into a coherent system.

## Project objectives

The main objectives of this Data Management System are:

- To design a relational database in Third Normal Form suitable for agro-environmental analysis
- To integrate real and simulated data from multiple sources
- To document all stages of the data lifecycle, from data collection to data use
- To support analytical questions related to vegetation vigor, climate conditions, and irrigation practices using SQL queries

## Domain and data scope

The system focuses on vineyard parcels located in the Alentejo region and integrates the following types of data:

- Vegetation indices (NDVI) derived from Copernicus satellite products
- Climate observations derived from ERA5 reanalysis data
- Simulated irrigation records representing management practices
- Structural entities representing users, parcels, and data sources

All datasets are either real open-access data or simulated for academic purposes.

## Database structure overview

The database is composed of the following main entity groups:

- Structural entities: `user`, `parcel`, `data_source`
- Observational entities: `weather_observation`, `vegetation_index`, `irrigation_log`
- Analytical entities: `analysis_result`

These entities are linked through primary and foreign key relationships to ensure referential integrity and support complex queries.

## Documentation structure

The `documentation/` directory is organised as follows:

- `00_project_overview.md` – Project context and overview
- `01_problem_definition.md` – Analytical questions guiding the system
- `02_metadata_weather.md` – Metadata for ERA5 weather observations
- `03_metadata_ndvi.md` – Metadata for NDVI vegetation observations
- `04_metadata_irrigation.md` – Metadata for irrigation records
- `05_database_design.md` – Database schema and design rationale
- `06_how_to_run.md` – Instructions to run the system from scratch
- `07_metadata_core_entities.md` – Metadata for structural entities

## Intended use

This Data Management System is intended for analytical and educational purposes. It demonstrates best practices in data modelling, data integration, and SQL-based analysis within an agro-environmental context.
