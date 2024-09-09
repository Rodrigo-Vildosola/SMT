# utils.py

import numpy as np
import pandas as pd
import streamlit as st

def percent_error(real_values, numerical_values):
    """
    Calculate the percent error between real and numerical values.
    """
    error = np.abs((real_values - numerical_values) / np.abs(real_values)) * 100
    error[np.isinf(error)] = 0  # Handle division by zero cases
    error[np.isnan(error)] = 0  # Handle NaN cases
    return error

def compare_methods(error_stats_dict):
    """
    Compare the mean and max errors across different methods and step sizes.
    """
    comparison_rows = []
    
    for method, stats in error_stats_dict.items():
        for (step_size, mean_error, max_error) in stats:
            if pd.notna(mean_error) and pd.notna(max_error):
                comparison_rows.append({
                    'Method': method,
                    'Step Size': step_size,
                    'Mean Error (%)': round(mean_error, 2),
                    'Max Error (%)': round(max_error, 2)
                })

    if comparison_rows:
        comparison_df = pd.DataFrame(comparison_rows)
    else:
        comparison_df = pd.DataFrame(columns=['Method', 'Step Size', 'Mean Error (%)', 'Max Error (%)'])

    st.markdown("## 🔍 Cross-Method Comparison")
    st.markdown("The following table compares the error statistics across the selected methods:")
    st.table(comparison_df)

    if not comparison_df.empty:
        st.markdown("### 📊 Insights from Comparison:")
        min_mean_error_row = comparison_df.loc[comparison_df['Mean Error (%)'].idxmin()]
        min_max_error_row = comparison_df.loc[comparison_df['Max Error (%)'].idxmin()]

        st.write(f"- The method with the lowest **mean error** is `{min_mean_error_row['Method']}` with a step size of {min_mean_error_row['Step Size']} and a mean error of {min_mean_error_row['Mean Error (%)']}%.")
        st.write(f"- The method with the lowest **max error** is `{min_max_error_row['Method']}` with a step size of {min_max_error_row['Step Size']} and a max error of {min_max_error_row['Max Error (%)']}%.")
