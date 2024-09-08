import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, Text, fixed
import ipywidgets as widgets
from scipy.integrate import solve_ivp

# Helper function: Convert string equation to ODE function
def dynamic_ode_function(equation_str):
    """
    Creates a Python function from an equation string.
    Example input: "y**2 / 2"
    Output: A function f(t, y) that returns the evaluated equation.
    """
    def f(t, y):
        return eval(equation_str, {"t": t, "y": y, "np": np})
    return f

# Helper function: Compute the real solution using SciPy's solve_ivp
def real_solution(t0, tf, x0, ode_func):
    sol = solve_ivp(ode_func, [t0, tf], [x0], dense_output=True, method='RK45')
    return sol

# Helper function: Calculate percent error
def percent_error(real_values, numerical_values):
    error = np.abs((real_values - numerical_values) / np.abs(real_values)) * 100
    error[np.isinf(error)] = 0  # Handle division by zero
    error[np.isnan(error)] = 0  # Handle NaN values
    return error

# Helper function: Generate a list of colors based on the number of step sizes
def generate_colors(num_steps):
    cmap = plt.get_cmap('tab10')  # Use matplotlib's colormap for distinct colors
    return [cmap(i) for i in range(num_steps)]

# Euler's method for solving ODE
def euler_method(f, t_values, x0, h):
    N = len(t_values)
    x_euler = np.zeros(N)
    x_euler[0] = x0
    for n in range(N - 1):
        x_euler[n+1] = x_euler[n] + h * f(t_values[n], x_euler[n])
    return x_euler

# Runge-Kutta 2nd order method
def rk2_method(f, t_values, x0, h):
    N = len(t_values)
    x_rk2 = np.zeros(N)
    x_rk2[0] = x0
    for n in range(N - 1):
        k1 = h * f(t_values[n], x_rk2[n])
        k2 = h * f(t_values[n] + h/2, x_rk2[n] + k1/2)
        x_rk2[n+1] = x_rk2[n] + k2
    return x_rk2

# Main function to plot different step sizes on the same plot and calculate errors
def plot_solution_and_errors(equation_str, x0, t0, tf, method, step_sizes):
    colors = generate_colors(len(step_sizes))  # Dynamically generate colors based on step sizes
    
    # Convert the string equation into an ODE function
    ode_func = dynamic_ode_function(equation_str)
    
    # Get real solution
    real_sol = real_solution(t0, tf, x0, ode_func)
    t_fine = np.linspace(t0, tf, 1000)  # Use fine time grid for real solution
    x_real = real_sol.sol(t_fine)[0]  # Get the real solution
    
    plt.figure(figsize=(10, 6))
    
    # Plot the real (approximated) solution
    plt.plot(t_fine, x_real, label='Real Solution (approx)', color='k', linestyle='--', linewidth=2)
    
    error_stats = []  # To store statistics for each step size
    
    for h, color in zip(step_sizes, colors):
        t_values = np.linspace(t0, tf, int((tf - t0) / h) + 1)  # Ensure exact range for t_values
        
        # Solve using the selected method
        if method == 'Euler':
            x_values = euler_method(ode_func, t_values, x0, h)
        else:
            x_values = rk2_method(ode_func, t_values, x0, h)
        
        # Plot lines and points
        plt.plot(t_values, x_values, label=f'{method} (h={h})', color=color)
        plt.scatter(t_values, x_values, color=color)
        
        # Compute the real solution at the time points of the numerical method
        x_real_at_steps = real_sol.sol(t_values)[0]
        
        # Calculate percent error
        errors = percent_error(x_real_at_steps, x_values)
        mean_error = np.mean(errors)
        max_error = np.max(errors)
        
        # Append error statistics
        error_stats.append((h, mean_error, max_error))
    
    plt.xlabel('Time t')
    plt.ylabel('Solution x(t)')
    plt.title(f'Solution of ODE ({equation_str}) with {method} method\nInitial condition x0 = {x0}')
    plt.legend()
    plt.grid(True)
    plt.show()

    # Print error statistics
    print(f"\nPercent Error Statistics for {method} method:")
    print(f"{'Step Size':<10} {'Mean Error (%)':<15} {'Max Error (%)':<15}")
    for h, mean_err, max_err in error_stats:
        print(f"{h:<10} {mean_err:<15.2f} {max_err:<15.2f}")

# Step sizes array is now external and configurable
step_sizes = [0.1, 0.05, 0.01, 0.005]  # Define the step sizes array globally

# Define widgets for input
equation_input = Text(value='y**2 / 2', description='ODE:')
x0_slider = FloatSlider(min=-10, max=10, step=0.1, value=1.0, description='x0')
t0_slider = FloatSlider(min=0.0, max=5.0, step=0.1, value=0.0, description='t0')
tf_slider = FloatSlider(min=0.1, max=5.0, step=0.1, value=1.0, description='tf')
method_dropdown = widgets.Dropdown(
    options=['Euler', 'Runge-Kutta 2nd Order'],
    value='Euler',
    description='Method'
)

# Use interact to dynamically update the plot with multiple step sizes and input equation
interact(plot_solution_and_errors, 
         equation_str=equation_input, 
         x0=x0_slider, 
         t0=t0_slider, 
         tf=tf_slider, 
         method=method_dropdown,
         step_sizes=fixed(step_sizes))
