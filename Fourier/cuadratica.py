import numpy as np
import matplotlib.pyplot as plt

L = 1
x = np.linspace(-L, L, 1000)

f = np.where(x < 0, 0, x)

N = 10
S = np.full_like(x, L*(1/3))  # a0/2

for n in range(1, N+1):
    an = 4*(-1)**n / (n * np.pi)**2
    # bn = (-1)**(n+1) * L / (n * np.pi)
    bn = 0
    S += an * np.cos(n * np.pi * x / L) + bn * np.sin(n * np.pi * x / L)

plt.plot(x, x**2, label='f(x)', linewidth=1)
plt.plot(x, S, label=f'Serie de Fourier N={N}', linestyle='--')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Serie de Fourier')
plt.legend()
plt.grid(True)
plt.show()