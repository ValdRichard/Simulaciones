from manim import *
import numpy as np

# ── Parámetros físicos ──────────────────────────────────────────────
g = 9.81
m = 1.0
l = 1.0
tiempo_total = 6
dt = 0.01
pasos = int(tiempo_total / dt)

# ── Condición inicial ───────────────────────────────────────────────
theta0  = np.pi / 3   # 60°, lejos del equilibrio para ver movimiento claro
thetap0 = 0.0

# ── Ecuación de movimiento ──────────────────────────────────────────
def thetapp(theta, thetap):
    num = (m * g * np.cos(theta)) / (2 * l) + (thetap**2 * np.sin(2 * theta)) / 2
    den = np.sin(theta)**2 + 1/3
    return -num / den

# ── Integración de Euler ────────────────────────────────────────────
thetas  = []
thetaps = []

for _ in range(pasos):
    thetap_new = thetap0 + thetapp(theta0, thetap0) * dt
    theta_new  = theta0  + thetap0 * dt

    thetas.append(theta0)
    thetaps.append(thetap0)

    theta0  = theta_new
    thetap0 = thetap_new

# ── Geometría ───────────────────────────────────────────────────────
# Varilla 1: origen → (l cosθ, l sinθ)
# Varilla 2: extremo varilla 1 → pivote en y=0
# φ = π/2 - θ  =>  extremo deslizante en (l cosθ + l sinθ,  0)

def get_A(theta):
    return np.array([0.0, 0.0, 0.0])

def get_B(theta):
    return np.array([l * np.cos(theta), l * np.sin(theta), 0.0])

def get_C(theta):
    return np.array([2*l*np.cos(theta), 0, 0])

# ── Escena ───────────────────────────────────────────────────────────
class DosVarillas(Scene):
    def construct(self):
        self.camera.background_color = WHITE

        # ── Layout: mecanismo izquierda, gráfico derecha ──
        mec_shift = ORIGIN
        # ── Eje y=0 (guía del pivote deslizante) ──
        guia = Line(
            LEFT * config.frame_width/2,
            RIGHT * config.frame_width/2,
            color=GRAY,
            stroke_width=2
        )
        marca_origen = Dot(mec_shift, color=BLACK, radius=0.06)
        self.add(guia, marca_origen)

        # ── Tracker de tiempo ──
        t = ValueTracker(0)

        # ── Varilla 1 ──
        varilla1 = always_redraw(lambda: Line(
            mec_shift + get_A(thetas[min(int(t.get_value() / dt), pasos - 1)]),
            mec_shift + get_B(thetas[min(int(t.get_value() / dt), pasos - 1)]),
            color=BLUE, stroke_width=5
        ))

        # ── Varilla 2 ──
        varilla2 = always_redraw(lambda: Line(
            mec_shift + get_B(thetas[min(int(t.get_value() / dt), pasos - 1)]),
            mec_shift + get_C(thetas[min(int(t.get_value() / dt), pasos - 1)]),
            color=RED, stroke_width=5
        ))

        # ── Pivote en B (articulación entre varillas) ──
        pivote_B = always_redraw(lambda: Dot(
            mec_shift + get_B(thetas[min(int(t.get_value() / dt), pasos - 1)]),
            color=BLACK, radius=0.08
        ))

        # ── Pivote deslizante C ──
        pivote_C = always_redraw(lambda: Dot(
            mec_shift + get_C(thetas[min(int(t.get_value() / dt), pasos - 1)]),
            color=GREEN_D, radius=0.08
        ))

        self.add(varilla1, varilla2, pivote_B, pivote_C)

      

        # ── Animación ──
        self.play(
            t.animate.set_value(pasos * dt),
            run_time=pasos * dt,
            rate_func=linear
        )