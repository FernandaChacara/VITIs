# Metadata – Core structural entities

## Overview

This document describes the core structural entities of the database that support the Data Management System. These entities do not originate from external data repositories; instead, they were defined and created specifically for this project to enable relational integrity, user attribution, and data provenance across the system.

The tables documented here provide contextual and organisational structure for observational and analytical data.

## Scope of this metadata

This document covers the following tables:

- `user`
- `parcel`
- `data_source`

These tables are considered **structural entities** and are distinct from observational datasets such as weather, NDVI, or irrigation records.

---

## Table: user

### Purpose

The `user` table represents individuals or entities associated with vineyard parcels. It allows the attribution of parcels to users and supports potential multi-user scenarios within the system.

### Data origin

- Type: Simulated data
- Source: Project-defined
- Privacy: Personal identifiers are fictitious and used for academic purposes only

### Data dictionary

| Column name | Description | Data type |
|------------|------------|-----------|
| id | Unique identifier of the user | INT (PK) |
| name | User name | VARCHAR |
| email | Contact email address | VARCHAR |
| phone | Contact phone number | VARCHAR |
| affiliation | Organisational affiliation | VARCHAR |

---

## Table: parcel

### Purpose

The `parcel` table represents vineyard parcels located in the Alentejo region. It provides spatial and contextual information used to associate weather, vegetation, irrigation, and analysis data with specific parcels.

### Data origin

- Type: Simulated data
- Source: Project-defined
- Spatial context: Coordinates selected to represent vineyards in Alentejo, Portugal

### Data dictionary

| Column name | Description | Data type |
|------------|------------|-----------|
| id | Unique parcel identifier | INT (PK) |
| user_id | Reference to the associated user | INT (FK) |
| name | Parcel name | VARCHAR |
| region | Administrative region | VARCHAR |
| latitude | Latitude coordinate | DECIMAL |
| longitude | Longitude coordinate | DECIMAL |
| area_ha | Parcel area in hectares | FLOAT |

---

## Table: data_source

### Purpose

The `data_source` table documents the origin of each dataset used in the system. It supports data provenance by allowing observational records to be linked to their respective data providers.

### Data origin

- Type: Project-defined reference data
- Source: Manually created based on known data providers

### Data dictionary

| Column name | Description | Data type |
|------------|------------|-----------|
| id | Unique source identifier | INT (PK) |
| name | Name of the data source | VARCHAR |
| provider | Organisation providing the data | VARCHAR |
| licence | Data usage licence | VARCHAR |

---

## Notes

- These entities were created to support relational integrity and database normalisation.
- They do not represent external datasets and therefore do not require licensing, download format, or API documentation.
- All values were designed to be coherent with the analytical objectives of the project and aligned with the database schema.

