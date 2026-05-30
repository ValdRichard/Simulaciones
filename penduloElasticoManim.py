from manim import *
import numpy as np

# ── Parámetros físicos ──────────────────────────────────────────────
g = 9.81
k = 50
m = 5
l = 3
tiempo_total = 10
dt = 0.01
pasos = int(tiempo_total / dt)

# ── Condiciones iniciales ───────────────────────────────────────────
theta0  = np.pi / 8
r0      = l
rp0     = 0.0
thetap0 = 0.0

# ── Ecuaciones de movimiento ────────────────────────────────────────
def rpp(r, theta, thetap):
    return r * thetap**2 + g * np.cos(theta) + k/m * (l - r)

def thetapp(r, rp, theta, thetap):
    return -g/r * np.sin(theta) - 2 * rp * thetap / r

# ── Integración de Euler ────────────────────────────────────────────
posiciones = []

for i in range(pasos):
    rp     = rp0     + rpp(r0, theta0, thetap0)     * dt
    thetap = thetap0 + thetapp(r0, rp0, theta0, thetap0) * dt
    r      = r0      + rp     * dt
    theta  = theta0  + thetap * dt

    x = r * np.sin(theta)
    y = -r * np.cos(theta)

    posiciones.append((x, y))

    r0      = r
    rp0     = rp
    theta0  = theta
    thetap0 = thetap

# ── Animación ───────────────────────────────────────────────────────
class SpringSimulation(MovingCameraScene):
    def construct(self):
        self.camera.background_color = WHITE
        # self.camera.frame_width = 6   # por defecto es 14
        # self.camera.frame_height = 4  # por defecto es 8
        # self.camera.frame.move_to(UP * 2)  # esto sí funciona      
          # Techo
        wall = Rectangle(width=2, height=0.3).set_fill(GRAY, 1).to_edge(UP)
        pivot = wall.get_center() + DOWN * 0.15
        self.add(wall)

        # Posición inicial — relativa al pivote
        x0, y0 = posiciones[0]

        # Masa
        box = Square(side_length=0.5).set_fill(ORANGE, 1)
        box.move_to(pivot + np.array([x0, y0, 0]))

        trace = TracedPath(
            box.get_center,
            stroke_color=BLUE,
            stroke_width=2
        )

        # Resorte
        spring = always_redraw(lambda: Line(
            pivot,
            box.get_center(),
            color=BLACK
        ))

        self.add(spring, trace, box)

        # Updater
        t = ValueTracker(0)

        def update_box(mob):
            i = int(t.get_value() / dt)
            i = min(i, len(posiciones) - 1)
            x, y = posiciones[i]
            mob.move_to(pivot + np.array([x, y, 0]))

        box.add_updater(update_box)

        # Animación
        self.play(
            t.animate.set_value(pasos * dt),
            run_time=pasos * dt,
            rate_func=linear
        )