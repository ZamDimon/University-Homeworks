"""
Package responsible for calculating descriptive statistics for 
the air quality data, including mean, median, mode, min, max, kurtosis, skewness, and standard deviation.
"""

import pandas as pd
from scipy import stats
import numpy as np


def calculate_descriptive_stats(df, pollutant_columns):
    """
    Calculates descriptive statistics for each pollutant, grouped by year and overall.
    """
    
    all_stats = []

    if df.empty or df.index.empty:
        print("Warning: DataFrame is empty or has no valid DatetimeIndex. Cannot calculate yearly stats.")
        return pd.DataFrame()

    if not isinstance(df.index, pd.DatetimeIndex):
        print("Warning: Index is not a DatetimeIndex. Cannot extract year.")
        
        try:
            df.index = pd.to_datetime(df.index)
        except Exception as e:
            print(f"Error converting index to DatetimeIndex: {e}")
            return pd.DataFrame()

    df_with_year = df.copy()
    df_with_year['Year'] = df_with_year.index.year

    if df_with_year['Year'].isnull().all():
        print("Warning: Could not extract valid years from the DataFrame index.")
        years = []
    else:
        years = sorted(df_with_year['Year'].dropna().unique().astype(int))

    for col in pollutant_columns:
        # Overall statistics
        data_series = df_with_year[col].dropna()
        if not data_series.empty:
            mode_result = stats.mode(data_series, keepdims=True)
            mode_val = mode_result.mode[0] if mode_result.mode.size > 0 else np.nan

            stats_dict = {
                'Pollutant': col,
                'Year': 'Overall',
                'Mean': data_series.mean(),
                'Median': data_series.median(),
                'Mode': mode_val,
                'Min': data_series.min(),
                'Max': data_series.max(),
                'Kurtosis': data_series.kurtosis(),
                'Skewness': data_series.skew(),
                'Std Dev': data_series.std()
            }
            all_stats.append(stats_dict)

        # Per-year statistics
        for year in years:
            year_data = df_with_year[df_with_year['Year'] == year][col].dropna()
            if not year_data.empty:
                mode_result_year = stats.mode(year_data, keepdims=True)
                mode_val_year = mode_result_year.mode[0] if mode_result_year.mode.size > 0 else np.nan

                stats_dict_year = {
                    'Pollutant': col,
                    'Year': str(year),
                    'Mean': year_data.mean(),
                    'Median': year_data.median(),
                    'Mode': mode_val_year,
                    'Min': year_data.min(),
                    'Max': year_data.max(),
                    'Kurtosis': year_data.kurtosis(),
                    'Skewness': year_data.skew(),
                    'Std Dev': year_data.std()
                }
                all_stats.append(stats_dict_year)

    stats_df = pd.DataFrame(all_stats)
    if not stats_df.empty:
        stats_df['Year'] = stats_df['Year'].astype(str)
        stats_df = stats_df.set_index(['Pollutant', 'Year'])
    
    return stats_df
