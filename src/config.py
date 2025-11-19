"""
Configuration Constants
=======================
All configuration parameters for the DataMinions project.
Centralized configuration makes it easy to modify settings.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================================================
# PROJECT STRUCTURE
# ============================================================================

# Base directories
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / 'data'
CLEANED_DIR = PROJECT_ROOT / 'cleaned_data'
LOGS_DIR = PROJECT_ROOT / 'logs'
REPORTS_DIR = PROJECT_ROOT / 'reports'
DB_DIR = PROJECT_ROOT / 'database_ready'
VISUALIZATIONS_DIR = PROJECT_ROOT / 'visualizations'

# Ensure all directories exist
for directory in [DATA_DIR, CLEANED_DIR, LOGS_DIR, REPORTS_DIR, DB_DIR, VISUALIZATIONS_DIR]:
    directory.mkdir(exist_ok=True, parents=True)

# ============================================================================
# API CONFIGURATION
# ============================================================================

# OpenAQ API Configuration (v3)
OPENAQ_API_KEY = os.getenv('OPENAQ_API_KEY')
OPENAQ_BASE_URL = "https://api.openaq.org/v3"

# OpenAQ Parameter IDs (v3 API)
OPENAQ_PARAMETERS = {
    'pm10': 1,
    'pm25': 2,
    'no2': 7,
    'co': 8,
    'o3': 10
}

# World Bank Indicators
WORLD_BANK_INDICATORS = {
    'pm25_exposure': 'EN.ATM.PM25.MC.M3',
    'gdp_per_capita': 'NY.GDP.PCAP.CD',
    'urban_population_pct': 'SP.URB.TOTL.IN.ZS'
}

# World Bank time range
WB_START_YEAR = 2010
WB_END_YEAR = 2023

# ============================================================================
# DATA QUALITY THRESHOLDS
# ============================================================================

# Valid ranges for air quality parameters (based on scientific standards)
PARAMETER_THRESHOLDS = {
    'PM10': {'min': 0, 'max': 1000, 'unit': 'µg/m³'},
    'PM25': {'min': 0, 'max': 500, 'unit': 'µg/m³'},
    'NO2': {'min': 0, 'max': 1000, 'unit': 'ppb'},
    'CO': {'min': 0, 'max': 50, 'unit': 'ppm'},
    'O3': {'min': 0, 'max': 0.5, 'unit': 'ppm'}
}

# Geographic coordinate bounds
LAT_MIN, LAT_MAX = -90, 90
LON_MIN, LON_MAX = -180, 180

# World Bank regional/aggregate codes to exclude (not actual countries)
EXCLUDED_WB_CODES = [
    'ARB', 'CSS', 'CEB', 'EAR', 'EAS', 'EAP', 'TEA', 'EMU', 'ECS', 'ECA',
    'TEC', 'EUU', 'FCS', 'HPC', 'HIC', 'IBD', 'IBT', 'IDB', 'IDX', 'IDA',
    'LTE', 'LCN', 'LAC', 'TLA', 'LDC', 'LMY', 'LIC', 'LMC', 'MEA', 'MNA',
    'TMN', 'MIC', 'NAC', 'OED', 'OSS', 'PSS', 'PST', 'PRE', 'SST', 'SAS',
    'TSA', 'SSF', 'SSA', 'TSS', 'UMC', 'WLD'
]

# ============================================================================
# API REQUEST SETTINGS
# ============================================================================

# Pagination settings
MAX_PAGES_LOCATIONS = 5
MAX_PAGES_MEASUREMENTS = 10
ITEMS_PER_PAGE = 1000
REQUEST_TIMEOUT = 30  # seconds
REQUEST_DELAY = 0.5  # seconds between requests

# ============================================================================
# DATA CATEGORIZATION THRESHOLDS
# ============================================================================

# Income categories (World Bank classification, in USD)
INCOME_BINS = [0, 1085, 4255, 13205, float('inf')]
INCOME_LABELS = ['Low Income', 'Lower Middle Income', 'Upper Middle Income', 'High Income']

# Urbanization levels (percentage)
URBANIZATION_BINS = [0, 40, 60, 80, 100]
URBANIZATION_LABELS = ['Rural', 'Moderately Urbanized', 'Highly Urbanized', 'Extremely Urbanized']

# EPA AQI Categories for PM2.5 (µg/m³)
AQI_PM25_BINS = [0, 12, 35.4, 55.4, 150.4, 250.4, float('inf')]
AQI_PM25_LABELS = ['Good', 'Moderate', 'Unhealthy for Sensitive', 'Unhealthy', 'Very Unhealthy', 'Hazardous']

# ============================================================================
# FILE NAMES
# ============================================================================

# Raw data files
OPENAQ_RAW_CSV = 'openaq_raw.csv'
OPENAQ_RAW_JSON = 'openaq_raw.json'
WORLDBANK_RAW_CSV = 'worldbank_raw.csv'
WORLDBANK_RAW_JSON = 'worldbank_raw.json'

# Cleaned data files
OPENAQ_CLEANED_CSV = 'openaq_cleaned.csv'
WORLDBANK_CLEANED_CSV = 'worldbank_cleaned.csv'
ANALYSIS_READY_CSV = 'analysis_ready.csv'
MERGED_COMPLETE_CSV = 'merged_complete.csv'

# Database-ready files
OPENAQ_DB_CSV = 'openaq_db_ready.csv'
OPENAQ_DB_PARQUET = 'openaq_db_ready.parquet'
WORLDBANK_DB_CSV = 'worldbank_db_ready.csv'
WORLDBANK_DB_PARQUET = 'worldbank_db_ready.parquet'

# Metadata files
OPENAQ_DATA_DICT = 'openaq_data_dictionary.json'
WORLDBANK_DATA_DICT = 'worldbank_data_dictionary.json'
ANALYSIS_DATA_DICT = 'data_dictionary.json'

# Report files
PREPROCESSING_REPORT = 'preprocessing_report.md'

# ============================================================================
# LOGGING SETTINGS
# ============================================================================

LOG_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
LOG_FILE_PREFIX = 'data_fetch_analysis'
PREPROCESSING_LOG_PREFIX = 'preprocessing_log'
