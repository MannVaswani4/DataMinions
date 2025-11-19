"""
Data Cleaning Module
====================
Cleans, validates, and merges OpenAQ and World Bank datasets.
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple

from src.config import (
    PARAMETER_THRESHOLDS, LAT_MIN, LAT_MAX, LON_MIN, LON_MAX,
    EXCLUDED_WB_CODES, INCOME_BINS, INCOME_LABELS,
    URBANIZATION_BINS, URBANIZATION_LABELS
)
from src.utils import Logger, get_iso_country_code_mapping


# ============================================================================
# OPENAQ DATA CLEANING
# ============================================================================

def clean_openaq_data(df: pd.DataFrame, logger: Logger) -> Tuple[pd.DataFrame, Dict]:
    """
    Comprehensive cleaning of OpenAQ data.

    Args:
        df: Raw OpenAQ DataFrame
        logger: Logger instance

    Returns:
        Tuple of (cleaned_df, cleaning_stats)
    """
    logger.log("=" * 80)
    logger.log("CLEANING OPENAQ DATA")
    logger.log("=" * 80)

    initial_count = len(df)
    logger.log(f"Initial records: {initial_count:,}")
    logger.log("")

    # Track cleaning steps
    cleaning_stats = {
        'initial': initial_count,
        'removed_unknown_countries': 0,
        'removed_invalid_coordinates': 0,
        'removed_invalid_values': 0,
        'removed_duplicates': 0,
        'final': 0
    }

    # 1. Remove records with Unknown country (46.91% of data - critical issue)
    logger.log("STEP 1: Removing Unknown countries...")
    unknown_mask = df['country'] == 'Unknown'
    unknown_count = unknown_mask.sum()
    df = df[~unknown_mask].copy()
    cleaning_stats['removed_unknown_countries'] = unknown_count
    logger.log(f"   Removed {unknown_count:,} records with Unknown country ({unknown_count/initial_count*100:.2f}%)")
    logger.log(f"   Remaining: {len(df):,} records")
    logger.log("")

    # 2. Remove invalid coordinates
    logger.log("STEP 2: Removing invalid coordinates...")
    before = len(df)
    df = df[
        ((df['latitude'].isna()) | ((df['latitude'] >= LAT_MIN) & (df['latitude'] <= LAT_MAX))) &
        ((df['longitude'].isna()) | ((df['longitude'] >= LON_MIN) & (df['longitude'] <= LON_MAX)))
    ].copy()
    invalid_coords = before - len(df)
    cleaning_stats['removed_invalid_coordinates'] = invalid_coords
    logger.log(f"   Removed {invalid_coords:,} records with invalid coordinates")
    logger.log(f"   Remaining: {len(df):,} records")
    logger.log("")

    # 3. Remove invalid measurement values (parameter-specific)
    logger.log("STEP 3: Removing invalid measurement values...")
    before = len(df)

    for param, thresholds in PARAMETER_THRESHOLDS.items():
        param_mask = df['parameter'] == param
        invalid_mask = param_mask & (
            (df['value'] < thresholds['min']) |
            (df['value'] > thresholds['max'])
        )
        invalid_count = invalid_mask.sum()

        if invalid_count > 0:
            logger.log(f"   Removing {invalid_count:,} invalid {param} values (outside {thresholds['min']}-{thresholds['max']} {thresholds['unit']})")
            df = df[~invalid_mask].copy()

    total_invalid = before - len(df)
    cleaning_stats['removed_invalid_values'] = total_invalid
    logger.log(f"  Total invalid values removed: {total_invalid:,}")
    logger.log(f"   Remaining: {len(df):,} records")
    logger.log("")

    # 4. Remove duplicates
    logger.log("STEP 4: Removing duplicates...")
    before = len(df)
    df = df.drop_duplicates(subset=['parameter', 'location_id', 'datetime', 'value']).copy()
    duplicates = before - len(df)
    cleaning_stats['removed_duplicates'] = duplicates
    logger.log(f"   Removed {duplicates:,} duplicate records")
    logger.log(f"   Remaining: {len(df):,} records")
    logger.log("")

    # 5. Add datetime components
    logger.log("STEP 5: Extracting datetime components...")
    df['datetime'] = pd.to_datetime(df['datetime'], errors='coerce')
    df['measurement_year'] = df['datetime'].dt.year
    df['measurement_month'] = df['datetime'].dt.month
    df['measurement_hour'] = df['datetime'].dt.hour
    logger.log(f"   Added year, month, hour columns")
    logger.log("")

    # 6. Create data quality flags
    logger.log("STEP 6: Creating data quality flags...")
    df['has_coordinates'] = df['latitude'].notna() & df['longitude'].notna()
    df['has_city'] = (df['city'] != 'Unknown') & df['city'].notna()
    logger.log(f"   Added quality flag columns")
    logger.log("")

    cleaning_stats['final'] = len(df)

    # Summary
    logger.log("CLEANING SUMMARY:")
    logger.log(f"  Initial records: {cleaning_stats['initial']:,}")
    logger.log(f"  - Unknown countries: -{cleaning_stats['removed_unknown_countries']:,}")
    logger.log(f"  - Invalid coordinates: -{cleaning_stats['removed_invalid_coordinates']:,}")
    logger.log(f"  - Invalid values: -{cleaning_stats['removed_invalid_values']:,}")
    logger.log(f"  - Duplicates: -{cleaning_stats['removed_duplicates']:,}")
    logger.log(f"  = Final records: {cleaning_stats['final']:,}")
    logger.log(f"  Data retention: {cleaning_stats['final']/cleaning_stats['initial']*100:.2f}%")
    logger.log("")

    return df, cleaning_stats


# ============================================================================
# WORLD BANK DATA CLEANING
# ============================================================================

def clean_world_bank_data(df: pd.DataFrame, logger: Logger) -> Tuple[pd.DataFrame, Dict]:
    """
    Clean World Bank data.

    Args:
        df: Raw World Bank DataFrame
        logger: Logger instance

    Returns:
        Tuple of (cleaned_df, cleaning_stats)
    """
    logger.log("=" * 80)
    logger.log("CLEANING WORLD BANK DATA")
    logger.log("=" * 80)

    initial_count = len(df)
    logger.log(f"Initial records: {initial_count:,}")
    logger.log("")

    cleaning_stats = {
        'initial': initial_count,
        'removed_regional_aggregates': 0,
        'removed_all_null': 0,
        'final': 0
    }

    # 1. Remove regional/aggregate codes (not actual countries)
    logger.log("STEP 1: Removing regional aggregates...")
    before = len(df)
    df = df[~df['country_code'].isin(EXCLUDED_WB_CODES)].copy()
    removed = before - len(df)
    cleaning_stats['removed_regional_aggregates'] = removed
    logger.log(f"   Removed {removed:,} regional aggregate records")
    logger.log(f"   Remaining: {len(df):,} records")
    logger.log("")

    # 2. Remove records where ALL indicators are null
    logger.log("STEP 2: Removing records with all null indicators...")
    before = len(df)
    indicator_cols = ['pm25_exposure', 'gdp_per_capita', 'urban_population_pct']
    df = df[df[indicator_cols].notna().any(axis=1)].copy()
    removed = before - len(df)
    cleaning_stats['removed_all_null'] = removed
    logger.log(f"   Removed {removed:,} records with all null indicators")
    logger.log(f"   Remaining: {len(df):,} records")
    logger.log("")

    # 3. Create derived columns
    logger.log("STEP 3: Creating derived columns...")

    # Income category based on GDP per capita (World Bank classification)
    df['income_category'] = pd.cut(
        df['gdp_per_capita'],
        bins=INCOME_BINS,
        labels=INCOME_LABELS
    )

    # Urbanization category
    df['urbanization_level'] = pd.cut(
        df['urban_population_pct'],
        bins=URBANIZATION_BINS,
        labels=URBANIZATION_LABELS
    )

    logger.log(f"   Added income_category column")
    logger.log(f"   Added urbanization_level column")
    logger.log("")

    cleaning_stats['final'] = len(df)

    # Summary
    logger.log("CLEANING SUMMARY:")
    logger.log(f"  Initial records: {cleaning_stats['initial']:,}")
    logger.log(f"  - Regional aggregates: -{cleaning_stats['removed_regional_aggregates']:,}")
    logger.log(f"  - All null indicators: -{cleaning_stats['removed_all_null']:,}")
    logger.log(f"  = Final records: {cleaning_stats['final']:,}")
    logger.log(f"  Data retention: {cleaning_stats['final']/cleaning_stats['initial']*100:.2f}%")
    logger.log("")

    return df, cleaning_stats


# ============================================================================
# OPENAQ AGGREGATION BY COUNTRY
# ============================================================================

def aggregate_openaq_by_country(df: pd.DataFrame, logger: Logger) -> pd.DataFrame:
    """
    Aggregate OpenAQ data by country for merging with World Bank data.

    Args:
        df: Cleaned OpenAQ DataFrame
        logger: Logger instance

    Returns:
        Aggregated DataFrame (one row per country)
    """
    logger.log("=" * 80)
    logger.log("AGGREGATING OPENAQ DATA BY COUNTRY")
    logger.log("=" * 80)

    # Create aggregation for each parameter
    agg_dict = {
        'value': ['mean', 'median', 'std', 'min', 'max', 'count'],
        'has_coordinates': 'mean',
        'location_id': 'nunique'
    }

    # Aggregate by country and parameter
    df_agg = df.groupby(['country', 'country_code', 'parameter']).agg(agg_dict).reset_index()

    # Flatten column names
    df_agg.columns = ['_'.join(col).strip('_') if col[1] else col[0]
                      for col in df_agg.columns.values]

    # Rename for clarity
    df_agg.rename(columns={
        'value_mean': 'mean_value',
        'value_median': 'median_value',
        'value_std': 'std_value',
        'value_min': 'min_value',
        'value_max': 'max_value',
        'value_count': 'measurement_count',
        'has_coordinates_mean': 'coordinate_completeness',
        'location_id_nunique': 'num_locations'
    }, inplace=True)

    # Pivot to get one row per country with columns for each parameter
    df_pivot = df_agg.pivot_table(
        index=['country', 'country_code'],
        columns='parameter',
        values=['mean_value', 'median_value', 'measurement_count', 'num_locations']
    ).reset_index()

    # Flatten column names
    df_pivot.columns = ['_'.join([str(c) for c in col]).strip('_') if col[1] else col[0]
                        for col in df_pivot.columns.values]

    logger.log(f" Aggregated to {len(df_pivot):,} countries")
    logger.log(f"  Columns created: {len(df_pivot.columns)}")
    logger.log("")

    return df_pivot


# ============================================================================
# DATASET MERGING
# ============================================================================

def merge_datasets(
    df_openaq_agg: pd.DataFrame,
    df_wb: pd.DataFrame,
    logger: Logger
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Merge OpenAQ and World Bank datasets.

    Args:
        df_openaq_agg: Aggregated OpenAQ DataFrame
        df_wb: Cleaned World Bank DataFrame
        logger: Logger instance

    Returns:
        Tuple of (analysis_df, merged_complete_df)
    """
    logger.log("=" * 80)
    logger.log("MERGING DATASETS")
    logger.log("=" * 80)

    # Get country code mapping (2-letter to 3-letter)
    iso_mapping = get_iso_country_code_mapping()

    # Convert OpenAQ 2-letter codes to 3-letter codes
    logger.log("Converting OpenAQ country codes (2-letter ’ 3-letter)...")
    df_openaq_agg['country_code_3'] = df_openaq_agg['country_code'].map(iso_mapping)

    # Count how many codes were successfully converted
    converted = df_openaq_agg['country_code_3'].notna().sum()
    total = len(df_openaq_agg)
    logger.log(f"  Converted {converted}/{total} country codes")

    # Show unmapped codes
    unmapped = df_openaq_agg[df_openaq_agg['country_code_3'].isna()]
    if len(unmapped) > 0:
        logger.log(f"    Unmapped codes: {unmapped['country_code'].unique().tolist()}")

    # Use 3-letter code for merging, and keep original 2-letter code
    df_openaq_agg['country_code_2'] = df_openaq_agg['country_code']  # Keep original 2-letter
    df_openaq_agg['country_code'] = df_openaq_agg['country_code_3'].fillna(df_openaq_agg['country_code_2'])  # Use 3-letter for merging

    # Drop temporary columns
    df_openaq_agg.drop(columns=['country_code_3'], inplace=True)

    logger.log("")

    # Try merging on converted country_code
    logger.log("Merging datasets on country_code...")
    df_merged = pd.merge(
        df_openaq_agg,
        df_wb,
        on='country_code',
        how='outer',
        suffixes=('_openaq', '_wb'),
        indicator=True
    )

    # Consolidate country names (keep the non-null one)
    df_merged['country'] = df_merged['country_openaq'].fillna(df_merged['country_wb'])

    # Analyze merge results
    merge_stats = df_merged['_merge'].value_counts()
    logger.log(f"\nMerge statistics:")
    logger.log(f"  Both datasets: {merge_stats.get('both', 0):,}")
    logger.log(f"  Only OpenAQ: {merge_stats.get('left_only', 0):,}")
    logger.log(f"  Only World Bank: {merge_stats.get('right_only', 0):,}")
    logger.log("")

    # Keep only records that exist in both datasets for primary analysis
    df_analysis = df_merged[df_merged['_merge'] == 'both'].copy()

    # Drop merge indicator and redundant columns
    cols_to_drop = ['_merge', 'country_code_2', 'country_openaq', 'country_wb']
    cols_to_drop = [c for c in cols_to_drop if c in df_analysis.columns]
    df_analysis.drop(columns=cols_to_drop, inplace=True)

    logger.log(f" Analysis dataset: {len(df_analysis):,} records")
    logger.log(f"  Countries: {df_analysis['country'].nunique()}")
    if 'year' in df_analysis.columns:
        logger.log(f"  Years: {df_analysis['year'].min():.0f}-{df_analysis['year'].max():.0f}")
    logger.log("")

    # Keep full merged dataset for reference
    cols_to_drop_full = ['country_code_2']
    cols_to_drop_full = [c for c in cols_to_drop_full if c in df_merged.columns]
    df_merged.drop(columns=cols_to_drop_full, inplace=True)

    return df_analysis, df_merged


# ============================================================================
# COMPLETE CLEANING PIPELINE
# ============================================================================

def clean_and_merge_data(
    df_openaq_raw: pd.DataFrame,
    df_wb_raw: pd.DataFrame,
    logger: Logger
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame, Dict, Dict]:
    """
    Complete data cleaning and merging pipeline.

    Args:
        df_openaq_raw: Raw OpenAQ DataFrame
        df_wb_raw: Raw World Bank DataFrame
        logger: Logger instance

    Returns:
        Tuple of (
            df_openaq_clean,
            df_wb_clean,
            df_analysis,
            df_merged_full,
            openaq_stats,
            wb_stats
        )
    """
    # Clean OpenAQ data
    df_openaq_clean, openaq_stats = clean_openaq_data(df_openaq_raw, logger)

    # Clean World Bank data
    df_wb_clean, wb_stats = clean_world_bank_data(df_wb_raw, logger)

    # Aggregate OpenAQ by country
    df_openaq_agg = aggregate_openaq_by_country(df_openaq_clean, logger)

    # Merge datasets
    df_analysis, df_merged_full = merge_datasets(df_openaq_agg, df_wb_clean, logger)

    return (
        df_openaq_clean,
        df_wb_clean,
        df_analysis,
        df_merged_full,
        openaq_stats,
        wb_stats
    )
