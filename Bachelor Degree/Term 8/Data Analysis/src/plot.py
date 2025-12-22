"""
Package for visualizing air quality statistics, specifically generating plots
for overall means and yearly means grouped by pollutant.
"""

import os
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from scipy import stats


def plot_yearly_means_grouped(stats_df, output_dir="plots"):
    """
    Generates and saves a single grouped bar plot showing mean pollutant levels
    for each year. 
    """
    
    if stats_df.empty:
        print("Statistics DataFrame is empty. No plot will be generated.")
        return

    output_path = Path(output_dir)
    if not output_path.exists():
        os.makedirs(output_path)
        print(f"Created directory: {output_path}")

    try:
        # 1. Prepare data
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
        num_years = len(plot_data.index)
        fig_width = max(14, num_years * 1.5)
        _ = plot_data.plot(kind='bar', figsize=(fig_width, 8), width=0.8)

        # 5. Setting plot design
        plt.title('Mean Pollutant Levels by Year in Khmelnytskyi', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel('Mean Value (Concentration / Index)', fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend(title='Pollutants', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout(rect=[0, 0, 0.88, 1])

        # 6. Define the output filename and path
        plot_filename = "yearly_mean_grouped_by_pollutant.pdf"
        full_plot_path = output_path / plot_filename

        # 7. Save the plot as PDF
        plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
        plt.close()
        print(f"Saved grouped bar plot to: {full_plot_path}")
        
    except KeyError as e:
        print(f"Error: Could not find expected column for plotting: {e}")
    except Exception as e:
        print(f"An error occurred while generating the grouped bar plot: {e}")


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
        if 'Overall' not in stats_df.index.get_level_values('Year'):
            print("No 'Overall' data found in statistics. Skipping plot.")
            return

        # Extract 'Overall' 'Mean' values and sort them
        overall_means = stats_df.xs('Overall', level='Year')['Mean'].sort_values()

        if overall_means.empty:
            print("No 'Overall' 'Mean' data to plot.")
            return

        # Create the plot
        plt.figure(figsize=(12, 8))
        overall_means.plot(kind='barh', colormap='rainbow')
        plt.title('Overall Mean Air Pollutant Values in Khmelnytskyi')
        plt.xlabel('Mean Value (Concentration / Index)')
        plt.ylabel('Pollutant')
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()

        # Define the output filename and path
        plot_filename = "overall_mean_by_pollutant.pdf"
        full_plot_path = output_path / plot_filename

        # Save the plot
        plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
        plt.close()
        print(f"Saved plot to: {full_plot_path}")
    except KeyError:
        print("Could not find 'Mean' statistic or 'Overall' year for plotting.")
    except Exception as e:
        print(f"An error occurred while plotting: {e}")
    

def plot_density_functions(df, pollutant_columns, output_dir="plots/density_functions"):
    """
    Generates and saves probability density function (PDF/KDE) plots
    for each pollutant in separate files.
    """
    
    if df.empty:
        print("DataFrame is empty. No density plots will be generated.")
        return

    # Ensure the output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Ensured directory exists: {output_path}")

    # Iterate through each pollutant column
    for col in pollutant_columns:
        plt.figure(figsize=(10, 6))
        data_series = df[col].dropna()

        # Check if there is data left to plot
        if data_series.empty:
            print(f"No data for pollutant '{col}'. Skipping density plot.")
            plt.close()
            continue

        # Create the Kernel Density Estimate plot using seaborn
        sns.kdeplot(data_series, fill=True, bw_adjust=0.75) # bw_adjust controls smoothness

        # Customize the plot
        plt.title(f'Probability Density Function for {col}', fontsize=14)
        plt.xlabel(f'{col} Value (Concentration)', fontsize=10)
        plt.ylabel('Density', fontsize=10)
        plt.grid(True, linestyle='--', alpha=0.6)
        plt.tight_layout()

        # Prepare filename (make it filesystem-safe)
        safe_col_name = col.replace(' ', '_').replace('/', '_').lower()
        plot_filename = f"density_{safe_col_name}.pdf"
        full_plot_path = output_path / plot_filename

        # Save the plot
        try:
            plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
            print(f"Saved density plot to: {full_plot_path}")
        except Exception as e:
            print(f"Error saving plot for {col}: {e}")

        plt.close()    


def _plot_spectrum_bars(spec_df, title, ylabel, filename, output_dir):
    """
    Helper function to plot amplitude or phase spectrum as a grouped bar plot.
    """
    
    if spec_df is None or spec_df.empty:
        print(f"No spectrum data provided for {title}. Skipping plot.")
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    num_harmonics, num_pollutants = spec_df.shape
    fig_width = max(12, num_harmonics * num_pollutants * 0.2)

    _ = spec_df.plot(kind='bar', figsize=(fig_width, 7), width=0.8)

    plt.title(title, fontsize=16)
    plt.xlabel('Harmonic Index (Frequency Component)', fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=0)
    plt.legend(title='Pollutants', bbox_to_anchor=(1.02, 1), loc='upper left')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout(rect=[0, 0, 0.88, 1])

    full_plot_path = output_path / f"{filename}.pdf"

    try:
        plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
        plt.close()
        print(f"Saved spectrum plot to: {full_plot_path}")
    except Exception as e:
        print(f"Error saving spectrum plot {full_plot_path}: {e}")


def plot_amplitude_spectrum(amp_df, output_dir="plots"):
    """
    Plots the amplitude spectrum as a grouped bar plot.
    """
    
    _plot_spectrum_bars(amp_df,
                        'Amplitude Spectrum of Pollutant Oscillations',
                        'Amplitude',
                        'amplitude_spectrum',
                        output_dir)


def plot_phase_spectrum(phase_df, output_dir="plots"):
    """
    Plots the phase spectrum as a grouped bar plot.
    """
    
    _plot_spectrum_bars(phase_df,
                        'Phase Spectrum of Pollutant Oscillations',
                        'Phase (Radians)',
                        'phase_spectrum',
                        output_dir)
    
    
def plot_phase_analysis(
    df, 
    pollutant_columns, 
    output_dir="plots/phase_analysis"
) -> None:
    """
    Generates and saves phase analysis plots (derivatives vs. value/derivatives)
    for each pollutant in separate files.
    """
    
    if df.empty:
        print("DataFrame is empty. No phase plots will be generated.")
        return

    # Ensure the output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Ensured directory exists: {output_path}")

    # Iterate through each pollutant column
    for col in pollutant_columns:
        # Calculate value and derivatives
        x = df[col]
        dx_dt = df[col].diff()  # 1st derivative (velocity)
        d2x_dt2 = dx_dt.diff() # 2nd derivative (acceleration)

        plot_df = pd.DataFrame({
            'x': x,
            'dx_dt': dx_dt,
            'd2x_dt2': d2x_dt2
        }).dropna()

        # Check if there is data left to plot
        if plot_df.empty:
            print(f"Not enough data (after differentiation) for {col}. Skipping phase plot.")
            continue
        
        # Save the derivative data to CSV
        safe_col_name = col.replace(' ', '_').replace('/', '_').lower()
        csv_filename = f"phase_data_{safe_col_name}.csv"
        full_csv_path = output_path / csv_filename
        try:
            plot_df.to_csv(full_csv_path)
            print(f"Saved phase derivative data for {col} to: {full_csv_path}")
        except Exception as e:
            print(f"Error saving phase data CSV for {col}: {e}")

        # Create a figure with 3 subplots for three phase portraits
        fig, axes = plt.subplots(1, 3, figsize=(20, 6)) # 1 row, 3 columns
        fig.suptitle(f'Phase Analysis Plots for {col}', fontsize=16, y=1.03)

        # Plot 1: 1st Der vs. Value (Velocity vs. Position)
        axes[0].scatter(plot_df['x'], plot_df['dx_dt'], s=5, alpha=0.3, color='blue')
        axes[0].set_title('1st Derivative vs. Value')
        axes[0].set_xlabel(f'{col} (Position)')
        axes[0].set_ylabel('1st Derivative (Velocity)')
        axes[0].grid(True, linestyle='--', alpha=0.6)

        # Plot 2: 2nd Der vs. Value (Acceleration vs. Position)
        axes[1].scatter(plot_df['x'], plot_df['d2x_dt2'], s=5, alpha=0.3, color='green')
        axes[1].set_title('2nd Derivative vs. Value')
        axes[1].set_xlabel(f'{col} (Position)')
        axes[1].set_ylabel('2nd Derivative (Acceleration)')
        axes[1].grid(True, linestyle='--', alpha=0.6)

        # Plot 3: 2nd Der vs. 1st Der (Phase Portrait)
        axes[2].scatter(plot_df['dx_dt'], plot_df['d2x_dt2'], s=5, alpha=0.3, color='red')
        axes[2].set_title('Phase Portrait (Acceleration vs. Velocity)')
        axes[2].set_xlabel('1st Derivative (Velocity)')
        axes[2].set_ylabel('2nd Derivative (Acceleration)')
        axes[2].grid(True, linestyle='--', alpha=0.6)

        plt.tight_layout(rect=[0, 0.03, 1, 0.98])

        # Prepare filename and save
        safe_col_name = col.replace(' ', '_').replace('/', '_').lower()
        plot_filename = f"phase_analysis_{safe_col_name}.pdf"
        full_plot_path = output_path / plot_filename

        try:
            plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
            print(f"Saved phase plot to: {full_plot_path}")
        except Exception as e:
            print(f"Error saving phase plot for {col}: {e}")

        plt.close(fig)


def plot_yearly_distributions(df, pollutant_columns, output_dir="plots/yearly_comparison"):
    """
    Generates and saves box plots showing the distribution of each pollutant
    level for each year.
    """
    
    print("\nGenerating yearly distribution box plots...")
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Ensured directory exists: {output_path}")

    df_with_year = df.copy()
    df_with_year.index = pd.to_datetime(df_with_year.index)
    df_with_year = df_with_year[df_with_year.index.notna()]
    df_with_year['Year'] = df_with_year.index.year

    for col in pollutant_columns:
        plt.figure(figsize=(12, 7))

        if col not in df_with_year or df_with_year[col].isnull().all():
            print(f"No data for pollutant '{col}'. Skipping yearly box plot.")
            plt.close()
            continue

        # Again, setting some styles and stuff
        sns.boxplot(x='Year', y=col, data=df_with_year, palette="viridis")
        plt.title(f'Yearly Distribution of {col}', fontsize=16)
        plt.xlabel('Year', fontsize=12)
        plt.ylabel(f'{col} Level', fontsize=12)
        plt.grid(axis='y', linestyle='--', alpha=0.6)
        plt.tight_layout()

        safe_col_name = col.replace(' ', '_').replace('/', '_').lower()
        full_plot_path = output_path / f"boxplot_yearly_{safe_col_name}.pdf"

        try:
            plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
            print(f"Saved yearly box plot to: {full_plot_path}")
        except Exception as e:
            print(f"Error saving box plot for {col}: {e}")

        plt.close()


def plot_monthly_averages_by_year(df, pollutant_columns, output_dir="plots/yearly_comparison"):
    """
    Generates and saves line plots comparing the monthly average of each
    pollutant across different years.
    """
    
    print("\nGenerating monthly average comparison plots...")
    
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True) # Ensure dir exists

    df_monthly = df.copy()
    df_monthly.index = pd.to_datetime(df_monthly.index)
    df_monthly = df_monthly[df_monthly.index.notna()]
    df_monthly['Year'] = df_monthly.index.year
    df_monthly['Month'] = df_monthly.index.month

    for col in pollutant_columns:
        if col not in df_monthly or df_monthly[col].isnull().all():
            print(f"No data for pollutant '{col}'. Skipping monthly avg plot.")
            continue

        monthly_avg = df_monthly.groupby(['Year', 'Month'])[col].mean().unstack(level=0)

        if monthly_avg.empty:
            print(f"Could not compute monthly averages for {col}. Skipping plot.")
            continue

        plt.figure(figsize=(14, 8))
        ax = plt.gca()

        num_years = len(monthly_avg.columns)
        cmap = plt.get_cmap('viridis')
        colors = [cmap(i) for i in np.linspace(0, 1, num_years)]

        monthly_avg.plot(ax=ax, marker='o', linestyle='-', color=colors)

        plt.title(f'Monthly Average {col} - Year by Year Comparison', fontsize=16)
        plt.xlabel('Month', fontsize=12)
        plt.ylabel(f'Mean {col} Level', fontsize=12)
        plt.xticks(range(1, 13), ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
        plt.legend(title='Year', bbox_to_anchor=(1.02, 1), loc='upper left')
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout(rect=[0, 0, 0.88, 1])

        safe_col_name = col.replace(' ', '_').replace('/', '_').lower()
        full_plot_path = output_path / f"monthly_avg_{safe_col_name}.pdf"

        try:
            plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
            print(f"Saved monthly avg plot to: {full_plot_path}")
        except Exception as e:
            print(f"Error saving monthly avg plot for {col}: {e}")

        plt.close()


def plot_correlation_heatmap(correlation_matrix, output_dir="plots") -> None:
    """
    Plots a heatmap of the pollutant correlation matrix.

    Args:
        correlation_matrix (pd.DataFrame): The correlation matrix to plot.
        output_dir (str): Directory to save the heatmap PDF.
    """
    
    print("Generating correlation heatmap...")
    if correlation_matrix is None or correlation_matrix.empty:
        print("Correlation matrix is empty or None. Skipping heatmap plot.")
        return

    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    heatmap_file_path = output_path / "pollutant_correlation_heatmap.pdf"

    plt.figure(figsize=(max(10, len(correlation_matrix.columns) * 0.8), max(8, len(correlation_matrix.columns) * 0.7)))
    sns.heatmap(
        correlation_matrix,
        annot=True,          
        cmap='coolwarm',     
        fmt=".2f",          
        linewidths=.5,       
        vmin=-1, vmax=1,    
        cbar_kws={'label': 'Correlation Coefficient'}
    )
    plt.title('Correlation Matrix Heatmap', fontsize=16)
    plt.xticks(rotation=45, ha="right", fontsize=10)
    plt.yticks(rotation=0, fontsize=10)
    plt.tight_layout()

    try:
        plt.savefig(heatmap_file_path, dpi=300, format='pdf')
        print(f"Correlation heatmap saved to: {heatmap_file_path}")
    except Exception as e:
        print(f"Error saving correlation heatmap: {e}")
    plt.close()


def plot_linear_regression_scatter(df, predictor_col, outcome_col, output_dir="plots/regression_analysis"):
    """
    Performs linear regression between two pollutants and plots the scatter
    of actual data points along with the fitted regression line.

    Args:
        df (pd.DataFrame): DataFrame containing the pollutant data (preferably filled).
        predictor_col (str): Name of the column to use as the independent variable (X).
        outcome_col (str): Name of the column to use as the dependent variable (Y).
        output_dir (str): Directory to save the plot PDF.
    """
    print(f"\nGenerating linear regression plot for {outcome_col} vs. {predictor_col}...")

    if predictor_col not in df.columns or outcome_col not in df.columns:
        print(f"Error: One or both columns ('{predictor_col}', '{outcome_col}') not found in DataFrame. Skipping regression.")
        return

    # Prepare data: drop NaNs for the specific pair of columns
    regression_data = df[[predictor_col, outcome_col]].dropna()

    if regression_data.empty or len(regression_data) < 2:
        print(f"Not enough data points after dropping NaNs for {predictor_col} and {outcome_col}. Skipping regression.")
        return

    x_data = regression_data[predictor_col]
    y_data = regression_data[outcome_col]

    try:
        # Perform linear regression
        slope, intercept, r_value, p_value, std_err = stats.linregress(x_data, y_data)
        r_squared = r_value**2
    except Exception as e:
        print(f"Error performing linear regression for {outcome_col} vs. {predictor_col}: {e}")
        return

    # Create the plot
    plt.figure(figsize=(10, 7))
    plt.scatter(x_data, y_data, alpha=0.4, label='Actual Daily Data', color='steelblue')

    # Generate points for the regression line
    # To ensure the line spans the range of x_data, even if x_data is not sorted
    x_line = np.array([x_data.min(), x_data.max()])
    y_fit = slope * x_line + intercept
    plt.plot(x_line, y_fit, color='red', linewidth=2,
             label=f'Fitted Line\ny = {slope:.3f}x + {intercept:.3f}\nR² = {r_squared:.3f}')

    plt.title(f'Linear Regression: {outcome_col} vs. {predictor_col}', fontsize=16)
    plt.xlabel(f'{predictor_col} Level', fontsize=12)
    plt.ylabel(f'{outcome_col} Level', fontsize=12)
    plt.legend(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()

    # Ensure the output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # Prepare filename and save
    safe_predictor = predictor_col.replace(' ', '_').replace('/', '_').lower()
    safe_outcome = outcome_col.replace(' ', '_').replace('/', '_').lower()
    plot_filename = f"regression_{safe_outcome}_vs_{safe_predictor}.pdf"
    full_plot_path = output_path / plot_filename

    try:
        plt.savefig(full_plot_path, dpi=300, format='pdf', bbox_inches='tight')
        print(f"Linear regression plot saved to: {full_plot_path}")
    except Exception as e:
        print(f"Error saving regression plot for {outcome_col} vs. {predictor_col}: {e}")

    plt.close()