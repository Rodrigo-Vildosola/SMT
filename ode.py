import numpy as np
import pandas as pd
from scipy.integrate import solve_ivp

# Convert string equation to ODE function
def dynamic_ode_function(equation_str):
    """
    Creates a Python function from an equation string.
    Example input: "y**2 / 2"
    Output: A function f(t, y) that returns the evaluated equation.
    """
    def f(t, y):
        return eval(equation_str, {"t": t, "y": y, "np": np})
    return f

def real_solution(t0, tf, x0, ode_func):
    sol = solve_ivp(ode_func, [t0, tf], [x0], dense_output=True, method='RK45')
    return sol

def percent_error(real_values, numerical_values):
    error = np.abs((real_values - numerical_values) / np.abs(real_values)) * 100
    error[np.isinf(error)] = 0
    error[np.isnan(error)] = 0 
    return error

# Euler's method
def euler_method(f, t_values, x0, h):
    N = len(t_values)
    x_euler = np.zeros(N)
    x_euler[0] = x0
    for n in range(N - 1):
        x_euler[n+1] = x_euler[n] + h * f(t_values[n], x_euler[n])
    return x_euler

# Runge-Kutta 2nd Order (RK2) method
def rk2_method(f, t_values, x0, h):
    N = len(t_values)
    x_rk2 = np.zeros(N)
    x_rk2[0] = x0
    for n in range(N - 1):
        k1 = h * f(t_values[n], x_rk2[n])
        k2 = h * f(t_values[n] + h/2, x_rk2[n] + k1/2)
        x_rk2[n+1] = x_rk2[n] + k2
    return x_rk2

# Midpoint Method
def midpoint_method(f, t_values, x0, h):
    N = len(t_values)
    x_midpoint = np.zeros(N)
    x_midpoint[0] = x0
    for n in range(N - 1):
        k1 = f(t_values[n], x_midpoint[n])
        x_midpoint[n+1] = x_midpoint[n] + h * f(t_values[n] + h/2, x_midpoint[n] + h/2 * k1)
    return x_midpoint

# Runge-Kutta 4th Order (RK4) method
def rk4_method(f, t_values, x0, h):
    N = len(t_values)
    x_rk4 = np.zeros(N)
    x_rk4[0] = x0
    for n in range(N - 1):
        k1 = h * f(t_values[n], x_rk4[n])
        k2 = h * f(t_values[n] + h/2, x_rk4[n] + k1/2)
        k3 = h * f(t_values[n] + h/2, x_rk4[n] + k2/2)
        k4 = h * f(t_values[n] + h, x_rk4[n] + k3)
        x_rk4[n+1] = x_rk4[n] + (k1 + 2*k2 + 2*k3 + k4) / 6
    return x_rk4
