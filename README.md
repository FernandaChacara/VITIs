VITIs — Predictive Water-Stress Monitoring System for Mediterranean Vineyards
Overview

VITIs is a desktop-first application (with a simplified mobile version) designed to monitor and predict intra-parcel water stress in Mediterranean vineyards. It integrates multispectral, meteorological, phenological and field-based observations into a harmonized analytical workflow capable of delivering 3–7-day stress forecasts and spatially explicit decision-support outputs.

The application operationalizes the methodological framework and scientific foundations presented in Sustainable Water Management in Mediterranean Vineyards , translating an academic data-science workflow into a functional decision-support tool for sustainable irrigation management.

Key Features

Short-term water-stress prediction using supervised machine-learning models.

Spatial visualization of stress patterns through NDVI/NDRE-based maps.

Integration of atmospheric demand indicators (VPD, GDD, temperature, humidity).

Phenological alignment using BBCH stages for physiologically coherent predictions.

Interactive analytics dashboard with maps, temporal charts, variable summaries and tooltips.

Desktop application for complete analysis + mobile interface for in-field consultation.

Support for ground-truth annotation for iterative validation and model refinement.

Scientific and Conceptual Basis

The project builds upon environmental data-science principles, particularly:

Multisource data integration (Sentinel-2, weather stations/ERA5, scouting, soil/topography).

Semantic harmonization and temporal synchronization, addressing heterogeneity and alignment challenges frequently described in Environmental Data Science literature.

DIKW-oriented structuring, moving from raw data to actionable knowledge through validated evidence and interpretability.

Physiological relevance, ensuring predictions reflect vine responses under Mediterranean climatic constraints, as outlined in the project report.
VITIs/
│
├── data/
│   ├── raw/                  # Multispectral, meteorological and field data
│   ├── processed/            # Harmonized and cleaned datasets
│   └── features/             # Derived indicators (NDVI, NDRE, VPD, GDD, etc.)
│
├── modelling/
│   ├── notebooks/            # Exploratory and modelling workflows
│   ├── models/               # Trained prediction models
│   └── evaluation/           # Performance and validation reports
│
├── app/
│   ├── desktop/              # Main analytical interface
│   ├── mobile/               # Simplified version for field use
│   └── assets/               # Icons, color scales, UI resources
│
├── docs/
│   ├── methodology/          # Methodological notes and diagrams
│   └── report.pdf            # Full academic report
│
└── README.md
Data Sources

Sentinel-2 multispectral imagery: NDVI, NDRE and red-edge indicators for canopy condition.

Meteorological variables: temperature, humidity, precipitations, VPD, GDD (weather stations or ERA5).

Phenological observations: BBCH scale for temporal alignment.

Field scouting: canopy symptoms, soil conditions, ground truth.

Soil and topographic layers: texture, OM content, depth, slope.

These heterogeneous sources are pre-processed following the data-quality procedures detailed in the report .

Methodological Workflow
1. Pre-Processing

Atmospheric correction and cloud masking of Sentinel-2 imagery.

Temporal synchronization between imagery, weather data and phenology.

Spatial harmonization with soil/topography.

Filtering, interpolation and imputation of missing environmental data.

Feature engineering: NDVI/NDRE, cumulative GDD, moving averages of VPD, rainfall windows, morphological indices.

2. Modelling

Supervised learning using Random Forest and Gradient Boosting, selected for:

Robustness to heterogeneity and multicollinearity

High interpretability

Strong performance with medium-scale environmental datasets

Temporal and spatial cross-validation to ensure generalization across vineyard zones and phenological stages.

3. Prediction and Output Generation

Pixel-level stress prediction (3–7 days lead time).

Export of georeferenced maps and tabular outputs.

Integration with the app for visualization and interpretation.

Application Design
Desktop Interface

Map viewer with intra-parcel resolution.

Filters by date, phenological stage and variable of interest.

Charts linking predicted stress to NDVI/NDRE, VPD, GDD and other drivers.

Explanatory panels highlighting key physiological insights.

Export of annotated maps and analytical summaries.

Mobile Interface

Simplified view optimized for field use.

Quick access to stress warnings, notes and recent predictions.

Option to add field photos or observations linked to coordinates.

Target Users

Vineyard technicians

Production and irrigation managers

Precision-viticulture consultants

Sustainability officers

Researchers in agri-environmental data science

Limitations

As discussed in the project report :

Limited temporal frequency of ground-truth water-status measurements.

Spatial constraints of Sentinel-2 (10–20 m) for fine-scale heterogeneity.

Dependence on accurate phenological alignment.

Variable digital literacy among end users, requiring training sessions.

Future Development

Incorporation of deep-learning architectures for temporal forecasting.

Integration with IoT soil-moisture or canopy-temperature sensors.

Automated ET-based irrigation recommendations.

Cloud-based version for multi-parcel data management.

Real-time alert systems (SMS, WhatsApp, Telegram).

Authors

Fernanda Chácara

Dandara França

Catarina Silva
Developed within the UC Fundamentals of AgroEnvironmental Data Science (ISA).
Scientific foundations documented in the full project report.


License

MIT License (modifiable upon request).
