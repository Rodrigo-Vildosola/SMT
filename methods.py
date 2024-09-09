import numpy as np

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
