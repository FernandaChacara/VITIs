# Problem Definition

## Context

Mediterranean viticulture is highly dependent on climatic conditions and water availability. In regions such as Alentejo (Portugal), vineyards are increasingly exposed to periods of water stress driven by high temperatures, low precipitation, and high evaporative demand. At the same time, irrigation practices play a central role in mitigating these impacts, but require adequate information to support decision making.

The availability of heterogeneous data sources, including remote sensing indicators, climate reanalysis products, and farm management records, creates the need for an integrated data management system capable of structuring, storing, and supporting the analysis of such data in a coherent and reproducible way.

This project addresses that need by developing a relational Data Management System that integrates vegetation, climate, and irrigation data for exploratory analysis in a viticultural context.

---

## Problem Statement

The core problem addressed by this project is the lack of a unified and structured data system to support the exploratory analysis of vegetation conditions and irrigation practices in vineyards, using heterogeneous environmental and management data sources.

Specifically, the challenge lies in integrating:
- regional-scale vegetation indicators derived from remote sensing,
- climatic observations describing atmospheric conditions,
- parcel-level irrigation records and structural information,

within a single relational database that ensures data consistency, traceability, and analytical usability.

---

## Objectives

The main objective of this Data Management System is to support exploratory analysis of vineyard vegetation conditions and irrigation practices at parcel level, within a regional environmental context.

To achieve this goal, the system is designed to:
- store and manage data from multiple heterogeneous sources,
- ensure data consistency through relational constraints,
- support temporal and spatial queries using SQL,
- enable the inspection of relationships between vegetation indicators, climate variables, and irrigation activity.

The focus of the project is on data organisation, integration, and use, rather than on predictive modelling or causal inference.

---

## Analytical Questions

The implementation of the database is guided by a set of analytical questions that the system should be able to support:

1. How do regional vegetation conditions, represented by NDVI, vary over time in the context of vineyard parcels?
2. Are there differences in NDVI values associated with different parcels, reflecting spatial variability in regional vegetation conditions?
3. What climatic conditions are associated with periods of low vegetation vigor?
4. How frequently are irrigation events applied across parcels, and how do irrigation volumes vary?
5. How do irrigation practices relate to NDVI values associated with parcels within a regional vegetation context?
6. Are there parcels associated with higher temporal variability of NDVI values?
7. Are there situations where low NDVI values occur in the absence of recent irrigation activity?

These questions are exploratory in nature and are intended to demonstrate the analytical capabilities of the data management system through SQL-based queries.

---

## Scope and Limitations

The NDVI data used in this project corresponds to a regional-scale remote sensing product for the Alentejo region. NDVI values are associated with vineyard parcels to provide contextual information, but do not represent parcel-level NDVI measurements derived from spatial intersection with parcel geometries.

As a result, the analyses supported by this system are exploratory and descriptive. Parcel-level biophysical interpretation of NDVI would require higher spatial resolution data and spatial processing workflows that are outside the scope of this assignment.

---

## Relation to the FADS Project

This Data Management System is aligned with the broader objectives of the associated Fundamentals of Agro-Environmental Data Science (FADS) project. While the FADS project focuses on modelling and predictive analysis, the present work concentrates on the design, implementation, and use of a robust data infrastructure to support such analyses.

By structuring and integrating the relevant datasets, this project provides a foundational data layer that can be reused and extended in future data science workflows.
