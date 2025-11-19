"""
Feature Engineering Module
===========================
Creates derived features and calculated columns for analysis.
"""

import pandas as pd
import numpy as np

from src.config import AQI_PM25_BINS, AQI_PM25_LABELS
from src.utils import Logger


# ============================================================================
# FEATURE ENGINEERING FUNCTIONS
# ============================================================================

def create_pollution_per_gdp(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create PM2.5 per GDP feature (normalized pollution by economic output).

    Args:
        df: DataFrame with pm25 and gdp_per_capita columns

    Returns:
        DataFrame with pm25_per_gdp column added
    """
    if 'mean_value_PM25' in df.columns and 'gdp_per_capita' in df.columns:
        df['pm25_per_gdp'] = df['mean_value_PM25'] / (df['gdp_per_capita'] / 1000)
    return df


def create_urban_pollution_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create urban pollution index (PM2.5 × urbanization percentage).

    Args:
        df: DataFrame with pm25 and urban_population_pct columns

    Returns:
        DataFrame with urban_pollution_index column added
    """
    if 'mean_value_PM25' in df.columns and 'urban_population_pct' in df.columns:
        df['urban_pollution_index'] = df['mean_value_PM25'] * (df['urban_population_pct'] / 100)
    return df


def create_aqi_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create AQI category for PM2.5 (US EPA standard).

    Args:
        df: DataFrame with mean_value_PM25 column

    Returns:
        DataFrame with aqi_category_pm25 column added
    """
    if 'mean_value_PM25' in df.columns:
        df['aqi_category_pm25'] = pd.cut(
            df['mean_value_PM25'],
            bins=AQI_PM25_BINS,
            labels=AQI_PM25_LABELS
        )
    return df


def create_data_completeness_score(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create data completeness score (0-100 based on non-null percentage).

    Args:
        df: DataFrame to calculate completeness for

    Returns:
        DataFrame with data_completeness_pct column added
    """
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    df['data_completeness_pct'] = (1 - df[numeric_cols].isna().mean(axis=1)) * 100
    return df


def create_composite_pollution_index(df: pd.DataFrame) -> pd.DataFrame:
    """
    Create composite pollution index (normalized average of all pollutants).

    Args:
        df: DataFrame with mean_value_* columns

    Returns:
        DataFrame with composite_pollution_index column added
    """
    pollutant_cols = [col for col in df.columns if col.startswith('mean_value_')]

    if pollutant_cols:
        # Normalize each pollutant to 0-100 scale
        normalized_pollutants = pd.DataFrame()
        for col in pollutant_cols:
            if df[col].notna().sum() > 0:
                max_val = df[col].max()
                if max_val > 0:
                    normalized_pollutants[col] = (df[col] / max_val) * 100

        if not normalized_pollutants.empty:
            df['composite_pollution_index'] = normalized_pollutants.mean(axis=1)

    return df


# ============================================================================
# MAIN FEATURE ENGINEERING FUNCTION
# ============================================================================

def create_all_features(df: pd.DataFrame, logger: Logger) -> pd.DataFrame:
    """
    Create all derived features for analysis.

    Args:
        df: Merged DataFrame
        logger: Logger instance

    Returns:
        DataFrame with all derived features added
    """
    logger.log("=" * 80)
    logger.log("CREATING DERIVED FEATURES")
    logger.log("=" * 80)

    initial_col_count = len(df.columns)

    # 1. Pollution per capita (normalized by GDP)
    df = create_pollution_per_gdp(df)
    if 'pm25_per_gdp' in df.columns:
        logger.log(" Created: pm25_per_gdp (PM2.5 normalized by GDP)")

    # 2. Urban pollution intensity
    df = create_urban_pollution_index(df)
    if 'urban_pollution_index' in df.columns:
        logger.log(" Created: urban_pollution_index (PM2.5 × urbanization %)")

    # 3. Air Quality Index category for PM2.5 (US EPA standard)
    df = create_aqi_category(df)
    if 'aqi_category_pm25' in df.columns:
        logger.log(" Created: aqi_category_pm25 (EPA AQI categories)")

    # 4. Data completeness score (0-100)
    df = create_data_completeness_score(df)
    if 'data_completeness_pct' in df.columns:
        logger.log(" Created: data_completeness_pct (% of non-null values)")

    # 5. Multi-pollutant index (average of available pollutants, normalized)
    df = create_composite_pollution_index(df)
    if 'composite_pollution_index' in df.columns:
        logger.log(" Created: composite_pollution_index (average of all pollutants, normalized)")

    new_features = len(df.columns) - initial_col_count
    logger.log(f"\n Added {new_features} new features")
    logger.log(f" Total features in dataset: {len(df.columns)}")
    logger.log("")

    return df


# ============================================================================
# FEATURE SELECTION & FILTERING
# ============================================================================

def filter_by_completeness(
    df: pd.DataFrame,
    threshold: float = 80.0,
    logger: Logger = None
) -> pd.DataFrame:
    """
    Filter dataset by data completeness threshold.

    Args:
        df: DataFrame with data_completeness_pct column
        threshold: Minimum completeness percentage (0-100)
        logger: Optional logger instance

    Returns:
        Filtered DataFrame
    """
    if 'data_completeness_pct' not in df.columns:
        return df

    before = len(df)
    df_filtered = df[df['data_completeness_pct'] >= threshold].copy()
    after = len(df_filtered)

    if logger:
        logger.log(f"Filtered by completeness >= {threshold}%:")
        logger.log(f"  Before: {before:,} records")
        logger.log(f"  After: {after:,} records")
        logger.log(f"  Removed: {before - after:,} records ({(before - after) / before * 100:.1f}%)")

    return df_filtered


def get_key_analysis_columns(df: pd.DataFrame) -> dict:
    """
    Get list of key columns for analysis, organized by category.

    Args:
        df: DataFrame to analyze

    Returns:
        Dictionary of column categories and their columns
    """
    key_columns = {
        'Identifiers': [],
        'Air Quality Metrics': [],
        'Economic Indicators': [],
        'Urbanization': [],
        'Derived Features': [],
        'Quality Flags': []
    }

    # Identifiers
    for col in ['country', 'country_code', 'year']:
        if col in df.columns:
            key_columns['Identifiers'].append(col)

    # Air Quality Metrics
    for col in df.columns:
        if col.startswith('mean_value_') or col.startswith('median_value_'):
            key_columns['Air Quality Metrics'].append(col)

    # Economic Indicators
    for col in ['gdp_per_capita', 'income_category']:
        if col in df.columns:
            key_columns['Economic Indicators'].append(col)

    # Urbanization
    for col in ['urban_population_pct', 'urbanization_level']:
        if col in df.columns:
            key_columns['Urbanization'].append(col)

    # Derived Features
    for col in ['pm25_per_gdp', 'urban_pollution_index', 'aqi_category_pm25', 'composite_pollution_index']:
        if col in df.columns:
            key_columns['Derived Features'].append(col)

    # Quality Flags
    for col in ['data_completeness_pct', 'has_coordinates', 'has_city']:
        if col in df.columns:
            key_columns['Quality Flags'].append(col)

    return key_columns


# ============================================================================
# STATISTICAL SUMMARY
# ============================================================================

def get_feature_summary(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get statistical summary of derived features.

    Args:
        df: DataFrame with derived features

    Returns:
        Summary DataFrame
    """
    derived_features = [
        'pm25_per_gdp',
        'urban_pollution_index',
        'data_completeness_pct',
        'composite_pollution_index'
    ]

    summary_data = []

    for feature in derived_features:
        if feature in df.columns and df[feature].notna().sum() > 0:
            summary_data.append({
                'Feature': feature,
                'Count': df[feature].notna().sum(),
                'Mean': df[feature].mean(),
                'Median': df[feature].median(),
                'Std': df[feature].std(),
                'Min': df[feature].min(),
                'Max': df[feature].max()
            })

    return pd.DataFrame(summary_data)
