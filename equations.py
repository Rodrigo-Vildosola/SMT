import sympy as sp
import numpy as np

# Mapping common math functions to SymPy equivalents
sympy_functions = {
    'sin': sp.sin,
    'cos': sp.cos,
    'tan': sp.tan,
    'exp': sp.exp,
    'log': sp.log,
    'sqrt': sp.sqrt
}

def parse_equation(equation_str):
    """
    Parse the input ODE string and convert it to a SymPy expression and numpy lambda function.
    """
    for np_func, sympy_func in sympy_functions.items():
        equation_str = equation_str.replace(f'{np_func}', np_func)
    
    sympy_eq = sp.sympify(equation_str, locals=sympy_functions)
    np_eq = sp.lambdify(['t', 'y'], sympy_eq, 'numpy')

    print(np_eq)
    
    return sympy_eq, np_eq

def dynamic_ode_function(equation_str):
    """
    Convert the ODE string into a callable function for numerical methods.
    """
    return lambda t, y: eval(equation_str, {"t": t, "y": y, "np": np})
