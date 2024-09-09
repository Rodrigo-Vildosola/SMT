# utils.py

import numpy as np
import pandas as pd
import streamlit as st
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image


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


def create_pdf_report(equation_str, error_stats_dict, method_plots):
    """Generate a PDF report using ReportLab."""
    
    # Create a BytesIO object to store the PDF
    pdf_output = BytesIO()
    
    # Create a SimpleDocTemplate for the PDF
    doc = SimpleDocTemplate(pdf_output, pagesize=letter)
    
    # Elements list to hold all content for the PDF
    elements = []
    
    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']
    
    # Title
    title = Paragraph("Numerical ODE Solver Report", title_style)
    elements.append(title)
    elements.append(Spacer(1, 12))  # Add a spacer
    
    # ODE Equation
    ode_paragraph = Paragraph(f"<strong>ODE Equation:</strong> {equation_str}", normal_style)
    elements.append(ode_paragraph)
    elements.append(Spacer(1, 12))  # Add a spacer
    
    # Iterate over methods and add plots and error tables
    for method, fig in method_plots.items():
        # Add method title
        method_title = Paragraph(f"<strong>{method} Method</strong>", normal_style)
        elements.append(method_title)
        elements.append(Spacer(1, 12))  # Add a spacer
        
        # Save Plot as PNG and insert it into the PDF
        img_buffer = BytesIO()
        fig.write_image(img_buffer, format="png")
        img_buffer.seek(0)
        
        # Add image to the report
        img = Image(img_buffer, 6 * inch, 4 * inch)  # Adjust image size
        elements.append(img)
        elements.append(Spacer(1, 24))  # Add space after the image
        
        # Error Table for the method
        error_table_data = [["Step Size", "Mean Error (%)", "Max Error (%)"]]  # Table Header
        for row in error_stats_dict[method]:
            error_table_data.append([str(row[0]), f"{row[1]:.2f}", f"{row[2]:.2f}"])
        
        # Create table with styling
        error_table = Table(error_table_data)
        error_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Gridlines
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Body background color
        ]))
        
        elements.append(error_table)
        elements.append(Spacer(1, 24))  # Add a spacer after the table
    
    # Build the PDF
    doc.build(elements)
    
    # Move cursor to start of the BytesIO object
    pdf_output.seek(0)
    
    return pdf_output
