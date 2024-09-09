import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from ode import dynamic_ode_function, real_solution, percent_error, euler_method, rk2_method

# Set the page layout to wide
st.set_page_config(layout="wide")

# Cache the real solution calculation to optimize performance
@st.cache_data
def get_real_solution(t0, tf, x0, equation_str):
    ode_func = dynamic_ode_function(equation_str)
    return real_solution(t0, tf, x0, ode_func)

# Cache the function to generate error statistics and plot
@st.cache_data
def plot_solution_and_errors(equation_str, x0, t0, tf, method, step_sizes):
    ode_func = dynamic_ode_function(equation_str)

    # Get real solution
    real_sol = get_real_solution(t0, tf, x0, equation_str)
    t_fine = np.linspace(t0, tf, 1000)  # Use fine time grid for real solution
    x_real = real_sol.sol(t_fine)[0]  # Get the real solution
    
    # Create a Plotly figure with larger size
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=t_fine, y=x_real, mode='lines', name='Real Solution (approx)', 
                             line=dict(color='black', dash='dash')))

    error_stats = []
    
    for h in step_sizes:
        t_values = np.linspace(t0, tf, int((tf - t0) / h) + 1)
        
        if method == 'Euler':
            x_values = euler_method(ode_func, t_values, x0, h)
        else:
            x_values = rk2_method(ode_func, t_values, x0, h)
        
        fig.add_trace(go.Scatter(x=t_values, y=x_values, mode='lines+markers', name=f'{method} (h={h})'))
        
        x_real_at_steps = real_sol.sol(t_values)[0]
        
        errors = percent_error(x_real_at_steps, x_values)
        mean_error = np.mean(errors)
        max_error = np.max(errors)
        
        error_stats.append((h, mean_error, max_error))
    
    fig.update_layout(title=f'Solution of ODE ({equation_str}) with {method} method',
                      xaxis_title='Time t', yaxis_title='Solution x(t)', legend_title='Step Sizes',
                      height=600, width=1000)

    error_df = pd.DataFrame({
        "Step Size": [h for h, _, _ in error_stats],
        "Mean Error (%)": [round(mean_err, 2) for _, mean_err, _ in error_stats],
        "Max Error (%)": [round(max_err, 2) for _, _, max_err in error_stats]
    })

    return fig, error_df

def main():
    # Main app title and description
    st.title("Numerical ODE Solver with Dynamic Plot")
    st.subheader("This application allows you to solve ordinary differential equations using numerical methods.")
    
    # Define widgets for input in a wide layout
    equation_str = st.text_input("Enter the ODE function in terms of y and t:", "y**2 / 2")
    
    # Sidebar Inputs
    st.sidebar.markdown("### Set the initial condition and time range:")
    x0 = st.sidebar.slider("Initial Condition (y(0)):", -10.0, 10.0, 1.0)
    
    # Place t0 and tf sliders in the same row in the sidebar
    st.sidebar.markdown("### Time Range:")
    t0 = st.sidebar.slider("Initial Time (t0):", 0.0, 5.0, 0.0)
    tf = st.sidebar.slider("Final Time (tf):", 0.1, 5.0, 1.0)

    st.sidebar.markdown("### Choose the numerical method and step sizes:")
    method = st.sidebar.selectbox("Numerical Method:", ["Euler", "Runge-Kutta 2nd Order"])
    step_sizes = st.sidebar.multiselect("Step Sizes (h):", [0.1, 0.05, 0.01, 0.005], [0.1, 0.05, 0.01])

    # Automatically update the plot and table as inputs change
    if step_sizes:
        fig, error_df = plot_solution_and_errors(equation_str, x0, t0, tf, method, step_sizes)

        # Show plot
        st.plotly_chart(fig, use_container_width=True)

        # Show error statistics table
        st.markdown("### Percent Error Statistics")
        st.table(error_df)
    else:
        st.warning("Please select at least one step size to see the results.")

if __name__ == "__main__":
    main()
