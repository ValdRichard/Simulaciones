import numpy as np
import matplotlib.pyplot as plt

# Parámetros
N = 5
z = 0

# Grilla
x = np.linspace(0, 1, 1000)
y = np.linspace(0, 1, 1000)
X, Y = np.meshgrid(x, y)

# Inicializar
F = np.zeros_like(X)

# Suma doble
for n in range(N):
    for m in range(N):
        gamma_nm = np.sqrt(((2*n+1)*np.pi)**2 + ((2*m+1)*np.pi)**2)
        coef = 1 / (np.pi**2 * (2*n+1)*(2*m+1))
        
        term = coef * np.sin((2*n+1)*np.pi*X) * np.sin((2*m+1)*np.pi*Y) * np.exp(-gamma_nm * z)
        
        F += term

# Plot 2D
plt.figure()
plt.contourf(X, Y, F)
plt.colorbar()
plt.title(f"f(x,y,z={z})")
plt.xlabel("x")
plt.ylabel("y")
plt.show()

# Plot 3D
fig = plt.figure()
ax = fig.add_subplot(projection='3d')
ax.plot_surface(X, Y, F)
plt.show()
