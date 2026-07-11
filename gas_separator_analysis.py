"""
Gas Separator Anomaly Detection & Mass Balance Analysis
Author: Amirhossein Kazemi
GitHub: amirhkazemi-chem

This script reads sensor data from a chemical gas separator and:
1. Calculates mass balance error (inlet flow vs outlet flows)
2. Detects outliers using the IQR method
3. Analyzes time-based trends using correlation and rolling averages
4. Produces annotated visualizations for temperature, pressure, and mass balance
"""

import pandas as pd
import matplotlib.pyplot as plt


# ==========================================
# Helper functions
# ==========================================

def get_outliers_iqr(df, column):
    """Detect outliers using the IQR method for a given column.

    Returns the outlier rows plus the lower and upper bounds used.
    NaN values are automatically excluded from the quantile calculation
    by pandas, so missing data will not distort the bounds.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df[column] < lower_bound) | (df[column] > upper_bound)]
    return outliers, lower_bound, upper_bound


def get_time_correlations(df, column, split_at=None):
    """Compute correlation with time: full range, first half, second half.

    Rows with NaN in `column` are automatically excluded by pandas' .corr(),
    so missing values do not need to be dropped manually beforehand.
    """
    if split_at is None:
        split_at = len(df) // 2
    corr_full = df['time_min'].corr(df[column])
    corr_first_half = df['time_min'].iloc[:split_at].corr(df[column].iloc[:split_at])
    corr_second_half = df['time_min'].iloc[split_at:].corr(df[column].iloc[split_at:])
    return corr_full, corr_first_half, corr_second_half


def get_rolling_average(series, window=10):
    """Return rolling average of a series to smooth noise and reveal trend.

    Note: rolling() treats NaN as a missing observation, so a window
    containing a NaN will itself produce NaN until enough valid points
    are available again. This is expected behavior, not a bug.
    """
    return series.rolling(window=window).mean()


def report_missing_values(df):
    """Print a summary of missing values per column, with row indices."""
    for col in df.columns:
        n_missing = df[col].isna().sum()
        if n_missing > 0:
            missing_rows = df[df[col].isna()].index.tolist()
            print(f"Column '{col}': {n_missing} missing value(s) at rows {missing_rows}")


# ==========================================
# Load data
# ==========================================

df = pd.read_csv('../data/final_project_unknown.csv')

print("=== Missing Value Report ===")
report_missing_values(df)
print()

# ==========================================
# Mass balance analysis
# ==========================================

df['mass_balance_error'] = df['flow_in_L_min'] - (df['flow_out1_L_min'] + df['flow_out2_L_min'])

outliers_balance, lb_balance, ub_balance = get_outliers_iqr(df, 'mass_balance_error')
corr_full_b, corr_first_b, corr_second_b = get_time_correlations(df, 'mass_balance_error', split_at=125)
df['rolling_balance'] = get_rolling_average(df['mass_balance_error'])

print("=== Mass Balance Error ===")
print(f"Outliers found: {len(outliers_balance)}")
print(f"Correlation - full: {corr_full_b:.3f}, first half: {corr_first_b:.3f}, second half: {corr_second_b:.3f}")
print()

# ==========================================
# Separator temperature analysis
# ==========================================

outliers_temp, lb_temp, ub_temp = get_outliers_iqr(df, 'separator_temp_C')
corr_full_t, corr_first_t, corr_second_t = get_time_correlations(df, 'separator_temp_C', split_at=125)
df['temp_rolling'] = get_rolling_average(df['separator_temp_C'])

print("=== Separator Temperature ===")
print(f"Outliers found: {len(outliers_temp)}")
print(outliers_temp[['time_min', 'separator_temp_C']].to_string(index=False))
print()

# ==========================================
# Pressure analysis
# ==========================================

outliers_pres, lb_pres, ub_pres = get_outliers_iqr(df, 'pressure_bar')
corr_full_p, corr_first_p, corr_second_p = get_time_correlations(df, 'pressure_bar', split_at=125)

# Note: pressure_bar has 2 missing values (see missing value report above).
# We do not fill/interpolate them here because the goal of this analysis
# is anomaly detection, not data completion. Filling them could mask or
# fabricate a trend that isn't really in the sensor data. The rolling
# average below will naturally show a short NaN gap at those points,
# which is flagged directly in the chart instead of being hidden.
df['pres_rolling'] = get_rolling_average(df['pressure_bar'])

print("=== Separator Pressure ===")
print(f"Outliers found: {len(outliers_pres)}")
print()

# ==========================================
# Visualization
# ==========================================

fig, axes = plt.subplots(3, 1, figsize=(11, 10))

# --- Temperature ---
axes[0].plot(df['time_min'], df['separator_temp_C'], color='steelblue', alpha=0.6, label='separator_temp_C')
axes[0].plot(df['time_min'], df['temp_rolling'], color='darkred', linewidth=2, label='Rolling Average (window=10)')
axes[0].annotate('Spike (row 95)', xy=(95, 112), xytext=(128, 108),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[0].annotate('Drop (row 74)', xy=(74, 85.38), xytext=(40, 95),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[0].annotate('Spike (row 179)', xy=(179, 90.72), xytext=(160, 100),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[0].annotate('Spike (row 209)', xy=(209, 91.85), xytext=(225, 100),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[0].set_title('Separator Temperature over Time')
axes[0].set_xlabel('Time (min)')
axes[0].set_ylabel('Temperature (C)')
axes[0].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

# --- Pressure ---
axes[1].plot(df['time_min'], df['pressure_bar'], color='orange', label='pressure_bar')
axes[1].plot(df['time_min'], df['pres_rolling'], color='darkred', linewidth=2, label='Rolling Average (window=10)')
axes[1].annotate('Spike (row 61)', xy=(61, 7.93), xytext=(65, 8.4),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[1].annotate('Spike (row 101)', xy=(101, 7.921), xytext=(115, 8.4),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[1].axvspan(xmin=38, xmax=42, color='gray', alpha=0.4, label='Missing Data (row 40)')
axes[1].axvspan(xmin=199, xmax=203, color='gray', alpha=0.4, label='Missing Data (row 201)')
axes[1].set_title('Separator Pressure over Time')
axes[1].set_xlabel('Time (min)')
axes[1].set_ylabel('Pressure (bar)')
axes[1].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

# --- Mass balance ---
axes[2].plot(df['time_min'], df['mass_balance_error'], color='seagreen', label='Mass Balance Error')
axes[2].plot(df['time_min'], df['rolling_balance'], color='darkred', linewidth=2, label='Rolling Average (window=10)')
axes[2].annotate('Drop (row 12)', xy=(12, -3.75), xytext=(35, -3.5),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[2].annotate('Spike (row 228)', xy=(228, 5.86), xytext=(205, 6.8),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[2].annotate('Spike (row 241)', xy=(241, 5.57), xytext=(255, 6.2),
                  arrowprops=dict(facecolor='black', arrowstyle='->'))
axes[2].axvline(x=166, color='orange', linestyle='--', alpha=0.7, label='Drift Start (166)')
axes[2].axvline(x=250, color='orange', linestyle='--', alpha=0.7, label='Drift End (250)')
axes[2].set_title('Mass Balance Error over Time')
axes[2].set_xlabel('Time (min)')
axes[2].set_ylabel('Mass Balance Error (L/min)')
axes[2].legend(bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0)

plt.tight_layout(pad=3.0)
plt.savefig('../images/chart_of_final_project.png', dpi=300, bbox_inches='tight')
plt.show()
