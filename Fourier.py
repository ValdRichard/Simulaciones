import numpy as np
import matplotlib.pyplot as plt

L = 1
x = np.linspace(-L, L, 1000)

f = np.where(x < 0, 0, x)

N = 20
S = np.full_like(x, L/4)  # a0/2

for n in range(1, N+1):
    an = L/(n**2 * np.pi**2) * ((-1)**n - 1)
    bn = (-1)**(n+1) * L / (n * np.pi)
    S += an * np.cos(n * np.pi * x / L) + bn * np.sin(n * np.pi * x / L)

plt.plot(x, f, label='f(x)', linewidth=2)
plt.plot(x, S, label=f'Serie de Fourier N={N}', linestyle='--')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Serie de Fourier')
plt.legend()
plt.grid(True)
plt.show()