"""
Utility Functions
=================
Common utilities for logging, file operations, and data dictionary generation.
"""

import json
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from src.config import (
    LOGS_DIR, DB_DIR, CLEANED_DIR,
    LOG_DATE_FORMAT, LOG_FILE_PREFIX, PREPROCESSING_LOG_PREFIX
)


# ============================================================================
# LOGGING UTILITIES
# ============================================================================

class Logger:
    """
    Simple logger that writes to both console and buffer.
    Can be saved to file at any time.
    """

    def __init__(self, print_to_console: bool = True):
        """
        Initialize logger.

        Args:
            print_to_console: Whether to print messages to console
        """
        self.buffer: List[str] = []
        self.print_to_console = print_to_console

    def log(self, message: str, print_override: bool = None):
        """
        Log a message to buffer and optionally print.

        Args:
            message: Message to log
            print_override: Override the print_to_console setting
        """
        timestamp = datetime.now().strftime(LOG_DATE_FORMAT)
        log_entry = f"[{timestamp}] {message}"
        self.buffer.append(log_entry)

        should_print = print_override if print_override is not None else self.print_to_console
        if should_print:
            print(message)

    def save(self, log_dir: Path = LOGS_DIR, prefix: str = LOG_FILE_PREFIX):
        """
        Save all logs to file.

        Args:
            log_dir: Directory to save logs
            prefix: Prefix for log filename
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        log_file = log_dir / f"{prefix}_{timestamp}.log"

        with open(log_file, 'w') as f:
            f.write('\n'.join(self.buffer))

        print(f"\n✓ Logs saved to {log_file}")

    def get_logs(self) -> List[str]:
        """Get all log entries."""
        return self.buffer.copy()

    def clear(self):
        """Clear log buffer."""
        self.buffer.clear()


# ============================================================================
# DATA DICTIONARY GENERATION
# ============================================================================

def create_data_dictionary(df: pd.DataFrame, dataset_name: str) -> Dict[str, Any]:
    """
    Create a data dictionary (schema information) for a DataFrame.

    Args:
        df: DataFrame to document
        dataset_name: Name of the dataset

    Returns:
        Dictionary containing schema information
    """
    if df.empty:
        return {
            'dataset_name': dataset_name,
            'generated_date': datetime.now().strftime(LOG_DATE_FORMAT),
            'total_rows': 0,
            'total_columns': 0,
            'columns': []
        }

    dictionary = {
        'dataset_name': dataset_name,
        'generated_date': datetime.now().strftime(LOG_DATE_FORMAT),
        'total_rows': len(df),
        'total_columns': len(df.columns),
        'columns': []
    }

    for col in df.columns:
        col_info = {
            'name': col,
            'data_type': str(df[col].dtype),
            'non_null_count': int(df[col].notna().sum()),
            'null_count': int(df[col].isna().sum()),
            'unique_values': int(df[col].nunique()),
            'sample_values': df[col].dropna().head(5).tolist()
        }

        # Add statistics for numerical columns
        if df[col].dtype in ['int64', 'float64']:
            col_info['min'] = float(df[col].min()) if pd.notna(df[col].min()) else None
            col_info['max'] = float(df[col].max()) if pd.notna(df[col].max()) else None
            col_info['mean'] = float(df[col].mean()) if pd.notna(df[col].mean()) else None
            col_info['median'] = float(df[col].median()) if pd.notna(df[col].median()) else None

        dictionary['columns'].append(col_info)

    return dictionary


def save_data_dictionary(df: pd.DataFrame, dataset_name: str, output_dir: Path = DB_DIR):
    """
    Save data dictionary to JSON file.

    Args:
        df: DataFrame to document
        dataset_name: Name of the dataset
        output_dir: Directory to save dictionary
    """
    if df.empty:
        return

    dictionary = create_data_dictionary(df, dataset_name)
    output_file = output_dir / f'{dataset_name}_data_dictionary.json'

    with open(output_file, 'w') as f:
        json.dump(dictionary, f, indent=2)


# ============================================================================
# FILE OPERATIONS
# ============================================================================

def check_file_exists(file_path: Path) -> bool:
    """
    Check if a file exists.

    Args:
        file_path: Path to file

    Returns:
        True if file exists, False otherwise
    """
    return file_path.exists() and file_path.is_file()


def load_csv_if_exists(file_path: Path) -> pd.DataFrame:
    """
    Load CSV file if it exists, otherwise return empty DataFrame.

    Args:
        file_path: Path to CSV file

    Returns:
        DataFrame with data or empty DataFrame
    """
    if check_file_exists(file_path):
        return pd.read_csv(file_path)
    return pd.DataFrame()


def save_dataframe_multiple_formats(
    df: pd.DataFrame,
    base_path: Path,
    base_name: str,
    formats: List[str] = ['csv', 'json']
):
    """
    Save DataFrame in multiple formats.

    Args:
        df: DataFrame to save
        base_path: Directory to save files
        base_name: Base name for files (without extension)
        formats: List of formats ('csv', 'json', 'parquet')
    """
    if df.empty:
        return

    saved_formats = []

    if 'csv' in formats:
        df.to_csv(base_path / f'{base_name}.csv', index=False)
        saved_formats.append('CSV')

    if 'json' in formats:
        df.to_json(base_path / f'{base_name}.json', orient='records', indent=2)
        saved_formats.append('JSON')

    if 'parquet' in formats:
        try:
            import pyarrow
            df.to_parquet(base_path / f'{base_name}.parquet', index=False)
            saved_formats.append('Parquet')
        except ImportError:
            pass  # Skip if pyarrow not available
        except Exception:
            pass  # Skip on error

    return saved_formats


# ============================================================================
# ISO COUNTRY CODE MAPPING
# ============================================================================

def get_iso_country_code_mapping() -> Dict[str, str]:
    """
    Get mapping between ISO 2-letter (OpenAQ) and 3-letter (World Bank) country codes.

    Returns:
        Dictionary mapping 2-letter codes to 3-letter codes
    """
    # ISO 3166-1 alpha-2 to alpha-3 mapping
    iso_mapping = {
        'AF': 'AFG', 'AL': 'ALB', 'DZ': 'DZA', 'AD': 'AND', 'AO': 'AGO',
        'AR': 'ARG', 'AM': 'ARM', 'AU': 'AUS', 'AT': 'AUT', 'AZ': 'AZE',
        'BS': 'BHS', 'BH': 'BHR', 'BD': 'BGD', 'BB': 'BRB', 'BY': 'BLR',
        'BE': 'BEL', 'BZ': 'BLZ', 'BJ': 'BEN', 'BT': 'BTN', 'BO': 'BOL',
        'BA': 'BIH', 'BW': 'BWA', 'BR': 'BRA', 'BN': 'BRN', 'BG': 'BGR',
        'BF': 'BFA', 'BI': 'BDI', 'KH': 'KHM', 'CM': 'CMR', 'CA': 'CAN',
        'CV': 'CPV', 'CF': 'CAF', 'TD': 'TCD', 'CL': 'CHL', 'CN': 'CHN',
        'CO': 'COL', 'KM': 'COM', 'CG': 'COG', 'CR': 'CRI', 'HR': 'HRV',
        'CU': 'CUB', 'CY': 'CYP', 'CZ': 'CZE', 'DK': 'DNK', 'DJ': 'DJI',
        'DO': 'DOM', 'EC': 'ECU', 'EG': 'EGY', 'SV': 'SLV', 'GQ': 'GNQ',
        'ER': 'ERI', 'EE': 'EST', 'ET': 'ETH', 'FJ': 'FJI', 'FI': 'FIN',
        'FR': 'FRA', 'GA': 'GAB', 'GM': 'GMB', 'GE': 'GEO', 'DE': 'DEU',
        'GH': 'GHA', 'GR': 'GRC', 'GT': 'GTM', 'GN': 'GIN', 'GW': 'GNB',
        'GY': 'GUY', 'HT': 'HTI', 'HN': 'HND', 'HU': 'HUN', 'IS': 'ISL',
        'IN': 'IND', 'ID': 'IDN', 'IR': 'IRN', 'IQ': 'IRQ', 'IE': 'IRL',
        'IL': 'ISR', 'IT': 'ITA', 'JM': 'JAM', 'JP': 'JPN', 'JO': 'JOR',
        'KZ': 'KAZ', 'KE': 'KEN', 'KI': 'KIR', 'KW': 'KWT', 'KG': 'KGZ',
        'LA': 'LAO', 'LV': 'LVA', 'LB': 'LBN', 'LS': 'LSO', 'LR': 'LBR',
        'LY': 'LBY', 'LT': 'LTU', 'LU': 'LUX', 'MG': 'MDG', 'MW': 'MWI',
        'MY': 'MYS', 'MV': 'MDV', 'ML': 'MLI', 'MT': 'MLT', 'MR': 'MRT',
        'MU': 'MUS', 'MX': 'MEX', 'MD': 'MDA', 'MC': 'MCO', 'MN': 'MNG',
        'ME': 'MNE', 'MA': 'MAR', 'MZ': 'MOZ', 'MM': 'MMR', 'NA': 'NAM',
        'NP': 'NPL', 'NL': 'NLD', 'NZ': 'NZL', 'NI': 'NIC', 'NE': 'NER',
        'NG': 'NGA', 'NO': 'NOR', 'OM': 'OMN', 'PK': 'PAK', 'PA': 'PAN',
        'PG': 'PNG', 'PY': 'PRY', 'PE': 'PER', 'PH': 'PHL', 'PL': 'POL',
        'PT': 'PRT', 'QA': 'QAT', 'KR': 'KOR', 'RO': 'ROU', 'RU': 'RUS',
        'RW': 'RWA', 'SA': 'SAU', 'SN': 'SEN', 'RS': 'SRB', 'SL': 'SLE',
        'SG': 'SGP', 'SK': 'SVK', 'SI': 'SVN', 'SB': 'SLB', 'SO': 'SOM',
        'ZA': 'ZAF', 'ES': 'ESP', 'LK': 'LKA', 'SD': 'SDN', 'SR': 'SUR',
        'SZ': 'SWZ', 'SE': 'SWE', 'CH': 'CHE', 'SY': 'SYR', 'TJ': 'TJK',
        'TZ': 'TZA', 'TH': 'THA', 'TG': 'TGO', 'TO': 'TON', 'TT': 'TTO',
        'TN': 'TUN', 'TR': 'TUR', 'TM': 'TKM', 'UG': 'UGA', 'UA': 'UKR',
        'AE': 'ARE', 'GB': 'GBR', 'US': 'USA', 'UY': 'URY', 'UZ': 'UZB',
        'VU': 'VUT', 'VE': 'VEN', 'VN': 'VNM', 'YE': 'YEM', 'ZM': 'ZMB',
        'ZW': 'ZWE', 'TW': 'TWN', 'PS': 'PSE', 'CD': 'COD'
    }
    return iso_mapping


# ============================================================================
# FORMATTING UTILITIES
# ============================================================================

def format_section_header(title: str, char: str = '=', length: int = 80) -> str:
    """
    Create a formatted section header.

    Args:
        title: Title text
        char: Character to use for separator
        length: Total length of separator

    Returns:
        Formatted header string
    """
    return f"{char * length}\n{title}\n{char * length}"


def format_number(num: int) -> str:
    """Format number with thousand separators."""
    return f"{num:,}"


def format_percentage(value: float, total: float, decimals: int = 2) -> str:
    """Format as percentage."""
    if total == 0:
        return "0.00%"
    return f"{(value / total * 100):.{decimals}f}%"
