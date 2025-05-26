"""
Package for performing analysis like Fast Fourier Transform (FFT)
on air quality data.
"""

import pandas as pd
import numpy as np

DEFAULT_NUM_HARMONICS: int = 9  # Default number of harmonics to analyze


def perform_fft_analysis(df, pollutant_columns, num_harmonics: int = DEFAULT_NUM_HARMONICS):
    """
    Performs FFT on each pollutant time series to find amplitudes and phases
    of the first N harmonics (excluding the 0th component).
    """
    
    results = {}

    print(f"Performing FFT for first {num_harmonics} harmonics...")

    for col in pollutant_columns:
        data_series = df[col].dropna()
        N = len(data_series)

        # Check if there's enough data
        if N < (num_harmonics + 1) * 2: # Need at least ~2 points per harmonic
            print(f"Warning: Not enough data for {col} ({N} points). Skipping FFT.")
            continue

        try:
            # Perform FFT
            yf = np.fft.fft(data_series.values)

            # Calculate amplitudes and phases for the first N harmonics (indices 1 to N)
            # Amplitude = 2.0/N * |Y(f)| for f > 0
            amplitudes = 2.0 / N * np.abs(yf[1 : num_harmonics + 1])
            phases = np.angle(yf[1 : num_harmonics + 1]) # Phase in radians

            results[col] = {'Amplitude': amplitudes, 'Phase': phases}

        except Exception as e:
            print(f"Error performing FFT for {col}: {e}")
            continue

    if not results:
        print("FFT analysis failed for all pollutants.")
        return None, None

    # Convert results to DataFrames for easier plotting
    amp_df = pd.DataFrame({k: v['Amplitude'] for k, v in results.items()})
    phase_df = pd.DataFrame({k: v['Phase'] for k, v in results.items()})

    # Set index to '1' through 'num_harmonics'
    harmonic_index = range(1, num_harmonics + 1)
    amp_df.index = harmonic_index
    phase_df.index = harmonic_index
    amp_df.index.name = "Harmonic"
    phase_df.index.name = "Harmonic"

    print("FFT analysis complete.")
    return amp_df, phase_df