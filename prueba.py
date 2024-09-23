import numpy as np
import matplotlib.pyplot as plt

# Definir la función
def f(x):
    return np.piecewise(
        x,
        [x < 1, (1 < x) & (x < 2), (2 < x) & (x < 3), x > 3],
        [lambda x: x,            # Para x < 1
         lambda x: 1,            # Para 1 < x < 2
         lambda x: x - 2,        # Para 2 < x < 3
         lambda x: 2])          # Para x > 3 (valor constante 2 después de x = 3)

# Definir los rangos de x
x1 = np.linspace(0, 1, 500)
x2 = np.linspace(1 + 1e-4, 2, 500)
x3 = np.linspace(2 + 1e-4, 3, 500)
x4 = np.linspace(3 + 1e-4, 5, 500)

# Calcular y unir las partes
y1 = f(x1)
y2 = f(x2)
y3 = f(x3)
y4 = f(x4)

# Crear la figura y el eje
fig, ax = plt.subplots(figsize=(8, 6))

# Graficar las partes de la función
ax.plot(x1, y1, label='f(x) en [0, 1)', color='blue')
ax.plot(x2, y2, label='f(x) en (1, 2)', color='blue')
ax.plot(x3, y3, label='f(x) en (2, 3)', color='blue')
ax.plot(x4, y4, label='f(x) en (3, 5]', color='blue')

# Indicar las discontinuidades
ax.axvline(x=1, color='red', linestyle='--', label='Discontinuidad removible en x=1')
ax.axvline(x=2, color='green', linestyle='--', label='Discontinuidad de salto en x=2')
ax.axvline(x=3, color='purple', linestyle='--', label='Discontinuidad infinita en x=3')

# Ajustar el rango de los ejes
ax.set_xlim([0, 5])
ax.set_ylim([-5, 5])

# Etiquetas y leyenda
ax.set_title('Gráfica de la función con discontinuidades')
ax.set_xlabel('x')
ax.set_ylabel('f(x)')
ax.legend()

# Mostrar el gráfico
plt.show()