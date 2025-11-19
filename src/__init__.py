"""
DataMinions - Air Quality Data Analysis Pipeline
=================================================
A modular system for fetching, cleaning, and analyzing air quality data
from OpenAQ and World Bank APIs.

Modules:
- config: Configuration constants
- utils: Common utilities and logging
- data_fetch: API data fetching functions
- data_cleaning: Data cleaning and validation
- features: Feature engineering and derived columns
"""

__version__ = "1.0.0"
__author__ = "Claude Code"

# Import key classes and functions for easier access
from src.utils import Logger
from src.data_fetch import fetch_or_load_data
from src.data_cleaning import clean_and_merge_data
from src.features import create_all_features

__all__ = [
    'Logger',
    'fetch_or_load_data',
    'clean_and_merge_data',
    'create_all_features',
]
