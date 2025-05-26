"""
File for preprocessing air quality data.
"""

from pathlib import Path
import pandas as pd

DEFAULT_MAX_GAP_SIZE: int = 14 # Maximum size of gaps to fill with interpolation. Defaults to 2 weeks.


def load_and_preprocess_data(file_path: Path):
    """
    Loads the CSV data, converts columns to numeric, and parses dates.
    """
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return None, None

    # Convert 'Date' column to datetime objects
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    # Remove rows where date conversion failed
    df = df.dropna(subset=['Date'])
    
    if df.empty:
        print("Error: No valid dates found after parsing. DataFrame is empty.")
        return None, None
    
    df = df.set_index('Date')

    # Identify pollutant columns
    pollutant_columns = df.columns.tolist()

    # Convert pollutant columns to numeric
    for col in pollutant_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    return df, pollutant_columns


def fill_small_gaps(
    df, 
    pollutant_columns, 
    max_gap_size=DEFAULT_MAX_GAP_SIZE, 
    method='linear'
):
    """
    Fills small gaps (NaN sequences of length <= max_gap_size) using interpolation.
    """
    
    df_filled_small = df.copy()
    for col in pollutant_columns:
        df_filled_small[col] = df_filled_small[col].interpolate(method=method, limit=max_gap_size, limit_area='inside')
    
    return df_filled_small


def fill_all_gaps(df, pollutant_columns, method='linear'):
    """
    Fills all gaps in the specified columns using interpolation.
    """
    
    df_filled_all = df.copy()
    for col in pollutant_columns:
        df_filled_all[col] = df_filled_all[col].interpolate(method=method)
        
    return df_filled_all