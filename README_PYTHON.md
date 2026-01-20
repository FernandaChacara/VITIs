# VITIS — Precision Water Stress Intelligence for Mediterranean Vineyards

## Introduction to Python  
MSc Green Data Science | Instituto Superior de Agronomia (ISA)

---

## 1. Project Overview

**VITIS** is a Python-based **Decision Support System (DSS)** designed to assess and monitor **vineyard water stress** under Mediterranean climatic conditions.  
The project integrates vegetation indices and climate data to generate parcel-level indicators that support informed decision-making in viticulture.

The system focuses on:
- Data integration from heterogeneous sources
- Domain modelling through object-oriented design
- Computation of water stress indicators
- Generation of analytical outputs and visualizations
- Automated testing using pytest


---

## 2. Data and Problem Description

Mediterranean vineyards are increasingly exposed to water scarcity and heat stress due to climate change.  
Early detection of water stress is critical for maintaining vine health, yield stability, and grape quality.

The VITIS DSS addresses this problem by combining:
- **NDVI (Normalized Difference Vegetation Index)** data as a proxy for vegetative vigor
- **Climate data**, particularly air temperature
- **Parcel metadata** describing vineyard units

The output is a set of indicators that quantify current and short-term projected water stress at the parcel level.

---

## 3. Project Structure

VITIS/
│
├── project.py # Main application and core logic
├── test_project.py # Automated tests (pytest)
├── requirements.txt # Project dependencies
├── README.md # Project documentation
│
├── processed_data/ # Pre-processed NDVI and climate data
├── original_data/ # Parcel metadata
├── outputs/ # Generated results and visualizations
└── notebooks/ # Exploratory analysis 


---

## 4. Code Description

### 4.1 Main Script (`project.py`)

The file `project.py` contains:
- A `main()` function that orchestrates the entire workflow
- Custom functions defined at top level
- A domain model implemented as a Python class

#### Key components:

**Data Loading Functions**
- `load_ndvi_data()`
- `load_climate_data()`
- `load_parcel_data()`

These functions read structured CSV files and prepare the data for analysis.

**Validation Functions**
- Ensure required columns exist
- Apply basic data sanity checks

**Integration Function**
- `integrate_data(ndvi, climate, parcels)`  
  Merges NDVI, climate, and parcel datasets into a unified dataframe.

**Processing Functions**
- `build_parcels(df)`  
  Creates parcel-level objects using object-oriented design.
- `process_parcels(vineyard_parcels)`  
  Computes DSS indicators for each parcel.

**Domain Model**
- `VineyardParcel` class  
  Encapsulates parcel-level logic, including:
  - Vegetative vigor computation
  - Water stress calculation
  - Stress classification
  - Short-term forecast

**Outputs**
- CSV file with DSS indicators
- Spatial risk map (PNG)
- Optional parcel-level alert reports

---

## 5. How to Run the Project

### 5.1 Install Dependencies

From the project root, install the required packages:

```bash
pip install -r requirements.txt
```
## 5.2 Run the Application

Execute the main script with:

```bash
python project.py
````
This will:

- Load and validate the data  
- Compute water stress indicators  
- Generate output files in the `outputs/` directory  

The application runs without requiring manual user input.

---
## 6. Testing

### 6.1 Test Strategy

Automated tests were implemented using **pytest**, covering:

- Core functions (unit tests)  
- Domain model methods  
- Edge cases (e.g., missing data)  
- End-to-end pipeline validation  

Synthetic and deterministic datasets are used to ensure reproducibility and independence from external files or services.

---

### 6.2 Running the Tests

To execute all tests:

```bash
pytest
```
To display informative messages from functional tests:

```bash
pytest -s
```
All tests pass successfully, validating the correctness and robustness of the DSS pipeline.

---

## 7. Requirements

The project depends only on external, pip-installable libraries:

- pandas
- matplotlib
- pytest


Modules from the Python standard library are intentionally excluded from `requirements.txt`.

---

## 8. Improvements and Future Work

Future developments of VITIS could include:

Integration of additional climate variables (e.g., precipitation, evapotranspiration)

Inclusion of spatial data layers and GIS-based analysis

Export of comprehensive reports (e.g., PDF summaries)

Development of a user-facing interface for vineyard managers

## 9. Potential Issues

The current implementation assumes that all input data files are available and correctly formatted.
Further validation layers could be implemented to improve robustness when dealing with heterogeneous or incomplete datasets.

---

## Author

- Fernada Chácara
- Dandara França
- Catarina Silva

MSc Green Data Science  
Instituto Superior de Agronomia (ISA)
