from scipy.integrate import solve_ivp
import numpy as np

def real_solution(t0, tf, x0, ode_func):
    """
    Solve the ODE using an accurate solver (e.g., RK45) and return the solution.
    """
    sol = solve_ivp(ode_func, [t0, tf], [x0], dense_output=True, method='RK45')
    return sol

def dynamic_ode_function(equation_str):
    """
    Convert an ODE string into a callable Python function for numerical methods.
    """
    return lambda t, y: eval(equation_str, {"t": t, "y": y, "np": np})
