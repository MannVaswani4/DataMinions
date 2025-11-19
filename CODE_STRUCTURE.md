# DataMinions - Code Structure Documentation

## Overview

DataMinions is a modular air quality data analysis pipeline that fetches, cleans, and analyzes data from OpenAQ and World Bank APIs. The codebase has been refactored into a clean, modular structure for easy maintenance and understanding.

## Project Structure

```
DataMinions/
├── src/                        # Core modules (modular, reusable code)
│   ├── __init__.py            # Package initialization
│   ├── config.py              # All configuration constants
│   ├── utils.py               # Common utilities (logging, file ops)
│   ├── data_fetch.py          # API data fetching functions
│   ├── data_cleaning.py       # Data cleaning and validation
│   ├── features.py            # Feature engineering
│   ├── models.py              # ML models (placeholder for future)
│   └── viz_streamlit.py       # Streamlit visualizations (placeholder)
│
├── fetch_data.py              # Main script: Fetch data from APIs
├── clean_data.py              # Main script: Clean and prepare data
│
├── data/                      # Raw data from APIs
├── cleaned_data/              # Cleaned, analysis-ready data
├── database_ready/            # Database-ready formats (CSV, Parquet)
├── logs/                      # Execution logs
├── reports/                   # Analysis reports
├── visualizations/            # Generated charts and graphs
├── archive/                   # Old script files (backup)
│
├── .gitignore                 # Git ignore file
├── CODE_STRUCTURE.md          # This file
└── README.md                  # Project documentation

```

## Module Descriptions

### Core Modules (`src/`)

#### 1. `config.py`
**Purpose:** Centralized configuration management

**Contains:**
- API credentials and endpoints (OpenAQ, World Bank)
- Directory paths
- Data quality thresholds
- Parameter definitions
- File naming constants

**Example:**
```python
from src.config import OPENAQ_API_KEY, DATA_DIR, PARAMETER_THRESHOLDS
```

#### 2. `utils.py`
**Purpose:** Common utilities used across modules

**Key Components:**
- `Logger`: Logging class with console and file output
- `create_data_dictionary()`: Generate schema documentation
- `save_data_dictionary()`: Save metadata to JSON
- `get_iso_country_code_mapping()`: ISO code conversions
- File operation helpers

**Example:**
```python
from src.utils import Logger

logger = Logger(print_to_console=True)
logger.log("Processing data...")
logger.save()
```

#### 3. `data_fetch.py`
**Purpose:** Fetch data from external APIs

**Key Functions:**
- `fetch_openaq_locations()`: Get location metadata
- `fetch_openaq_latest_measurements()`: Get air quality measurements
- `fetch_world_bank_indicator()`: Get economic/social indicators
- `fetch_or_load_data()`: High-level function with caching

**Features:**
- Automatic caching (checks for existing data)
- Pagination handling
- Error handling and retries
- Rate limiting

**Example:**
```python
from src.data_fetch import fetch_or_load_data
from src.utils import Logger

logger = Logger()
df_openaq, df_wb = fetch_or_load_data(logger, force_fetch=False)
```

#### 4. `data_cleaning.py`
**Purpose:** Clean, validate, and merge datasets

**Key Functions:**
- `clean_openaq_data()`: Remove invalid/unknown records
- `clean_world_bank_data()`: Filter regional aggregates
- `aggregate_openaq_by_country()`: Aggregate for analysis
- `merge_datasets()`: Merge OpenAQ + World Bank data
- `clean_and_merge_data()`: Complete pipeline

**Cleaning Steps:**
1. Remove unknown countries (46.91% of raw data)
2. Validate coordinates (lat/lon ranges)
3. Remove invalid measurement values
4. Remove duplicates
5. Add datetime components
6. Create quality flags

**Example:**
```python
from src.data_cleaning import clean_and_merge_data
from src.utils import Logger

logger = Logger()
(df_openaq_clean, df_wb_clean, df_analysis,
 df_merged_full, openaq_stats, wb_stats) = clean_and_merge_data(
    df_openaq_raw, df_wb_raw, logger
)
```

#### 5. `features.py`
**Purpose:** Create derived features for analysis

**Key Functions:**
- `create_pollution_per_gdp()`: PM2.5 normalized by GDP
- `create_urban_pollution_index()`: PM2.5 × urbanization
- `create_aqi_category()`: EPA AQI categories
- `create_data_completeness_score()`: Data quality metric
- `create_composite_pollution_index()`: Multi-pollutant index
- `create_all_features()`: Apply all transformations

**Example:**
```python
from src.features import create_all_features
from src.utils import Logger

logger = Logger()
df_with_features = create_all_features(df_merged, logger)
```

#### 6. `models.py` (Placeholder)
**Purpose:** Machine learning models

**Future Use:**
- Regression models for PM2.5 prediction
- Classification for AQI categories
- Time series forecasting
- Clustering for country grouping

#### 7. `viz_streamlit.py` (Placeholder)
**Purpose:** Interactive Streamlit dashboard

**Future Use:**
- Interactive maps
- Time series visualizations
- Country comparisons
- Filtering and drill-down

---

## Main Scripts

### 1. `fetch_data.py`
**Purpose:** Fetch data from APIs

**Usage:**
```bash
# Use cached data if available
python fetch_data.py

# Force fresh fetch from APIs
python fetch_data.py --force
```

**What it does:**
1. Checks for cached data
2. Fetches from OpenAQ and World Bank APIs (if needed)
3. Saves raw data to `data/` folder
4. Generates log file

**Output Files:**
- `data/openaq_raw.csv`
- `data/openaq_raw.json`
- `data/worldbank_raw.csv`
- `data/worldbank_raw.json`

### 2. `clean_data.py`
**Purpose:** Clean and prepare data for analysis

**Usage:**
```bash
python clean_data.py
```

**What it does:**
1. Loads raw data from `data/`
2. Cleans and validates data
3. Merges OpenAQ + World Bank datasets
4. Creates derived features
5. Saves cleaned data to `cleaned_data/`
6. Generates data dictionaries

**Output Files:**
- `cleaned_data/openaq_cleaned.csv`
- `cleaned_data/worldbank_cleaned.csv`
- `cleaned_data/analysis_ready.csv` ← **PRIMARY DATASET**
- `cleaned_data/merged_complete.csv`
- `cleaned_data/data_dictionary.json`

---

## Workflow

### Standard Pipeline

```
1. Fetch Data
   python fetch_data.py
   ↓
2. Clean Data
   python clean_data.py
   ↓
3. Analyze Data
   Use: cleaned_data/analysis_ready.csv
```

### Programmatic Usage

```python
# Complete pipeline in Python
from src.utils import Logger
from src.data_fetch import fetch_or_load_data
from src.data_cleaning import clean_and_merge_data
from src.features import create_all_features

# Initialize logger
logger = Logger(print_to_console=True)

# Step 1: Fetch data
df_openaq_raw, df_wb_raw = fetch_or_load_data(logger)

# Step 2: Clean and merge
(df_openaq_clean, df_wb_clean, df_analysis,
 df_merged_full, openaq_stats, wb_stats) = clean_and_merge_data(
    df_openaq_raw, df_wb_raw, logger
)

# Step 3: Create features
df_analysis = create_all_features(df_analysis, logger)

# Step 4: Analyze
print(f"Analysis-ready dataset: {len(df_analysis)} records")
print(f"Countries: {df_analysis['country'].nunique()}")
```

---

## Key Features

### 1. **Modular Design**
- Each module has a single responsibility
- Easy to understand and maintain
- Reusable functions

### 2. **Configuration Management**
- All settings in one place (`config.py`)
- Easy to modify API keys, thresholds, etc.
- No hard-coded values in logic

### 3. **Comprehensive Logging**
- All operations are logged
- Logs saved to files with timestamps
- Console output for real-time monitoring

### 4. **Data Caching**
- Automatic detection of existing data
- Avoids unnecessary API calls
- Force fetch option when needed

### 5. **Data Quality**
- Validation of all input data
- Removal of invalid/suspicious records
- Quality flags and completeness scores

### 6. **Documentation**
- Every module has docstrings
- Clear function signatures with type hints
- Data dictionaries for all datasets

---

## Data Dictionary

The primary analysis dataset (`analysis_ready.csv`) contains:

### Identifiers
- `country`: Country name
- `country_code`: ISO 3166-1 alpha-3 code
- `year`: Year of World Bank data

### Air Quality Metrics (from OpenAQ)
- `mean_value_PM25`: Average PM2.5 concentration (µg/m³)
- `mean_value_PM10`: Average PM10 concentration (µg/m³)
- `mean_value_NO2`: Average NO2 concentration (ppb)
- `mean_value_CO`: Average CO concentration (ppm)
- `mean_value_O3`: Average O3 concentration (ppm)
- `median_value_*`: Median values for each pollutant
- `measurement_count_*`: Number of measurements per pollutant

### Economic Indicators (from World Bank)
- `gdp_per_capita`: GDP per capita (current USD)
- `income_category`: Low/Lower Middle/Upper Middle/High Income

### Urbanization
- `urban_population_pct`: Urban population percentage
- `urbanization_level`: Rural/Moderately/Highly/Extremely Urbanized

### Derived Features
- `pm25_per_gdp`: PM2.5 per $1000 GDP (pollution intensity)
- `urban_pollution_index`: PM2.5 × urbanization %
- `aqi_category_pm25`: EPA AQI category (Good to Hazardous)
- `data_completeness_pct`: Data quality score (0-100)
- `composite_pollution_index`: Normalized multi-pollutant index

---

## Dependencies

```bash
# Core dependencies
pip install pandas numpy requests wbgapi

# Optional (for Parquet support)
pip install pyarrow

# Optional (for future visualizations)
pip install streamlit plotly matplotlib seaborn
```

---

## Maintenance & Extensibility

### Adding New Data Sources
1. Add configuration to `config.py`
2. Create fetch function in `data_fetch.py`
3. Create cleaning function in `data_cleaning.py`
4. Update merge logic if needed

### Adding New Features
1. Add feature function to `features.py`
2. Call from `create_all_features()`
3. Document in data dictionary

### Modifying Thresholds
1. Edit values in `config.py`
2. No code changes needed
3. Re-run `clean_data.py`

---

## Troubleshooting

### Issue: "Module not found"
**Solution:** Ensure you're running from project root and src/ is a package
```bash
cd /path/to/DataMinions
python fetch_data.py
```

### Issue: "API key invalid"
**Solution:** Update API key in `src/config.py`

### Issue: "No data files found"
**Solution:** Run `fetch_data.py` first to fetch data

---

## Archive Folder

The `archive/` folder contains old monolithic script files:
- `fetch_and_analyze_data.py` (old)
- `preprocess_data.py` (old)

These are kept for reference but should not be used. Use the new modular scripts instead.

---

## Next Steps

1. **Run the pipeline:**
   ```bash
   python fetch_data.py
   python clean_data.py
   ```

2. **Start analysis:**
   - Load `cleaned_data/analysis_ready.csv`
   - Refer to `cleaned_data/data_dictionary.json` for column details

3. **Extend functionality:**
   - Add ML models in `src/models.py`
   - Create Streamlit dashboard in `src/viz_streamlit.py`
   - Add new data sources as needed

---

## Contact & Support

For questions or issues, refer to:
- This documentation
- Module docstrings
- Data dictionary JSON files
- Log files in `logs/` folder
