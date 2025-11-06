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

## 🎯 Problem Understanding

### Why Air Quality Matters
Air pollution is responsible for approximately **7 million premature deaths annually** worldwide (WHO, 2021). Particulate matter (PM2.5 and PM10), nitrogen dioxide (NO₂), sulfur dioxide (SO₂), ozone (O₃), and carbon monoxide (CO) pose severe risks to human health, contributing to respiratory diseases, cardiovascular problems, and reduced life expectancy.

Despite global awareness, air quality remains a critical challenge, particularly in rapidly developing regions. Understanding pollution patterns, their drivers, and temporal trends is essential for:
- **Public Health Policy**: Informing regulations and interventions
- **Environmental Justice**: Identifying disproportionately affected communities
- **Climate Action**: Linking pollution to broader environmental goals
- **Predictive Planning**: Forecasting pollution events for early warnings

### Motivation for Dataset Selection

#### OpenAQ Platform
We chose **OpenAQ** as our primary data source because:
- **Global Coverage**: Data from 100+ countries and thousands of monitoring stations
- **Real-Time Updates**: Hourly measurements enable temporal analysis
- **Open Access**: Free, publicly available data aligned with open science principles
- **Standardized Format**: Consistent data structure facilitates cross-country comparisons
- **Community-Driven**: Aggregates government, research, and citizen science data

#### World Bank Open Data
We supplement OpenAQ with **World Bank** socioeconomic indicators to:
- Explore relationships between economic development (GDP per capita) and pollution
- Analyze urbanization's impact on air quality
- Investigate health expenditure and pollution-related mortality
- Test the **Environmental Kuznets Curve** hypothesis

### Significance of This Study
This project bridges **environmental science**, **public health**, and **data science** by:
1. Providing evidence-based insights into global pollution trends
2. Testing innovative hypotheses about pollution drivers
3. Building predictive models for air quality forecasting
4. Demonstrating practical applications of data mining techniques

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

## 🔬 Research Questions

Our analysis is guided by the following well-defined research questions:

### Geographic Analysis
1. **Which countries and cities have the highest and lowest average pollution levels?**
   - Identify global pollution hotspots and clean air regions
   - Compare developed vs. developing nations

2. **Do urbanized regions consistently show higher pollution than rural areas?**
   - Quantify urban-rural pollution disparities
   - Analyze population density effects

### Temporal Analysis
3. **How has air quality changed over the last 20 years globally and regionally?**
   - Track long-term trends in PM2.5, NO₂, and other pollutants
   - Identify regions with improving vs. worsening air quality

4. **What seasonal variations exist in pollution levels?**
   - Detect winter vs. summer patterns
   - Analyze meteorological influences (temperature, precipitation)

### Socioeconomic Correlations
5. **What is the relationship between GDP per capita and air pollution?**
   - Test the Environmental Kuznets Curve hypothesis
   - Explore development-pollution trade-offs

6. **How does air quality relate to respiratory disease and other health outcomes?**
   - Correlate pollution levels with mortality rates
   - Estimate public health burden

### Pollutant Interactions
7. **How do pollutants correlate with each other?**
   - Analyze PM2.5 vs. PM10, NO₂ vs. SO₂, O₃ vs. NO₂
   - Identify common emission sources

### Predictive Modeling
8. **Can we predict future pollution levels using time-series or machine learning models?**
   - Build forecasting models for early warning systems
   - Evaluate model accuracy across different regions

---

## 💡 Innovative Hypotheses

Beyond standard descriptive analysis, we propose the following **exploratory hypotheses** to drive deeper insights:

### H1: Urbanization-Pollutant Relationship
**Hypothesis**: Urbanization correlates positively with PM2.5 and NO₂ (traffic-related) but negatively with O₃ (due to NO₂-O₃ titration effect in cities).

**Rationale**: Urban areas have high vehicular emissions (PM2.5, NO₂), but nitrogen oxides consume ozone, leading to lower O₃ in city centers compared to suburbs.

**Testing Method**: Regression analysis with urbanization rate as predictor; separate models for each pollutant.

---

### H2: Environmental Kuznets Curve for Air Pollution
**Hypothesis**: Countries with rapid GDP growth first experience a pollution rise, then a decline as they transition to cleaner technologies and stricter regulations.

**Rationale**: The Environmental Kuznets Curve (EKC) suggests an inverted U-shaped relationship between economic development and environmental degradation.

**Testing Method**: Polynomial regression of GDP per capita vs. PM2.5; identify inflection point.

---

### H3: Policy Impact Post-2015 Paris Agreement
**Hypothesis**: Air pollution reduction policies post-2015 (Paris Agreement) led to measurable improvements in air quality in developed regions (Europe, North America).

**Rationale**: International climate commitments incentivized cleaner energy transitions and stricter emission standards.

**Testing Method**: Time-series analysis with structural break detection at 2015; compare pre/post trends.

---

### H4: Seasonal Inversion Effect
**Hypothesis**: Winter months exhibit significantly higher PM2.5 due to thermal inversion, heating emissions, and reduced atmospheric mixing.

**Rationale**: Cold weather traps pollutants near the surface, and residential heating increases particulate emissions.

**Testing Method**: ANOVA comparing seasonal means; geographic stratification (temperate vs. tropical regions).

---

### H5: Weekend Effect on NO₂
**Hypothesis**: NO₂ levels are significantly lower on weekends due to reduced commercial traffic and industrial activity.

**Rationale**: Weekday commuting and freight transport are major NO₂ sources.

**Testing Method**: T-test comparing weekday vs. weekend NO₂ concentrations; control for seasonality.

---

## 📊 Methodology Overview

Our research follows a systematic, reproducible approach. For detailed methodology, see [`docs/methodology.md`](docs/methodology.md).

### 1. Data Collection
- **OpenAQ API**: Batch downloads of hourly measurements (2015-2025)
- **World Bank API**: Socioeconomic indicators (GDP, urbanization, health metrics)
- **Data Storage**: Raw data in `data/raw/`, processed data in `data/processed/`

### 2. Data Preprocessing
- **Missing Value Handling**: Linear interpolation for time-series gaps
- **Outlier Detection**: IQR method and domain knowledge (e.g., PM2.5 > 500 µg/m³)
- **Normalization**: StandardScaler for ML models
- **Feature Engineering**: Temporal features (season, day of week), AQI calculation, rolling averages
- **Implementation**: See [`notebooks/data_preprocessing.ipynb`](notebooks/data_preprocessing.ipynb)

### 3. Exploratory Data Analysis (EDA)
- **Geographic Visualization**: Choropleth maps, hotspot identification
- **Temporal Analysis**: Trend decomposition, seasonality detection
- **Correlation Analysis**: Pollutant correlation matrices, scatter plots
- **Tools**: Matplotlib, Seaborn, Plotly, Folium

### 4. Statistical Hypothesis Testing
- **Parametric Tests**: T-tests, ANOVA for group comparisons
- **Regression Analysis**: Linear, polynomial, multivariate models
- **Time Series Analysis**: Trend analysis, structural break detection
- **Significance Level**: α = 0.05

### 5. Predictive Modeling
- **Time Series Forecasting**: ARIMA, SARIMA, Prophet
- **Regression Models**: Random Forest, XGBoost, Neural Networks
- **Classification**: Air quality category prediction (Good, Moderate, Unhealthy, etc.)
- **Evaluation**: Cross-validation, RMSE, MAE, R², F1-score

### 6. Interpretation & Reporting
- **Technical Report**: Detailed findings and statistical results
- **Interactive Dashboard**: Streamlit app for stakeholder exploration
- **Presentation**: Visual storytelling of key insights

**📖 Full Methodology**: See [`docs/methodology.md`](docs/methodology.md) for comprehensive details, literature review, and timeline.

---

## 🧹 Data Preprocessing Pipeline

Our preprocessing pipeline ensures data quality and prepares datasets for analysis:

1. **Load Raw Data**: CSV files or API responses
2. **Quality Assessment**: Missing value analysis, outlier detection
3. **Data Cleaning**: 
   - Handle missing values (interpolation, forward-fill)
   - Cap outliers at 99th percentile
   - Remove invalid records (negative values, missing timestamps)
4. **Feature Engineering**:
   - Extract temporal features (year, month, season, day of week)
   - Calculate Air Quality Index (AQI)
   - Compute rolling averages (7-day, 30-day)
5. **Normalization**: Scale features for ML models
6. **Validation**: Final quality checks and descriptive statistics
7. **Export**: Save cleaned data to `data/processed/`

**📓 Implementation**: See [`notebooks/data_preprocessing.ipynb`](notebooks/data_preprocessing.ipynb) for complete code with visualizations.

---

## 📁 Repository Structure

```
DataMinions/
├── data/                          # Data storage (gitignored)
│   ├── raw/                       # Raw data from OpenAQ API
│   └── processed/                 # Cleaned and preprocessed data
│
├── notebooks/                     # Jupyter notebooks for analysis
│   ├── 01_data_fetch.ipynb        # API data collection
│   ├── data_preprocessing.ipynb   # Comprehensive preprocessing pipeline ✨
│   ├── 03_eda_visualization.ipynb # Exploratory analysis (planned)
│   └── 04_modeling.ipynb          # Predictive models (planned)
│
├── src/                           # Python scripts for production
│   ├── data_fetch.py              # OpenAQ API wrapper
│   ├── data_cleaning.py           # Preprocessing utilities
│   ├── features.py                # Feature engineering
│   ├── models.py                  # ML model implementations
│   └── viz_streamlit.py           # Dashboard application
│
├── docs/                          # Documentation ✨
│   ├── team_plan.md               # Team roles and collaboration plan
│   └── methodology.md             # Detailed research methodology
│
├── reports/                       # Analysis reports
│   └── final_report.md            # Final project report
│
├── README.md                      # Project overview (this file)
├── requirements.txt               # Python dependencies
└── .gitignore                     # Git ignore rules
```

**✨ New additions for Evaluation 1**

---

## 👥 Team Members and Roles

| Name | GitHub | Current Role (Phase 1) | Responsibilities |
|------|--------|------------------------|------------------|
| **Aarav Sharma** | @aarav-sharma | 🔧 Data Engineering Lead | API integration, data collection, preprocessing pipeline, data quality assurance |
| **Priya Patel** | @priya-patel | 📊 Visualization & EDA Specialist | Exploratory analysis, interactive dashboards, chart design, pattern identification |
| **Rohan Kumar** | @rohan-kumar | 🤖 Modeling & Analysis Lead | Statistical testing, hypothesis validation, predictive modeling, model evaluation |
| **Ananya Singh** | @ananya-singh | 📝 Documentation & Reporting Lead | README maintenance, report writing, presentation prep, GitHub documentation |

### 🔄 Rotating Leadership Plan
Leadership rotates every **3 weeks** to ensure equal learning opportunities:
- **Phase 1 (Weeks 1-3)**: Aarav Sharma - Data Collection & Preprocessing
- **Phase 2 (Weeks 4-6)**: Priya Patel - EDA & Visualization
- **Phase 3 (Weeks 7-9)**: Rohan Kumar - Modeling & Hypothesis Testing
- **Phase 4 (Weeks 10-12)**: Ananya Singh - Final Report & Presentation

**📋 Detailed Plan**: See [`docs/team_plan.md`](docs/team_plan.md) for collaboration tools, commit guidelines, and meeting notes.

---

## 🎯 Project Objectives

1. **Analyze Global Pollution Trends**: Identify geographic and temporal patterns in air quality data
2. **Test Innovative Hypotheses**: Explore relationships between pollution, urbanization, and economic development
3. **Build Predictive Models**: Forecast future pollution levels for early warning systems
4. **Inform Policy Decisions**: Provide evidence-based insights for public health interventions
5. **Demonstrate Data Mining Skills**: Apply preprocessing, EDA, statistical testing, and ML techniques

---

## 🌐 Data Sources

### Primary: OpenAQ Platform
- **URL**: https://explore.openaq.org
- **API**: https://docs.openaq.org
- **Coverage**: 100+ countries, 10,000+ monitoring stations
- **Pollutants**: PM2.5, PM10, NO₂, SO₂, O₃, CO
- **Time Range**: 2015-2025 (10 years)
- **Update Frequency**: Hourly measurements

### Secondary: World Bank Open Data
- **URL**: https://data.worldbank.org
- **Indicators**:
  - GDP per capita (current US$)
  - Urban population (% of total)
  - Population density (people per sq. km)
  - Health expenditure (% of GDP)
  - Mortality rate attributed to air pollution
- **Purpose**: Socioeconomic correlation analysis

---

## 🤝 Contribution & Commit Guidelines

### Commit Convention
We follow a structured commit message format for clarity:
```
[TYPE] Brief description

Examples:
[FEAT] Add preprocessing pipeline for missing values
[FIX] Correct outlier detection threshold
[DOCS] Update README with hypothesis section
[DATA] Add World Bank GDP dataset
[TEST] Add unit tests for data cleaning functions
```

### Contribution Requirements
- **Minimum 2 commits per week** per team member
- Each member contributes to **at least 2 different aspects** (e.g., code + documentation)
- **Code reviews required** before merging to `main` branch
- All commits use individual GitHub accounts for proper attribution

### Branch Strategy
- `main` - Stable, reviewed code only
- `dev` - Active development branch
- Feature branches: `feature/data-fetch`, `feature/eda`, etc.

**📋 Full Guidelines**: See [`docs/team_plan.md`](docs/team_plan.md)

---

## 📈 Project Updates (Version Tracking)

### Version 1.0 - Evaluation 1 Preparation (2025-11-06)
**Status**: ✅ Ready for First Evaluation

**Completed**:
- ✅ Repository structure established
- ✅ Comprehensive README with problem understanding, hypotheses, and methodology
- ✅ Team plan with rotating leadership documented ([`docs/team_plan.md`](docs/team_plan.md))
- ✅ Detailed research methodology with literature review ([`docs/methodology.md`](docs/methodology.md))
- ✅ Data preprocessing notebook with complete pipeline ([`notebooks/data_preprocessing.ipynb`](notebooks/data_preprocessing.ipynb))
- ✅ `.gitignore` configured for data and cache files
- ✅ Requirements.txt with all dependencies

**Key Deliverables**:
1. **Work Planning (15 marks)**: Team roles, rotation plan, collaboration tools documented
2. **Problem Understanding (20 marks)**: Clear motivation, dataset justification, research questions
3. **Data Preprocessing (10 marks)**: Notebook with missing value handling, outlier detection, normalization
4. **Innovation in Hypotheses (20 marks)**: 5 unique, testable hypotheses with rationale
5. **Research Methodology (20 marks)**: Step-by-step plan, tools, literature review
6. **GitHub Hygiene (15 marks)**: Clean structure, .gitignore, descriptive commits

**Team Contributions**:
- Aarav Sharma: Data fetching scripts, preprocessing pipeline
- Priya Patel: Visualization planning, EDA framework
- Rohan Kumar: Hypothesis formulation, statistical test planning
- Ananya Singh: Documentation, README, methodology writing

---

### Version 0.1 - Initial Setup (2025-10-15)
- Initial repository creation
- Basic data fetching script
- Preliminary README

---

## 🚀 Next Steps (Evaluation 2 Preview)

### Phase 2: Exploratory Data Analysis (Weeks 4-6)
- [ ] Implement comprehensive EDA notebook
- [ ] Create geographic visualizations (choropleth maps, hotspot analysis)
- [ ] Generate temporal trend plots (yearly, seasonal, daily patterns)
- [ ] Build pollutant correlation analysis
- [ ] Develop interactive Streamlit dashboard

### Phase 3: Modeling & Hypothesis Testing (Weeks 7-9)
- [ ] Test all 5 hypotheses with statistical methods
- [ ] Build time-series forecasting models (ARIMA, Prophet)
- [ ] Train regression models for PM2.5 prediction
- [ ] Implement classification for AQI categories
- [ ] Perform cross-validation and model comparison

### Phase 4: Final Report & Presentation (Weeks 10-12)
- [ ] Write comprehensive technical report
- [ ] Create executive summary for stakeholders
- [ ] Design presentation slides with key visualizations
- [ ] Record demo video of dashboard
- [ ] Prepare for final evaluation

---

## 🛠️ Getting Started

### Prerequisites
- Python 3.9 or higher
- Jupyter Notebook or JupyterLab
- Git for version control

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/team/DataMinions.git
   cd DataMinions
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run preprocessing notebook**:
   ```bash
   jupyter notebook notebooks/data_preprocessing.ipynb
   ```

### Quick Start
```python
# Fetch sample data
from src.data_fetch import fetch_openaq

df = fetch_openaq(country="IN", pollutant="pm25", limit=1000)
print(df.head())
```

---

## 📚 References & Literature

1. **WHO Air Quality Guidelines (2021)**  
   https://www.who.int/publications/i/item/9789240034228

2. **Grossman, G. M., & Krueger, A. B. (1995)**  
   "Economic Growth and the Environment"  
   *Quarterly Journal of Economics*

3. **OpenAQ Platform Documentation**  
   https://docs.openaq.org

4. **World Bank Open Data**  
   https://data.worldbank.org

5. **US EPA Air Quality Index Guide**  
   https://www.airnow.gov/aqi/aqi-basics/

---

## 📧 Contact & Support

**Team**: DataMinions  
**Course**: Data Mining (Fall 2025)  
**Institution**: [University Name]

For questions or collaboration inquiries, please open an issue on GitHub or contact the current project lead.

---

## 📄 License

This project is for educational purposes as part of a university data mining course. Data sources (OpenAQ, World Bank) are publicly available and used in accordance with their respective licenses.

---

**Last Updated**: 2025-11-06  
**Current Phase**: Phase 1 - Data Collection & Preprocessing  
**Next Evaluation**: [Date TBD]

---

*Made with ❤️ by the DataMinions team*
