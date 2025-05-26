"""
File for processing the air quality data from Khmelnytskyi, Ukraine.
"""

import os
import argparse
from pathlib import Path
import pandas as pd

# Internal imports
from src.preprocessing import (
    load_and_preprocess_data, 
    fill_small_gaps, 
    fill_all_gaps
)
from src.statistics import calculate_descriptive_stats
from src.analysis import perform_fft_analysis
from src.plot import (
    plot_overall_means_pdf, 
    plot_yearly_means_grouped,
    plot_density_functions,
    plot_amplitude_spectrum,
    plot_phase_spectrum,
    plot_phase_analysis,
    plot_yearly_distributions,
    plot_monthly_averages_by_year,
)

        
def main():
    """
    Main function to conduct the data loading, processing, analysis, and plotting.
    """
    
    # First, parse the command line arguments
    parser = argparse.ArgumentParser(description="Read a path from the command line")
    parser.add_argument("csv_path", type=Path, help="Path to a file or directory")
    args = parser.parse_args()
    
    # Now, specify the input file path
    assert args.csv_path.exists(), f"Input file {args.csv_path} does not exist. Please provide a valid path."
    input_file_path = args.csv_path

    # Create 'csv' directory if it doesn't exist
    if not input_file_path.parent.exists():
        os.makedirs(input_file_path.parent)
        print(f"Created directory: {input_file_path.parent}")
        print(f"Please ensure '{str(input_file_path)}' exists in this directory before running again.")

    output_filled_small_gaps_path = Path("csv/khmelnytskyi_filled_small_gaps.csv")
    output_filled_all_gaps_path = Path("csv/khmelnytskyi_filled_all_gaps.csv")
    output_stats_path = Path("csv/khmelnytskyi_descriptive_stats.csv")
    plot_output_dir = Path("plots/khmelnytskyi_stats_plots")
    density_plot_output_dir = plot_output_dir / "density_functions"
    spectrum_plot_output_dir = plot_output_dir / "spectrum_analysis"
    phase_plot_output_dir = plot_output_dir / "phase_analysis"
    yearly_comp_output_dir = plot_output_dir / "yearly_comparison"

    # 1. Load and preprocess data
    df_original, pollutant_columns = load_and_preprocess_data(input_file_path)
    if df_original is None or pollutant_columns is None:
        print("Exiting due to error in loading or preprocessing data.")
        return
    if not pollutant_columns:
        print("No pollutant columns found. Exiting.")
        return
    
    print("Original Data (first 5 rows):\n", df_original.head(), "\n")

    # 2. Fill small gaps
    df_filled_small = fill_small_gaps(df_original.copy(), pollutant_columns, max_gap_size=3)
    df_filled_small.to_csv(output_filled_small_gaps_path)
    print(f"Data with small gaps filled saved to: {output_filled_small_gaps_path}\n")

    # 3. Fill all gaps (this will be used further for statistics and plotting)
    df_filled_all = fill_all_gaps(df_original.copy(), pollutant_columns)
    df_filled_all.to_csv(output_filled_all_gaps_path)
    print(f"Data with all gaps filled saved to: {output_filled_all_gaps_path}\n")

    # 4. Calculate descriptive statistics
    print("Calculating descriptive statistics...")
    descriptive_stats_df = calculate_descriptive_stats(df_filled_all.copy(), pollutant_columns)

    # 5. Perform Spectral Analysis
    print("\nPerforming spectral analysis (FFT)...")
    amp_df, phase_df = perform_fft_analysis(df_filled_all.copy(), pollutant_columns, num_harmonics=9)

    # 6. Plotting Statistics
    if not descriptive_stats_df.empty:
        print("\nDescriptive Statistics Table:")
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
            print(descriptive_stats_df)
        descriptive_stats_df.to_csv(output_stats_path)
        print(f"\nDescriptive statistics saved to: {output_stats_path}")

        print("\nGenerating the yearly grouped bar plot (PDF)...")
        plot_yearly_means_grouped(descriptive_stats_df.copy(), output_dir=str(plot_output_dir)) # Call the NEW function
        
        print("\nGenerating the overall means plot (PDF)...")
        plot_overall_means_pdf(descriptive_stats_df.copy(), output_dir=str(plot_output_dir))
        
        print("\nGenerating density function plots (PDF)...")
        plot_density_functions(df_filled_all.copy(), pollutant_columns, output_dir=str(density_plot_output_dir))
    else:
        print("No statistics were calculated. Skipping plot generation.")

    # 7. Plot Spectral Analysis Results
    if amp_df is not None and phase_df is not None:
        print("\nGenerating spectrum plots (PDF)...")
        spectrum_plot_output_dir.mkdir(parents=True, exist_ok=True)
        
        plot_amplitude_spectrum(amp_df, output_dir=str(spectrum_plot_output_dir))
        plot_phase_spectrum(phase_df, output_dir=str(spectrum_plot_output_dir))
    else:
        print("Skipping spectrum plots due to analysis issues.")
    
    # 8. Plot Phase Analysis Results
    print("\nGenerating phase analysis plots (PDF)...")
    plot_phase_analysis(df_filled_all.copy(), pollutant_columns, output_dir=str(phase_plot_output_dir))
    
    # 9. Plot Yearly Comparison Results
    print("\nGenerating yearly comparison plots (PDF)...")
    plot_yearly_distributions(df_filled_all.copy(), pollutant_columns, output_dir=str(yearly_comp_output_dir))
    plot_monthly_averages_by_year(df_filled_all.copy(), pollutant_columns, output_dir=str(yearly_comp_output_dir))
    
    # Update the summary message
    print("Analysis Complete!")


if __name__ == "__main__":
    main()