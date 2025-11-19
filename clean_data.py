#!/usr/bin/env python3
"""
Clean Data Script
=================
Main script to clean, merge, and prepare air quality data for analysis.

Usage:
    python clean_data.py
"""

from datetime import datetime

from src.utils import Logger, save_dataframe_multiple_formats, save_data_dictionary
from src.data_cleaning import clean_and_merge_data
from src.features import create_all_features
from src.config import (
    DATA_DIR, CLEANED_DIR, DB_DIR,
    OPENAQ_RAW_CSV, WORLDBANK_RAW_CSV,
    OPENAQ_CLEANED_CSV, WORLDBANK_CLEANED_CSV,
    ANALYSIS_READY_CSV, MERGED_COMPLETE_CSV
)
import pandas as pd


def load_raw_data(logger: Logger):
    """Load raw data files."""
    logger.log("=" * 80)
    logger.log("LOADING RAW DATA")
    logger.log("=" * 80)

    df_openaq = pd.read_csv(DATA_DIR / OPENAQ_RAW_CSV)
    df_wb = pd.read_csv(DATA_DIR / WORLDBANK_RAW_CSV)

    logger.log(f"✓ Loaded OpenAQ: {len(df_openaq):,} records")
    logger.log(f"✓ Loaded World Bank: {len(df_wb):,} records")
    logger.log("")

    return df_openaq, df_wb


def save_cleaned_data(
    df_openaq_clean,
    df_wb_clean,
    df_analysis,
    df_merged_full,
    logger: Logger
):
    """Save all cleaned datasets."""
    logger.log("=" * 80)
    logger.log("SAVING CLEANED DATA")
    logger.log("=" * 80)

    # 1. Cleaned OpenAQ (detailed records)
    df_openaq_clean.to_csv(CLEANED_DIR / OPENAQ_CLEANED_CSV, index=False)
    logger.log(f"✓ Saved: {CLEANED_DIR / OPENAQ_CLEANED_CSV}")

    # 2. Cleaned World Bank
    df_wb_clean.to_csv(CLEANED_DIR / WORLDBANK_CLEANED_CSV, index=False)
    logger.log(f"✓ Saved: {CLEANED_DIR / WORLDBANK_CLEANED_CSV}")

    # 3. Analysis-ready dataset (merged, with derived features)
    df_analysis.to_csv(CLEANED_DIR / ANALYSIS_READY_CSV, index=False)
    logger.log(f"✓ Saved: {CLEANED_DIR / ANALYSIS_READY_CSV} (PRIMARY DATASET FOR ANALYSIS)")

    # 4. Full merged dataset (includes unmatched records)
    df_merged_full.to_csv(CLEANED_DIR / MERGED_COMPLETE_CSV, index=False)
    logger.log(f"✓ Saved: {CLEANED_DIR / MERGED_COMPLETE_CSV}")

    # 5. Save data dictionaries
    save_data_dictionary(df_openaq_clean, 'openaq', DB_DIR)
    logger.log(f"✓ Saved: {DB_DIR / 'openaq_data_dictionary.json'}")

    save_data_dictionary(df_wb_clean, 'worldbank', DB_DIR)
    logger.log(f"✓ Saved: {DB_DIR / 'worldbank_data_dictionary.json'}")

    save_data_dictionary(df_analysis, 'analysis_ready', CLEANED_DIR)
    logger.log(f"✓ Saved: {CLEANED_DIR / 'data_dictionary.json'}")

    logger.log("")


def print_summary(df_analysis, openaq_stats, wb_stats, logger: Logger):
    """Print summary statistics."""
    logger.log("=" * 80)
    logger.log("DATA CLEANING SUMMARY")
    logger.log("=" * 80)

    logger.log("\n### OpenAQ Cleaning")
    logger.log(f"  Initial records: {openaq_stats['initial']:,}")
    logger.log(f"  Final records: {openaq_stats['final']:,}")
    logger.log(f"  Retention rate: {openaq_stats['final']/openaq_stats['initial']*100:.1f}%")

    logger.log("\n### World Bank Cleaning")
    logger.log(f"  Initial records: {wb_stats['initial']:,}")
    logger.log(f"  Final records: {wb_stats['final']:,}")
    logger.log(f"  Retention rate: {wb_stats['final']/wb_stats['initial']*100:.1f}%")

    logger.log("\n### Final Analysis Dataset")
    logger.log(f"  Total records: {len(df_analysis):,}")
    logger.log(f"  Countries: {df_analysis['country'].nunique()}")
    if 'year' in df_analysis.columns:
        logger.log(f"  Years: {df_analysis['year'].min():.0f}-{df_analysis['year'].max():.0f}")
    logger.log(f"  Total columns: {len(df_analysis.columns)}")

    # Data completeness
    if 'data_completeness_pct' in df_analysis.columns:
        completeness = df_analysis['data_completeness_pct'].mean()
        logger.log(f"\n### Data Completeness")
        logger.log(f"  Average completeness: {completeness:.2f}%")

    logger.log("")


def main():
    """Main execution function."""
    # Initialize logger
    logger = Logger(print_to_console=True)
    start_time = datetime.now()

    # Header
    logger.log("=" * 80)
    logger.log("DATA CLEANING & PREPROCESSING PIPELINE")
    logger.log("=" * 80)
    logger.log(f"Started: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.log("")

    try:
        # Load raw data
        df_openaq_raw, df_wb_raw = load_raw_data(logger)

        # Clean and merge data
        (
            df_openaq_clean,
            df_wb_clean,
            df_analysis,
            df_merged_full,
            openaq_stats,
            wb_stats
        ) = clean_and_merge_data(df_openaq_raw, df_wb_raw, logger)

        # Create derived features
        df_analysis = create_all_features(df_analysis, logger)

        # Save cleaned data
        save_cleaned_data(
            df_openaq_clean,
            df_wb_clean,
            df_analysis,
            df_merged_full,
            logger
        )

        # Print summary
        print_summary(df_analysis, openaq_stats, wb_stats, logger)

        # Final summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.log("=" * 80)
        logger.log("EXECUTION SUMMARY")
        logger.log("=" * 80)
        logger.log(f"Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.log(f"Duration: {duration:.2f} seconds")
        logger.log("")
        logger.log("Next Steps:")
        logger.log(f"  1. Use: {CLEANED_DIR / ANALYSIS_READY_CSV} for analysis")
        logger.log(f"  2. Check: {CLEANED_DIR / 'data_dictionary.json'} for column details")
        logger.log("  3. Start visualization or statistical analysis")
        logger.log("=" * 80)

        # Save logs
        logger.save(prefix='preprocessing_log')

        logger.log("\n✓ DATA CLEANING COMPLETE")

    except Exception as e:
        logger.log(f"\n✗ ERROR: {e}")
        logger.save(prefix='preprocessing_log')
        raise


if __name__ == "__main__":
    main()
