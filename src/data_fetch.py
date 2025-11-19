"""
Data Fetching Module
====================
Fetches data from OpenAQ v3 and World Bank APIs with caching support.
"""

import pandas as pd
import requests
import time
import wbgapi as wb
from typing import Dict, List, Tuple, Optional

from src.config import (
    OPENAQ_API_KEY, OPENAQ_BASE_URL, OPENAQ_PARAMETERS,
    WORLD_BANK_INDICATORS, WB_START_YEAR, WB_END_YEAR,
    MAX_PAGES_LOCATIONS, MAX_PAGES_MEASUREMENTS,
    ITEMS_PER_PAGE, REQUEST_TIMEOUT, REQUEST_DELAY,
    DATA_DIR, OPENAQ_RAW_CSV, WORLDBANK_RAW_CSV
)
from src.utils import Logger, load_csv_if_exists


# ============================================================================
# OPENAQ API FUNCTIONS
# ============================================================================

def fetch_openaq_locations(
    parameter_id: int,
    parameter_name: str,
    logger: Logger,
    limit: int = ITEMS_PER_PAGE
) -> Dict[int, Dict[str, str]]:
    """
    Fetch locations with country metadata for a specific parameter from OpenAQ v3.

    Args:
        parameter_id: OpenAQ parameter ID
        parameter_name: Human-readable parameter name
        logger: Logger instance
        limit: Max items per page

    Returns:
        Dictionary mapping location_id to location metadata
    """
    logger.log(f"Fetching {parameter_name} locations from OpenAQ v3...")

    url = f"{OPENAQ_BASE_URL}/locations"
    headers = {
        'X-API-Key': OPENAQ_API_KEY,
        'Accept': 'application/json'
    }

    location_lookup = {}
    page = 1

    while page <= MAX_PAGES_LOCATIONS:
        params = {
            'limit': min(limit, ITEMS_PER_PAGE),
            'page': page,
            'parameters_id': parameter_id
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            data = response.json()
            results = data.get('results', [])

            if not results:
                break

            logger.log(f"  Page {page}: {len(results)} locations", print_override=False)

            # Build location lookup
            for loc in results:
                loc_id = loc.get('id')
                if loc_id:
                    country = loc.get('country', {})
                    location_lookup[loc_id] = {
                        'location_name': loc.get('name', 'Unknown'),
                        'country_code': country.get('code', 'Unknown'),
                        'country': country.get('name', 'Unknown'),
                        'city': loc.get('locality', 'Unknown'),
                    }

            # Check if we've retrieved all results
            meta = data.get('meta', {})
            found = meta.get('found', 0)
            if isinstance(found, int) and found <= len(location_lookup):
                break

            page += 1
            time.sleep(REQUEST_DELAY)

        except requests.exceptions.RequestException as e:
            logger.log(f"  ✗ Error fetching locations: {e}")
            break

    logger.log(f"  ✓ Built lookup table with {len(location_lookup)} locations")
    return location_lookup


def fetch_openaq_latest_measurements(
    parameter_id: int,
    parameter_name: str,
    logger: Logger,
    limit: int = ITEMS_PER_PAGE
) -> List[Dict]:
    """
    Fetch latest measurements for a specific parameter from OpenAQ v3.

    Args:
        parameter_id: OpenAQ parameter ID
        parameter_name: Human-readable parameter name
        logger: Logger instance
        limit: Max items per page

    Returns:
        List of measurement dictionaries
    """
    logger.log(f"Fetching latest {parameter_name} measurements from OpenAQ v3...")

    url = f"{OPENAQ_BASE_URL}/parameters/{parameter_id}/latest"
    headers = {
        'X-API-Key': OPENAQ_API_KEY,
        'Accept': 'application/json'
    }

    all_measurements = []
    page = 1

    while page <= MAX_PAGES_MEASUREMENTS:
        params = {
            'limit': min(limit, ITEMS_PER_PAGE),
            'page': page
        }

        try:
            response = requests.get(url, headers=headers, params=params, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()

            data = response.json()
            results = data.get('results', [])

            if not results:
                break

            logger.log(f"  Page {page}: {len(results)} measurements", print_override=False)
            all_measurements.extend(results)

            # Check if we've retrieved all results
            meta = data.get('meta', {})
            found = meta.get('found', 0)
            if isinstance(found, int) and found <= len(all_measurements):
                break

            page += 1
            time.sleep(REQUEST_DELAY)

        except requests.exceptions.RequestException as e:
            logger.log(f"  ✗ Error fetching {parameter_name}: {e}")
            break

    logger.log(f"  ✓ Fetched {len(all_measurements)} {parameter_name} measurements")
    return all_measurements


def parse_openaq_measurements(
    measurements: List[Dict],
    parameter_name: str,
    location_lookup: Dict[int, Dict[str, str]]
) -> pd.DataFrame:
    """
    Parse OpenAQ measurements into a structured DataFrame.

    Args:
        measurements: List of measurement dictionaries
        parameter_name: Parameter name
        location_lookup: Location metadata lookup

    Returns:
        DataFrame with parsed measurements
    """
    records = []

    for m in measurements:
        try:
            location_id = m.get('locationsId')
            location_info = location_lookup.get(location_id, {})

            coordinates = m.get('coordinates', {})
            value = m.get('value')
            datetime_str = m.get('datetime', {}).get('utc') if m.get('datetime') else None

            if value is not None:
                record = {
                    'parameter': parameter_name,
                    'value': float(value),
                    'location_id': location_id,
                    'location_name': location_info.get('location_name', 'Unknown'),
                    'country_code': location_info.get('country_code', 'Unknown'),
                    'country': location_info.get('country', 'Unknown'),
                    'city': location_info.get('city', 'Unknown'),
                    'latitude': coordinates.get('latitude'),
                    'longitude': coordinates.get('longitude'),
                    'datetime': datetime_str,
                    'sensors_id': m.get('sensorsId')
                }
                records.append(record)
        except Exception:
            continue

    return pd.DataFrame(records)


def fetch_all_openaq_data(logger: Logger) -> pd.DataFrame:
    """
    Fetch all OpenAQ data for all configured parameters.

    Args:
        logger: Logger instance

    Returns:
        Combined DataFrame with all OpenAQ data
    """
    logger.log("\n" + "=" * 80)
    logger.log("FETCHING OPENAQ DATA")
    logger.log("=" * 80)

    all_openaq_data = []

    for param_key, param_id in OPENAQ_PARAMETERS.items():
        # Fetch location metadata
        location_lookup = fetch_openaq_locations(param_id, param_key.upper(), logger)

        # Skip if location lookup failed
        if not location_lookup:
            logger.log(f"  ⚠ Skipping {param_key.upper()} - no location data available")
            time.sleep(1)
            continue

        # Fetch measurements
        measurements = fetch_openaq_latest_measurements(param_id, param_key.upper(), logger)

        if measurements and location_lookup:
            df = parse_openaq_measurements(measurements, param_key.upper(), location_lookup)
            if not df.empty:
                all_openaq_data.append(df)
                valid_countries = (df['country'] != 'Unknown').sum()
                logger.log(f"  ✓ Parsed {len(df)} valid {param_key.upper()} records")
                logger.log(f"    → {valid_countries}/{len(df)} records with valid country data")

        time.sleep(1)

    if all_openaq_data:
        df_openaq = pd.concat(all_openaq_data, ignore_index=True)
        logger.log(f"\n✓ Total OpenAQ records: {len(df_openaq)}")
        logger.log(f"  Countries: {df_openaq['country'].nunique()}")
        logger.log(f"  Cities: {df_openaq['city'].nunique()}")
        logger.log(f"  Parameters: {df_openaq['parameter'].unique().tolist()}")
        return df_openaq
    else:
        logger.log("\n✗ No OpenAQ data collected")
        return pd.DataFrame()


# ============================================================================
# WORLD BANK API FUNCTIONS
# ============================================================================

def fetch_world_bank_indicator(
    indicator_code: str,
    indicator_name: str,
    logger: Logger,
    start_year: int = WB_START_YEAR,
    end_year: int = WB_END_YEAR
) -> pd.DataFrame:
    """
    Fetch World Bank indicator data using wbgapi.

    Args:
        indicator_code: World Bank indicator code
        indicator_name: Human-readable indicator name
        logger: Logger instance
        start_year: Start year for data
        end_year: End year for data

    Returns:
        DataFrame with indicator data
    """
    logger.log(f"Fetching {indicator_name}...")

    try:
        # Fetch data
        df = wb.data.DataFrame(
            indicator_code,
            economy='all',
            time=range(start_year, end_year + 1),
            skipBlanks=True,
            columns='series'
        )

        # Process DataFrame
        df = df.reset_index()
        df.columns = ['country_code', 'year'] + [indicator_name]
        df['year'] = pd.to_numeric(df['year'].str.replace('YR', ''), errors='coerce')
        df = df[df['year'].notna()]
        df = df[df[indicator_name].notna()]
        df['year'] = df['year'].astype(int)

        # Get country names
        country_names = {}
        try:
            for code in df['country_code'].unique()[:100]:
                try:
                    country_info = wb.economy.get(code)
                    country_names[code] = country_info.get('value', code)
                except:
                    country_names[code] = code
        except:
            pass

        df['country'] = df['country_code'].map(country_names).fillna(df['country_code'])
        logger.log(f"  ✓ Fetched {len(df)} records ({df['country'].nunique()} countries)")
        return df

    except Exception as e:
        logger.log(f"  ✗ Error: {e}")
        return pd.DataFrame()


def fetch_all_world_bank_data(logger: Logger) -> pd.DataFrame:
    """
    Fetch all World Bank data for all configured indicators.

    Args:
        logger: Logger instance

    Returns:
        Combined DataFrame with all World Bank data
    """
    logger.log("\n" + "=" * 80)
    logger.log("FETCHING WORLD BANK DATA")
    logger.log("=" * 80)

    wb_data_frames = {}

    for key, indicator_code in WORLD_BANK_INDICATORS.items():
        df = fetch_world_bank_indicator(indicator_code, key, logger)
        if not df.empty:
            wb_data_frames[key] = df

    if wb_data_frames:
        logger.log("\nMerging World Bank datasets...")
        df_wb = list(wb_data_frames.values())[0]

        for df in list(wb_data_frames.values())[1:]:
            df_wb = df_wb.merge(df, on=['country_code', 'country', 'year'], how='outer')

        logger.log(f"✓ Combined World Bank data: {len(df_wb)} records")
        logger.log(f"  Countries: {df_wb['country'].nunique()}")
        logger.log(f"  Years: {df_wb['year'].min()}-{df_wb['year'].max()}")
        return df_wb
    else:
        logger.log("\n✗ No World Bank data collected")
        return pd.DataFrame()


# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

def check_cached_data(logger: Logger) -> Tuple[bool, bool]:
    """
    Check if data already exists locally.

    Args:
        logger: Logger instance

    Returns:
        Tuple of (openaq_exists, worldbank_exists)
    """
    logger.log("=" * 80)
    logger.log("CHECKING FOR LOCAL DATA")
    logger.log("=" * 80)

    openaq_path = DATA_DIR / OPENAQ_RAW_CSV
    wb_path = DATA_DIR / WORLDBANK_RAW_CSV

    openaq_exists = openaq_path.exists()
    wb_exists = wb_path.exists()

    logger.log(f"OpenAQ data exists locally: {openaq_exists}")
    logger.log(f"World Bank data exists locally: {wb_exists}")

    return openaq_exists, wb_exists


def load_cached_data(logger: Logger) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Load data from local cache files.

    Args:
        logger: Logger instance

    Returns:
        Tuple of (openaq_df, worldbank_df)
    """
    logger.log("\nLoading data from local files...")

    openaq_path = DATA_DIR / OPENAQ_RAW_CSV
    wb_path = DATA_DIR / WORLDBANK_RAW_CSV

    df_openaq = load_csv_if_exists(openaq_path)
    df_wb = load_csv_if_exists(wb_path)

    if not df_openaq.empty:
        logger.log(f"✓ Loaded {len(df_openaq)} OpenAQ records from local cache")

    if not df_wb.empty:
        logger.log(f"✓ Loaded {len(df_wb)} World Bank records from cache")

    return df_openaq, df_wb


def save_raw_data(
    df_openaq: pd.DataFrame,
    df_wb: pd.DataFrame,
    logger: Logger
):
    """
    Save raw data to files.

    Args:
        df_openaq: OpenAQ DataFrame
        df_wb: World Bank DataFrame
        logger: Logger instance
    """
    logger.log("\n" + "=" * 80)
    logger.log("SAVING RAW DATA TO FILES")
    logger.log("=" * 80)

    if not df_openaq.empty:
        df_openaq.to_csv(DATA_DIR / OPENAQ_RAW_CSV, index=False)
        df_openaq.to_json(DATA_DIR / 'openaq_raw.json', orient='records', indent=2)
        logger.log("✓ Saved OpenAQ raw data (CSV, JSON)")

    if not df_wb.empty:
        df_wb.to_csv(DATA_DIR / WORLDBANK_RAW_CSV, index=False)
        df_wb.to_json(DATA_DIR / 'worldbank_raw.json', orient='records', indent=2)
        logger.log("✓ Saved World Bank raw data (CSV, JSON)")


# ============================================================================
# HIGH-LEVEL FETCH FUNCTION
# ============================================================================

def fetch_or_load_data(
    logger: Logger,
    force_fetch: bool = False
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    """
    Fetch data from APIs or load from cache.

    Args:
        logger: Logger instance
        force_fetch: Force fetching even if cache exists

    Returns:
        Tuple of (openaq_df, worldbank_df)
    """
    openaq_exists, wb_exists = check_cached_data(logger)

    # Use cache if available and not forcing fetch
    if not force_fetch and openaq_exists and wb_exists:
        logger.log("\n✓ Using cached data from local files")
        return load_cached_data(logger)

    # Fetch data
    logger.log("\n⚠ Local data not found or force fetch enabled - fetching from APIs...")

    df_openaq = pd.DataFrame()
    df_wb = pd.DataFrame()

    if force_fetch or not openaq_exists:
        df_openaq = fetch_all_openaq_data(logger)
    else:
        df_openaq = load_csv_if_exists(DATA_DIR / OPENAQ_RAW_CSV)
        logger.log(f"\n✓ Loaded {len(df_openaq)} OpenAQ records from cache")

    if force_fetch or not wb_exists:
        df_wb = fetch_all_world_bank_data(logger)
    else:
        df_wb = load_csv_if_exists(DATA_DIR / WORLDBANK_RAW_CSV)
        logger.log(f"\n✓ Loaded {len(df_wb)} World Bank records from cache")

    # Save newly fetched data
    save_raw_data(df_openaq, df_wb, logger)

    return df_openaq, df_wb
