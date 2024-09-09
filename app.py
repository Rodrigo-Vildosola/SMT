# app.py

import streamlit as st
import numpy as np
import sympy as sp
import pandas as pd
import plotly.graph_objects as go
from equations import parse_equation
from solvers import real_solution, dynamic_ode_function
from methods import euler_method, rk2_method, rk4_method
from utils import percent_error, compare_methods, create_pdf_report

st.set_page_config(layout="wide", page_title="Numerical ODE Solver", page_icon="🔢")

# Sidebar Title
st.sidebar.title("🔧 Numerical ODE Solver")

@st.cache_data
def get_real_solution(t0, tf, x0, equation_str):
    ode_func = dynamic_ode_function(equation_str)
    return real_solution(t0, tf, x0, ode_func)

@st.cache_data
def plot_solution_and_errors(_equation_str, x0, t0, tf, method, step_sizes):
    # Parse the equation string to obtain the callable function
    ode_func = dynamic_ode_function(_equation_str)
    
    # Get real solution using the parsed equation
    real_sol = get_real_solution(t0, tf, x0, _equation_str)
    t_fine = np.linspace(t0, tf, 1000)
    x_real = real_sol.sol(t_fine)[0]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=t_fine, y=x_real, mode='lines', name='Real Solution', line=dict(color='gray', width=2, dash='dash')))
    
    error_stats = []
    for h in step_sizes:
        t_values = np.linspace(t0, tf, int((tf - t0) / h) + 1)
        
        # Apply selected method
        if method == 'Euler':
            x_values = euler_method(ode_func, t_values, x0, h)
        elif method == 'Runge-Kutta 2nd Order':
            x_values = rk2_method(ode_func, t_values, x0, h)
        elif method == 'Runge-Kutta 4th Order':
            x_values = rk4_method(ode_func, t_values, x0, h)
        
        # Add to plot
        fig.add_trace(go.Scatter(x=t_values, y=x_values, mode='lines+markers', name=f'{method} (h={h})'))
        
        # Calculate error statistics
        x_real_at_steps = real_sol.sol(t_values)[0]
        errors = percent_error(x_real_at_steps, x_values)
        mean_error = np.mean(errors)
        max_error = np.max(errors)
        if pd.notna(mean_error) and pd.notna(max_error):
            error_stats.append((h, mean_error, max_error))
    
    fig.update_layout(title=f'Solution of ODE ({_equation_str}) with {method}', xaxis_title='Time t', yaxis_title='Solution x(t)')
    error_df = pd.DataFrame(error_stats, columns=["Step Size", "Mean Error (%)", "Max Error (%)"])
    
    return fig, error_df

def main():
    st.title("🔢 Numerical ODE Solver")
    
    # Take ODE input as string from user
    equation_str = st.text_input("Enter the ODE function in terms of y and t:", "np.sin(t) - y**2")
    
    # Parse the equation to get a sympy expression and the numpy equivalent
    equation_sympy = parse_equation(equation_str)
    
    # Display parsed equation as LaTeX
    st.latex(r"f(t, y) = " + sp.latex(equation_sympy))
    
    # Sidebar inputs for initial condition and time range
    x0 = st.sidebar.slider("Initial Condition (y(0)):", -10.0, 10.0, 1.0)
    t0 = st.sidebar.slider("Initial Time (t0):", 0.0, 5.0, 0.0)
    tf = st.sidebar.slider("Final Time (tf):", 0.1, 5.0, 1.0)
    
    # Method and step size selection
    methods = st.sidebar.multiselect("Numerical Methods:", ["Euler", "Runge-Kutta 2nd Order", "Runge-Kutta 4th Order"], ["Euler"])
    step_sizes = st.sidebar.multiselect("Step Sizes (h):", [0.1, 0.05, 0.01, 0.005], [0.1, 0.05, 0.01])
    
    error_stats_dict = {}
    method_plots = {}

    if methods and step_sizes:
        for method in methods:
            fig, error_df = plot_solution_and_errors(equation_str, x0, t0, tf, method, step_sizes)
            st.plotly_chart(fig)
            
            # Collect error stats for comparison and plots for the report
            error_stats_dict[method] = [(row['Step Size'], row['Mean Error (%)'], row['Max Error (%)']) for _, row in error_df.iterrows()]
            method_plots[method] = fig
        
        # Compare methods if there are valid error stats
        compare_methods(error_stats_dict)

        # Generate PDF Report Button
        if st.button("Download Report"):
            pdf_report = create_pdf_report(equation_str, error_stats_dict, method_plots)
            st.download_button(
                label="Download PDF Report",
                data=pdf_report,
                file_name="numerical_ode_report.pdf",
                mime="application/pdf"
            )
if __name__ == "__main__":
    main()
