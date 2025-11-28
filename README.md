# **VITIs — Predictive Water-Stress Monitoring System for Mediterranean Vineyards**

## **Overview**
VITIs is a desktop-first application (with a simplified mobile version) designed to monitor and predict **intra-parcel water stress** in Mediterranean vineyards. It integrates multispectral, meteorological, phenological, and field-based observations into a harmonized analytical workflow capable of delivering **3–7-day stress forecasts** and spatially explicit decision-support outputs.

The system operationalizes the scientific and methodological framework presented in *Sustainable Water Management in Mediterranean Vineyards* :contentReference[oaicite:0]{index=0}, translating an academic data-science workflow into a functional tool for sustainable irrigation management.

---

## **Key Features**
- Short-term (3–7 days) prediction of water stress using supervised ML models  
- Spatial visualization of intra-parcel variability (NDVI/NDRE)  
- Integration of atmospheric demand indicators (VPD, GDD, temperature, humidity)  
- Phenological alignment using BBCH stages  
- Interactive dashboard with maps, temporal charts, variable explanations  
- Full desktop application + simplified mobile version for in-field use  
- Support for ground-truth annotation and iterative model improvement  

---

## **Scientific and Conceptual Basis**
The project applies principles from Environmental Data Science and DIKW-oriented frameworks, emphasizing:

- Multisource integration (Sentinel-2, weather stations/ERA5, scouting, soil, topography)  
- Semantic harmonization and temporal synchronization of heterogeneous datasets  
- Emphasis on interpretability and physiological coherence under Mediterranean conditions  
- Structuring results from raw data → validated evidence → actionable knowledge  
:contentReference[oaicite:1]{index=1}

---

## **Project Structure**

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

## **Data Sources**
- **Sentinel-2 imagery:** NDVI, NDRE, red-edge vegetation indices  
- **Meteorological data:** temperature, humidity, precipitation, VPD, GDD  
- **Phenological information:** BBCH stages  
- **Field scouting:** canopy symptoms, soil surface conditions, manual observations  
- **Soil & topography:** texture, OM, depth, slope  

These sources follow the preprocessing strategy documented in the project report.  
:contentReference[oaicite:2]{index=2}

---

## **Methodological Workflow**

### **1. Pre-Processing**
- Atmospheric correction and cloud masking  
- Temporal synchronization of imagery, weather data, and phenology  
- Spatial harmonization with soil/topography layers  
- Noise filtering, gap-filling, and imputation  
- Feature engineering: NDVI/NDRE, cumulative GDD, VPD windows, rainfall indicators  

### **2. Modelling**
- Supervised learning using **Random Forest** and **Gradient Boosting**, selected for:
  - Robustness to heterogeneous environmental datasets  
  - High interpretability  
  - Good performance with medium-sized spatiotemporal data  
- Temporal and spatial cross-validation to ensure generalizability  

### **3. Prediction & Output Generation**
- Pixel-level stress prediction for short-term horizons  
- Export of georeferenced maps and tabular outputs  
- Integration into the application dashboard  

---

## **Application Design**

### **Desktop Interface**
- Interactive map viewer  
- Filters for date, phenological stage, and variable  
- Temporal charts linking predicted stress to NDVI/NDRE, VPD, GDD  
- Explanatory components and tooltips  
- Export of reports and annotated maps  

### **Mobile Interface**
- Simplified map and indicator view  
- Quick access to stress alerts  
- Field notes and photo annotation support  

---

## **Target Users**
- Vineyard technicians  
- Irrigation and production managers  
- Precision-viticulture consultants  
- Sustainability officers  
- Researchers in agri-environmental data science  

---

## **Limitations**
Acknowledged in the report:  
:contentReference[oaicite:3]{index=3}  
- Limited temporal frequency of ground-truth water-status measurements  
- Sentinel-2 spatial resolution may not capture fine-scale variability  
- Dependence on accurate phenological alignment  
- Variability in digital literacy among end users  

---

## **Future Development**
- Deep learning for enhanced temporal forecasting  
- Integration with IoT sensors (soil moisture, canopy temperature)  
- Irrigation optimization simulations  
- Cloud-based multi-parcel management  
- Real-time alerting (SMS/Telegram)  

---

## **Authors**
- **Fernanda Chácara**  
- **Dandara França**  
- **Catarina Silva**  

Developed within the UC *Fundamentals of AgroEnvironmental Data Science (ISA)*.  
Scientific foundations documented in the full project report.  
:contentReference[oaicite:4]{index=4}

---

## **License**
MIT License.
