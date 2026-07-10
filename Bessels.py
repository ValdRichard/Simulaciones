import numpy as np
import matplotlib.pyplot as plt
from scipy.special import jv, yv, iv, kv

# ============================================================
# CONFIGURACIÓN
# ============================================================

# Órdenes nu que querés graficar
# nus = [1/2, 3/2, 5/2, 7/2, 9/2]
nus = [1, 2, 3, 4, ]

# Dominio de x
x_min = 2   # evitar x=0 porque Y_nu y K_nu divergen ahí
x_max = 20
N = 2000

x = np.linspace(x_min, x_max, N)

# Elegí el tipo:
# "J" para Bessel primera especie J_nu
# "Y" para Bessel segunda especie Y_nu
# "I" para Bessel modificada primera especie I_nu
# "K" para Bessel modificada segunda especie K_nu
tipo = "K"

# ============================================================
# FUNCIÓN PARA ELEGIR BESSEL
# ============================================================

def bessel(tipo, nu, x):
    if tipo == "J":
        return jv(nu, x)
    elif tipo == "Y":
        return yv(nu, x)
    elif tipo == "I":
        return iv(nu, x)
    elif tipo == "K":
        return kv(nu, x)
    else:
        raise ValueError("tipo debe ser 'J', 'Y', 'I' o 'K'")

# ============================================================
# GRÁFICO
# ============================================================

plt.figure(figsize=(9, 5))

for nu in nus:
    y = bessel(tipo, nu, x)
    plt.plot(x, y, label=fr"${tipo}_{{{nu}}}(x)$")

plt.axhline(0, linewidth=0.8)
plt.xlabel(r"$x$")
plt.ylabel(fr"${tipo}_\nu(x)$")
plt.title(fr"Funciones de Bessel tipo ${tipo}_\nu(x)$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()