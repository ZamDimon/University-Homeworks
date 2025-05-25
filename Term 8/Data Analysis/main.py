"""
File for processing the air quality data from Khmelnytskyi, Ukraine.
"""

import os
from pathlib import Path # Added for type hinting
import pandas as pd
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt

# Internal imports
from src.preprocessing import load_and_preprocess_data, fill_small_gaps, fill_all_gaps


def calculate_descriptive_stats(df, pollutant_columns):
    """
    Calculates descriptive statistics for each pollutant, grouped by year and overall.
    """
    all_stats = []

    if df.empty or df.index.empty:
        print("Warning: DataFrame is empty or has no valid DatetimeIndex. Cannot calculate yearly stats.")
        return pd.DataFrame()

    # Ensure the index is a DatetimeIndex
    if not isinstance(df.index, pd.DatetimeIndex):
        print("Warning: Index is not a DatetimeIndex. Cannot extract year.")
        try:
            df.index = pd.to_datetime(df.index)
        except Exception as e:
            print(f"Error converting index to DatetimeIndex: {e}")
            return pd.DataFrame()

    df_with_year = df.copy()
    df_with_year['Year'] = df_with_year.index.year

    # Handle cases where there might be no valid years (e.g., all NaT in index)
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
                    'Year': str(year), # Ensure year is string for consistency with 'Overall'
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

def plot_overall_means_pdf(stats_df, output_dir="plots"):
    """
    Generates and saves a single plot comparing the 'Overall' mean
    values across all pollutants. Saves as PDF with 300 dpi.
    """
    if stats_df.empty:
        print("Statistics DataFrame is empty. No plot will be generated.")
        return

    output_path = Path(output_dir)
    if not output_path.exists():
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

    try:
        # Ensure 'Overall' exists in the 'Year' level of the MultiIndex
        if 'Overall' not in stats_df.index.get_level_values('Year'):
            print("No 'Overall' data found in statistics. Skipping plot.")
            return

        # Extract 'Overall' 'Mean' values and sort them
        overall_means = stats_df.xs('Overall', level='Year')['Mean'].sort_values()

        if overall_means.empty:
            print("No 'Overall' 'Mean' data to plot.")
            return

        # Create the plot
        plt.figure(figsize=(12, 8)) # Adjusted size slightly for PDF
        overall_means.plot(kind='barh', colormap='plasma')
        plt.title('Overall Mean Air Pollutant Values in Khmelnytskyi')
        plt.xlabel('Mean Value (Concentration / Index)')
        plt.ylabel('Pollutant')
        plt.grid(axis='x', linestyle='--', alpha=0.6) # Add grid lines for readability
        plt.tight_layout() # Adjust layout to prevent labels overlapping

        # Define the output filename and path
        plot_filename = "overall_mean_by_pollutant.pdf"
        full_plot_path = output_path / plot_filename

        # Save the plot as PDF with 300 dpi
        plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
        plt.close() # Close the figure to free up memory
        print(f"📈 Saved high-quality plot to: {full_plot_path}")

    except KeyError:
        print("Could not find 'Mean' statistic or 'Overall' year for plotting.")
    except Exception as e:
        print(f"An error occurred while plotting: {e}")
        

def plot_yearly_means_grouped(stats_df, output_dir="plots"):
    """
    Generates and saves a single grouped bar plot showing mean pollutant levels
    for each year. Saves as PDF with 300 dpi.
    """
    if stats_df.empty:
        print("Statistics DataFrame is empty. No plot will be generated.")
        return

    output_path = Path(output_dir)
    if not output_path.exists():
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

    try:
        # 1. Prepare data: Select 'Mean', reset index, filter out 'Overall'
        mean_stats = stats_df['Mean'].reset_index()
        mean_stats_yearly = mean_stats[mean_stats['Year'] != 'Overall'].copy()

        if mean_stats_yearly.empty:
            print("No yearly data found to plot.")
            return

        # 2. Ensure 'Year' is numeric for sorting, then convert back to string
        mean_stats_yearly['Year'] = pd.to_numeric(mean_stats_yearly['Year'])
        mean_stats_yearly = mean_stats_yearly.sort_values('Year')
        mean_stats_yearly['Year'] = mean_stats_yearly['Year'].astype(str)

        # 3. Pivot data for grouped bar chart (Years as index, Pollutants as columns)
        plot_data = mean_stats_yearly.pivot(index='Year', columns='Pollutant', values='Mean')

        if plot_data.empty:
            print("Could not pivot data for plotting.")
            return

        # 4. Create the plot
        #    Adjust figsize based on the number of years and pollutants
        num_years = len(plot_data.index)
        fig_width = max(10, num_years * 1.5) # Make width dependent on number of years
        ax = plot_data.plot(kind='bar', figsize=(fig_width, 8), width=0.8)

        # 5. Customize the plot
        plt.title('Mean Pollutant Levels by Year in Khmelnytskyi 📊', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Mean Value (Concentration / Index)', fontsize=12)
        plt.xticks(rotation=45, ha='right') # Rotate x-axis labels for better readability
        plt.legend(title='Pollutants', bbox_to_anchor=(1.02, 1), loc='upper left') # Place legend outside
        plt.grid(axis='y', linestyle='--', alpha=0.7) # Add a grid
        plt.tight_layout(rect=[0, 0, 0.88, 1]) # Adjust layout to make space for legend

        # 6. Define the output filename and path
        plot_filename = "yearly_mean_grouped_by_pollutant.pdf"
        full_plot_path = output_path / plot_filename

        # 7. Save the plot as PDF with 300 dpi
        plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
        plt.close() # Close the figure
        print(f"✅ Saved grouped bar plot to: {full_plot_path}")

    except KeyError as e:
        print(f"Error: Could not find expected column for plotting: {e}")
    except Exception as e:
        print(f"An error occurred while generating the grouped bar plot: {e}")


def main():
    """
    Main function to conduct the data loading, processing, analysis, and plotting.
    """
    
    # First, specify the input file path
    input_file_path_str = "csv/khmelnytskyi.csv"
    input_file_path = Path(input_file_path_str)

    # Create 'csv' directory if it doesn't exist
    if not input_file_path.parent.exists():
        os.makedirs(input_file_path.parent)
        print(f"Created directory: {input_file_path.parent}")
        print(f"Please ensure '{input_file_path_str}' exists in this directory before running again.")

    output_filled_small_gaps_path = Path("csv/khmelnytskyi_filled_small_gaps.csv")
    output_filled_all_gaps_path = Path("csv/khmelnytskyi_filled_all_gaps.csv")
    output_stats_path = Path("csv/khmelnytskyi_descriptive_stats.csv")
    plot_output_dir = Path("plots/khmelnytskyi_stats_plots")

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

    # 3. Fill all gaps
    df_filled_all = fill_all_gaps(df_original.copy(), pollutant_columns)
    df_filled_all.to_csv(output_filled_all_gaps_path)
    print(f"Data with all gaps filled saved to: {output_filled_all_gaps_path}\n")

    # 4. Calculate descriptive statistics
    print("Calculating descriptive statistics...")
    descriptive_stats_df = calculate_descriptive_stats(df_filled_all.copy(), pollutant_columns)

    if not descriptive_stats_df.empty:
        print("\nDescriptive Statistics Table:")
        with pd.option_context('display.max_rows', None, 'display.max_columns', None, 'display.width', 1000):
            print(descriptive_stats_df)
        descriptive_stats_df.to_csv(output_stats_path)
        print(f"\nDescriptive statistics saved to: {output_stats_path}")

        # 5. Plot the new grouped bar chart (MODIFIED PART)
        print("\nGenerating the yearly grouped bar plot (PDF)...")
        plot_yearly_means_grouped(descriptive_stats_df.copy(), output_dir=str(plot_output_dir)) # Call the NEW function
    else:
        print("No statistics were calculated. Skipping plot generation.")

    # Update the summary message
    print("\n--- Analysis Complete ---")
    print(f"Summary of generated files:")
    print(f"1. Small gaps filled: {output_filled_small_gaps_path}")
    print(f"2. All gaps filled:   {output_filled_all_gaps_path}")
    print(f"3. Statistics table:  {output_stats_path}")
    print(f"4. Yearly grouped plot: {plot_output_dir / 'yearly_mean_grouped_by_pollutant.pdf'}") # Updated path


if __name__ == "__main__":
    main()