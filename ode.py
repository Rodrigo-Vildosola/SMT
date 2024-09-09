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

def euler_method(f, t_values, x0, h):
    N = len(t_values)
    x_euler = np.zeros(N)
    x_euler[0] = x0
    for n in range(N - 1):
        x_euler[n+1] = x_euler[n] + h * f(t_values[n], x_euler[n])
    return x_euler

def rk2_method(f, t_values, x0, h):
    N = len(t_values)
    x_rk2 = np.zeros(N)
    x_rk2[0] = x0
    for n in range(N - 1):
        k1 = h * f(t_values[n], x_rk2[n])
        k2 = h * f(t_values[n] + h/2, x_rk2[n] + k1/2)
        x_rk2[n+1] = x_rk2[n] + k2
    return x_rk2
