# Database Design – VITIs Project

## Overview

This document describes the relational database design proposed for the VITIs data management system. The schema was designed to support agro-environmental analysis, with a focus on climate and vegetation monitoring for viticultural parcels.

The database follows relational best practices and is compliant with the Third Normal Form (3NF).

---

## Entities

### User

Represents users of the system.

Main attributes:

* `id` (PK)
* `name`
* `email`

---

### Parcel

Represents agricultural parcels associated with users.

Main attributes:

* `id` (PK)
* `user_id` (FK)
* `name`
* `region`
* `latitude`
* `longitude`

Each parcel belongs to a single user, while a user may manage multiple parcels.

---

### Data Source

Catalogues the origin of external and internal datasets used by the system.

Main attributes:

* `id` (PK)
* `name`
* `provider`
* `licence`

This entity allows traceability and documentation of data provenance.

---

### Weather Observation

Stores climate observations associated with parcels and time.

Main attributes:

* `id` (PK)
* `parcel_id` (FK)
* `source_id` (FK)
* `observation_time`
* `air_temperature_c`
* `dewpoint_temperature_c`
* `relative_humidity_pct`
* `precipitation_m`
* `solar_radiation_jm2`
* `wind_u_10m`
* `wind_v_10m`
* `evaporation_m`

Each record represents a climatic observation for a given parcel at a specific time.

---

### Vegetation Index

Stores vegetation indicators derived from remote sensing data.

Main attributes:

* `id` (PK)
* `parcel_id` (FK)
* `source_id` (FK)
* `observation_time`
* `ndvi_mean`

This table is designed to support vegetation monitoring and future integration of additional indices.

---

### Analysis Result

Stores derived indicators and classifications generated from climatic and vegetation data.

Main attributes:

* `id` (PK)
* `parcel_id` (FK)
* `observation_time`
* `vigor_class`
* `stress_flag`
* `notes`

This entity separates raw observations from analytical outputs.

---

## Relationships

* User (1) — (N) Parcel
* Parcel (1) — (N) Weather Observation
* Parcel (1) — (N) Vegetation Index
* Parcel (1) — (N) Analysis Result
* Data Source (1) — (N) Weather Observation
* Data Source (1) — (N) Vegetation Index

Foreign keys are used to enforce referential integrity between entities.

---

## Keys and Constraints

* All tables use surrogate primary keys (`id`).
* Foreign keys ensure consistency between related entities.
* Temporal information is stored using the `DATETIME` type.
* Numeric variables use appropriate numeric types (`FLOAT`, `DOUBLE`).

---

## Normalization

The database schema complies with the Third Normal Form (3NF):

* Each table represents a single entity or concept.
* Non-key attributes depend only on the primary key.
* No transitive dependencies exist between non-key attributes.

This design ensures data integrity, avoids redundancy, and supports efficient querying and future extensibility.
