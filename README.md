# VITIs — Predictive Water-Stress Monitoring System for Mediterranean Vineyards

VITIs is a desktop-first application (with a simplified mobile version) designed to monitor and predict intra-parcel water stress in Mediterranean vineyards. It integrates multispectral imagery, meteorological data, phenology, and ground-based observations into a unified workflow capable of generating 3–7-day water-stress forecasts.

---

## 📌 Overview

The system operationalizes a scientific framework grounded in Environmental Data Science, precision viticulture, and DIKW-style conceptual models.  
It converts heterogeneous observations into validated evidence and actionable indicators for sustainable irrigation management.

This repository contains:
- the analytical workflow  
- modelling scripts  
- the VITIs desktop/mobile interface  
- documentation and methodological report  

---

## 📱 Application Preview (GIFs)

### **Mobile Interface**
<p align="center">
  <img src="app/assets/iphone-coin-spin.gif" width="300">
</p>

---

### **Desktop Interface**
<p align="center">
  <img src="app/assets/simple-macbook-pro-m3-14-inch.gif" width="700">
</p>

---

## ⭐ Key Features

- Short-term (3–7 days) water-stress prediction using supervised ML models  
- Spatial visualization of intra-parcel variability (NDVI, NDRE, red-edge indices)  
- Integration of atmospheric demand indicators (VPD, GDD, temperature, humidity)  
- Phenological alignment using BBCH stages  
- Interactive dashboard with maps, charts and contextual tooltips  
- Desktop interface for full analysis + simplified mobile interface for field use  
- Ground-truth annotation and iterative model improvement  

---

## 🔬 Scientific Foundation

The modelling pipeline is inspired by Environmental Data Science principles:

- **Multisource integration** (Sentinel-2, ERA5, meteorological stations, field scouting, soil and topography)  
- **Semantic harmonization** and temporal synchronization  
- **Feature engineering** consistent with Mediterranean vine physiology  
- **Conversion of DATA → EVIDENCE → KNOWLEDGE**, following DIKW-inspired reasoning  

---

## 🧠 Methodological Workflow

### **1. Preprocessing**
- Atmospheric correction & cloud masking  
- Temporal alignment (imagery × weather × phenology)  
- Spatial harmonization (soil, DEM, topography)  
- Noise filtering, interpolation, gap-filling  
- Engineered features: NDVI, NDRE, VPD windows, cumulative GDD, rainfall indices  

### **2. Modelling**
Algorithms:
- Random Forest  
- Gradient Boosting  

Validation strategy:
- Temporal cross-validation  
- Spatial block cross-validation  

### **3. Outputs**
- Pixel-level water-stress predictions (3–7 days)  
- Georeferenced maps & exportable tables  
- Integrated dashboard visualization  

---

## 📁 Repository Structure


VITIs/
│
├── data/
│ ├── raw/
│ ├── processed/
│ └── features/
│
├── modelling/
│ ├── notebooks/
│ ├── models/
│ └── evaluation/
│
├── app/
│ ├── desktop/
│ ├── mobile/
│ └── assets/
│
└── docs/
├── methodology/
└── report.pdf


---

## 🎯 Target Users

- Vineyard technicians and irrigation managers  
- Precision-viticulture consultants  
- Sustainability teams  
- Researchers and students in agro-environmental data science  

---

## ⚠️ Current Limitations

- Limited temporal frequency of ground-truth water-status measurements  
- Sentinel-2 resolution insufficient for fine-scale canopy variability  
- Dependence on accurate phenology (BBCH staging)  
- Digital literacy variability among end-users  

---

## 🚀 Future Work

- Deep-learning models for extended prediction horizons  
- IoT integration (soil moisture, canopy thermography)  
- Irrigation optimization algorithms  
- Cloud-based multi-parcel management interface  
- Real-time alerts (SMS/Telegram)  

---

## 👩‍💻 Authors

- **Fernanda Chácara**  
- **Dandara França**  
- **Catarina Silva**

Developed under the UC **Fundamentals of Agro-Environmental Data Science (ISA/ULisboa)**.

---

## 📄 License
MIT License.


