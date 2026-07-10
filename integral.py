import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import quad

# =========================================
# Parámetros
# =========================================
a = 1.0
v = 1.0

# Dominio en x
x_vals = np.linspace(0, 7*a, 300)

# Tiempos en segundos
t_vals = [0.0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0]

# Corte superior de la integral en k
KMAX = 1200.0
LIMIT = 4000


# =========================================
# Integrando
# =========================================
def integrand(k, x, t, a, v):
    if k == 0:
        return 0.0

    return (
        (2.0 / (np.pi * k))
        * (np.cos(k*a) - np.cos(3.0*k*a))
        * np.sin(k*x)
        * np.cos(v*k*t)
    )


# =========================================
# Solución integral
# =========================================
def u_integral(x, t, a, v, kmax=KMAX):
    val, err = quad(
        integrand,
        0.0,
        kmax,
        args=(x, t, a, v),
        limit=LIMIT
    )
    return val


# =========================================
# Graficar en distintas figuras
# =========================================
for t in t_vals:
    u_vals = np.array([u_integral(x, t, a, v) for x in x_vals])

    plt.figure(figsize=(10, 5))

    plt.plot(x_vals, u_vals, label=f"t = {t:.2f} s")

    plt.axhline(0, color="black", linewidth=0.8)
    plt.axvline(0, color="black", linewidth=0.8)

    plt.xlabel("x")
    plt.ylabel("u(x,t)")
    plt.title(f"Solución numérica de la integral para t = {t:.2f} s")

    plt.ylim(-0.7, 0.7)
    plt.xlim(0, 7*a)

    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()