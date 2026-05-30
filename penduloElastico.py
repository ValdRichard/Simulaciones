import matplotlib.pyplot as plt
import numpy as np
xcal = []
ycal = []
g = 9.81
k = 50
m = 2
l = 1 
tiempo_total = 5
dt = 0.01
pasos = int(tiempo_total / dt)

theta0 = np.pi / 8
r0 = l 
rp0 = 0 
thetap0 = 0
def rpp(r0, thetap0, theta0):
    rpp = r0 * thetap0**2 + g * np.cos(theta0) + k/m * ( l - r0)
    return rpp

def thetapp(r, rp, theta, thetap):
    return -g/r * np.sin(theta) - 2 * rp * thetap / r


for i in range(pasos):
    rp = rp0 + rpp(r0, thetap0, theta0)*dt
    thetap = thetap0 + thetapp(r0, rp0, theta0, thetap0)*dt
    
    r = r0 + rp*dt
    theta = theta0 + thetap*dt
    x0 = r * np.sin(theta)
    y0 = -r * np.cos(theta)

    # x = -y0
    # y = x0

    # x = r * np.sin(theta)
    # y = -r * np.cos(theta)
    xcal.append(x0)
    ycal.append(y0)
    r0 = r
    rp0 = rp
    theta0 = theta
    thetap0 = thetap

# Acá de alguna forma se graficará algo. 
plt.scatter(xcal, ycal, s=5)
plt.scatter(xcal[0], ycal[0], s=80, label='Inicio')
plt.scatter(xcal[-1], ycal[-1], s=80, label='Final')
plt.legend()
plt.xlabel("x")
plt.ylabel("y")
plt.title("Trayectoria del péndulo elástico")
plt.axis("equal")
plt.show()

