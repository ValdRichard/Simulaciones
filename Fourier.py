import numpy as np
import matplotlib.pyplot as plt

L = 1  # Valor arbitrario

x = np.linspace(-L, L, 1000)

# tu función definida a trozos
f = np.where(x < 0, 0, x)

plt.plot(x, f)
plt.xlabel('x')
plt.ylabel('f(x)')
plt.title('f(x)')
plt.grid(True)
plt.show()

x = np.linspace(-3*L, 3*L, 3000)

# periodicidad manual: llevás x al intervalo [-L, L]
x_mod = ((x + L) % (2*L)) - L
f = np.where(x_mod < 0, 0, x_mod)

plt.plot(x, f)
plt.grid(True)
plt.show()

N = 20
S = np.full_like(x, L/4)  # término a0/2

for n in range(1, N+1):
    an = L/(n**2 * np.pi**2) * ((-1)**n - 1)
    bn = (-1)**(n+1) * L / (n * np.pi)
    S += an * np.cos(n * np.pi * x / L) + bn * np.sin(n * np.pi * x / L)

plt.plot(x, f, label='f(x)', linewidth=2)
plt.plot(x, S, label=f'Serie N={N}', linestyle='--')
plt.legend()
plt.grid(True)
plt.show()