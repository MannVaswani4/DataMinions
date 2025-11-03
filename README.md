# Global Air Quality and Pollution Trends — OpenAQ Analysis

## Overview
Air pollution is one of the most serious global public health challenges. In this project, we analyze global air quality trends using data from the **OpenAQ Platform**, which aggregates real-time and historical air pollution measurements across cities and countries worldwide.

Our goal is to understand:
- How pollution varies across geographic regions
- How it has changed over time
- How socioeconomic development (e.g., GDP per capita) relates to pollution
- Whether certain pollutants correlate with each other
- Whether seasonal and urbanization trends exist
- Whether pollution levels can be predicted using statistical or machine learning models

This project also investigates potential links between pollution and health outcomes commonly associated with unclean air exposure.

---

## Data Source
**Primary Dataset**: OpenAQ Global Air Quality Database  
Website: https://explore.openaq.org  
API Docs: https://docs.openaq.org

Data collected from governments, research-grade sensors, embassies, and NGOs.

### Key Pollutants Measured
| Variable | Description |
|---------|-------------|
| PM2.5 | Particulate matter with diameter < 2.5 μm |
| PM10  | Particulate matter with diameter < 10 μm |
| NO2   | Nitrogen Dioxide |
| SO2   | Sulfur Dioxide |
| O3    | Ozone |
| CO    | Carbon Monoxide |

### Important Fields
| Field | Meaning |
|------|---------|
| location | Sensor / monitoring station name |
| city | Nearest city |
| country | Country code |
| value | Pollutant reading |
| unit | Measurement unit |
| datetime | Timestamp of measurement |
| coordinates | Latitude & longitude |

---

## Research Questions

1. Which countries and cities have the highest and lowest average pollution levels?
2. How has air quality changed over the last 20 years globally and regionally?
3. Do urbanized regions consistently show higher pollution than rural areas?
4. What is the relationship between **GDP per capita** and air pollution?
5. What seasonal variations exist in pollution levels?
6. How do pollutants correlate (e.g., PM2.5 vs PM10, NO2 vs SO2)?
7. How does air quality relate to respiratory disease and other health outcomes?
8. Can we predict future pollution levels using time-series or ML models?

---

## Methodology

### 1. Data Collection
We use the **OpenAQ API** to download measurement data in batches and aggregate it at city & yearly levels.

### 2. Data Cleaning
- Remove missing or invalid measurements
- Convert units where necessary
- Detect and handle outliers
- Aggregate to daily / monthly / yearly averages

### 3. Exploratory Data Analysis
- Regional comparison maps
- Seasonal variation plots
- Pollutant correlation heatmaps
- Time-based trend analysis

### 4. Predictive Modeling
Possible models:
- ARIMA / SARIMA (Time-series forecasting)
- Random Forest / XGBoost Regression

### 5. Interpretation & Reporting
Results will be documented with:
- Visual dashboards
- Written insights
- Presentation slides

---

## Project Structure
project/
│── data/
│ ├── raw/
│ ├── processed/
│
│── notebooks/
│ ├── 01_data_fetch.ipynb
│ ├── 02_cleaning.ipynb
│ ├── 03_eda_visualization.ipynb
│ ├── 04_modeling.ipynb
│
│── src/
│ ├── data_fetch.py
│ ├── preprocess.py
│ ├── visualize.py
│
│── README.md
│── requirements.txt


---

## Contributors & Work Allocation (for scoring)
| Name | Role | Responsibility |
|------|------|----------------|
| Member 1 | Data Engineering Lead | Data Downloading + Preprocessing |
| Member 2 | Visualization + Dashboarding | Interactive Charts & EDA |
| Member 3 | Modeling + Analysis | Statistical Tests + Prediction |
| Member 4 | Documentation + Report Lead | Final Report + Presentation |

Leadership rotates every phase.

---

