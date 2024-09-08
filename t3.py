import numpy as np
import matplotlib.pyplot as plt

# Definimos la ecuación diferencial
def f(t, x):
    return 1 - (x**2)/50 - 1/x + 2 * np.sin(t)

# Parámetros iniciales
t0 = 0  # Tiempo inicial
x0 = 1  # Condición inicial para x
tf = 10  # Tiempo final
h = 0.01  # Tamaño del paso
N = int((tf - t0) / h)  # Número de pasos

t_values = np.linspace(t0, tf, N+1)
x_euler = np.zeros(N+1)
x_rk2 = np.zeros(N+1)

x_euler[0] = x0
x_rk2[0] = x0

for n in range(N):
    x_euler[n+1] = x_euler[n] + h * f(t_values[n], x_euler[n])

# Método de Runge-Kutta de segundo orden
for n in range(N):
    k1 = h * f(t_values[n], x_rk2[n])
    k2 = h * f(t_values[n] + h/2, x_rk2[n] + k1/2)
    x_rk2[n+1] = x_rk2[n] + k2

plt.figure(figsize=(10, 6))
plt.plot(t_values, x_euler, label='Método de Euler')
plt.plot(t_values, x_rk2, label='Método de Runge-Kutta 2º orden')
plt.xlabel('Tiempo t')
plt.ylabel('Solución x(t)')
plt.title('Solución de la EDO usando métodos numéricos')
plt.legend()
plt.grid(True)
plt.show()
