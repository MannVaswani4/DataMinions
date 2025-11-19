#!/usr/bin/env python3
"""
Fetch Data Script
=================
Main script to fetch air quality data from OpenAQ and World Bank APIs.

Usage:
    python fetch_data.py              # Use cached data if available
    python fetch_data.py --force      # Force fetch from APIs
"""

import argparse
from datetime import datetime

from src.utils import Logger
from src.data_fetch import fetch_or_load_data


def main():
    """Main execution function."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Fetch air quality data from APIs')
    parser.add_argument(
        '--force',
        action='store_true',
        help='Force fetch from APIs even if cached data exists'
    )
    args = parser.parse_args()

    # Initialize logger
    logger = Logger(print_to_console=True)
    start_time = datetime.now()

    # Header
    logger.log("=" * 80)
    logger.log("AIR QUALITY DATA FETCHER")
    logger.log("=" * 80)
    logger.log(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    logger.log(f"Force fetch: {args.force}")
    logger.log("")

    try:
        # Fetch or load data
        df_openaq, df_wb = fetch_or_load_data(logger, force_fetch=args.force)

        # Summary
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        logger.log("\n" + "=" * 80)
        logger.log("EXECUTION SUMMARY")
        logger.log("=" * 80)
        logger.log(f"Completed at: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.log(f"Total Duration: {duration:.2f} seconds")
        logger.log(f"OpenAQ Records: {len(df_openaq):,}")
        logger.log(f"World Bank Records: {len(df_wb):,}")
        logger.log("")
        logger.log("Next Steps:")
        logger.log("  1. Run: python clean_data.py")
        logger.log("  2. Check: data/ folder for raw data files")
        logger.log("=" * 80)

        # Save logs
        logger.save()

        logger.log("\n✓ DATA FETCHING COMPLETE")

    except Exception as e:
        logger.log(f"\n✗ ERROR: {e}")
        logger.save()
        raise


if __name__ == "__main__":
    main()
