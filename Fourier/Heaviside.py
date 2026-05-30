import numpy as np
import matplotlib.pyplot as plt

L = 1
a = 0.3          # parámetro del pulso, debe estar en (0, L)
N = 1000000           # número de términos

x = np.linspace(-L, L, 1000)

# g(x) exacta usando Heaviside
g = np.where(np.abs(x) < a, 1/(2*a), 0)

# Serie de Fourier
S = np.full_like(x, 1/(2*L))   # a0/2 = 1/(2L)

for n in range(1, N+1):
    an = np.sin(n * np.pi * a / L) / (n * np.pi * a)  
    # bn = 0 porque g(x) es par
    S += an * np.cos(n * np.pi * x / L)

plt.plot(x, g, label='g(x) exacta', linewidth=2, color='gray', linestyle='--')
plt.plot(x, S, label=f'Serie de Fourier N={N}', linewidth=2, color='steelblue')
plt.xlabel('x')
plt.ylabel('y')
plt.title(f'Serie de Fourier — Pulso rectangular (a={a}, N={N})')
plt.legend()
plt.grid(True)
plt.show()