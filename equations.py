import sympy as sp
import numpy as np

# Mapping common math functions to SymPy equivalents
sympy_functions = {
    'sin': sp.sin,
    'cos': sp.cos,
    'exp': sp.exp,
    'log': sp.log
}

def parse_equation(equation_str):
    # Replace 'np.' with '' so that sympy can understand the functions
    for np_func, sympy_func in sympy_functions.items():
        equation_str = equation_str.replace(f'np.{np_func}', np_func)
    
    # Parse the equation
    return sp.sympify(equation_str, locals=sympy_functions)

