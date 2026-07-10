import numpy as np
import matplotlib.pyplot as plt

from matplotlib import cm
from matplotlib.colors import Normalize
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg


# ============================================================
# COMPATIBILIDAD CON SCIPY NUEVO Y VIEJO
# ============================================================

try:
    from scipy.special import sph_harm_y

    def armonico_esferico(l, m, theta, phi):
        """
        theta: ángulo polar, entre 0 y pi
        phi: ángulo azimutal, entre 0 y 2pi
        """
        return sph_harm_y(l, m, theta, phi)

except ImportError:
    from scipy.special import sph_harm

    def armonico_esferico(l, m, theta, phi):
        """
        En la versión vieja, sph_harm recibe primero
        el ángulo azimutal y luego el polar.
        """
        return sph_harm(m, l, phi, theta)


# ============================================================
# CONFIGURACIÓN
# ============================================================

armonicos = [
    (0, 0),
    (1, -1),
    (1, 0),
    (1, 1),
    (2, -2),
    (2, -1),
    (2, 0),
    (2, 1),
    (2, 2),
]

# Puede ser:
# "real"
# "imag"
# "modulo"
parte = "real"

# Cantidad de columnas de la grilla final
n_columnas = 3

# Resolución de cada armónico.
# Bajá estos valores si todavía tarda demasiado.
n_theta = 70
n_phi = 140

# Ángulo fijo desde el cual se toma la "foto"
elevacion = 25
azimut = 40

# Resolución de cada imagen individual
dpi_imagen = 100


# ============================================================
# MALLA ANGULAR
# ============================================================

theta_1d = np.linspace(0, np.pi, n_theta)
phi_1d = np.linspace(0, 2 * np.pi, n_phi)

theta, phi = np.meshgrid(
    theta_1d,
    phi_1d,
    indexing="ij"
)


# ============================================================
# FUNCIÓN QUE RENDERIZA UN ARMÓNICO COMO UNA FOTO
# ============================================================

def crear_imagen_armonico(l, m):

    # --------------------------------------------------------
    # CALCULAR EL ARMÓNICO
    # --------------------------------------------------------

    Y = armonico_esferico(
        l,
        m,
        theta,
        phi
    )

    if parte == "real":
        valor = np.real(Y)

    elif parte == "imag":
        valor = np.imag(Y)

    elif parte == "modulo":
        valor = np.abs(Y)

    else:
        raise ValueError(
            'parte debe ser "real", "imag" o "modulo".'
        )

    # --------------------------------------------------------
    # RADIO DE LA SUPERFICIE
    # --------------------------------------------------------

    # La distancia radial tiene que ser positiva.
    # El signo se muestra mediante el color.
    radio = np.abs(valor)

    radio_maximo = np.max(radio)

    if radio_maximo > 1e-14:
        radio = radio / radio_maximo

    # --------------------------------------------------------
    # COORDENADAS CARTESIANAS
    # --------------------------------------------------------

    x = radio * np.sin(theta) * np.cos(phi)
    y = radio * np.sin(theta) * np.sin(phi)
    z = radio * np.cos(theta)

    # --------------------------------------------------------
    # COLORES
    # --------------------------------------------------------

    if parte == "modulo":

        valor_maximo = np.max(valor)

        if valor_maximo < 1e-14:
            valor_maximo = 1

        normalizacion = Normalize(
            vmin=0,
            vmax=valor_maximo
        )

        colores = cm.viridis(
            normalizacion(valor)
        )

    else:

        valor_maximo = np.max(
            np.abs(valor)
        )

        if valor_maximo < 1e-14:
            valor_maximo = 1

        normalizacion = Normalize(
            vmin=-valor_maximo,
            vmax=valor_maximo
        )

        colores = cm.coolwarm(
            normalizacion(valor)
        )

    # --------------------------------------------------------
    # CREAR FIGURA 3D FUERA DE LA INTERFAZ
    # --------------------------------------------------------

    figura_3d = Figure(
        figsize=(3.4, 3.4),
        dpi=dpi_imagen
    )

    canvas = FigureCanvasAgg(figura_3d)

    ax = figura_3d.add_subplot(
        111,
        projection="3d"
    )

    ax.plot_surface(
        x,
        y,
        z,
        facecolors=colores,
        rstride=1,
        cstride=1,
        linewidth=0,
        antialiased=True,
        shade=False
    )

    # --------------------------------------------------------
    # EJES CARTESIANOS
    # --------------------------------------------------------

    limite = 1.25

    # Eje x
    ax.quiver(
        -limite, 0, 0,
        2 * limite, 0, 0,
        arrow_length_ratio=0.06,
        linewidth=1
    )

    # Eje y
    ax.quiver(
        0, -limite, 0,
        0, 2 * limite, 0,
        arrow_length_ratio=0.06,
        linewidth=1
    )

    # Eje z
    ax.quiver(
        0, 0, -limite,
        0, 0, 2 * limite,
        arrow_length_ratio=0.06,
        linewidth=1
    )

    # Etiquetas de los ejes
    ax.text(
        limite * 1.08,
        0,
        0,
        r"$x$",
        fontsize=11
    )

    ax.text(
        0,
        limite * 1.08,
        0,
        r"$y$",
        fontsize=11
    )

    ax.text(
        0,
        0,
        limite * 1.08,
        r"$z$",
        fontsize=11
    )

    # Origen
    ax.scatter(
        [0],
        [0],
        [0],
        s=8
    )

    # --------------------------------------------------------
    # LÍMITES Y VISTA FIJA
    # --------------------------------------------------------

    ax.set_xlim(-limite, limite)
    ax.set_ylim(-limite, limite)
    ax.set_zlim(-limite, limite)

    ax.set_box_aspect((1, 1, 1))

    ax.view_init(
        elev=elevacion,
        azim=azimut
    )

    # Sacamos la caja 3D interactiva, pero dejamos
    # los ejes cartesianos dibujados manualmente.
    ax.set_axis_off()

    figura_3d.subplots_adjust(
        left=0,
        right=1,
        bottom=0,
        top=1
    )

    # --------------------------------------------------------
    # CONVERTIR LA FIGURA 3D EN UNA IMAGEN
    # --------------------------------------------------------

    canvas.draw()

    imagen = np.asarray(
        canvas.buffer_rgba()
    ).copy()

    return imagen


# ============================================================
# CREAR TODAS LAS FOTOS
# ============================================================

imagenes = []

for l, m in armonicos:

    imagen = crear_imagen_armonico(
        l,
        m
    )

    imagenes.append(
        (l, m, imagen)
    )


# ============================================================
# MOSTRAR LAS FOTOS EN UNA ÚNICA FIGURA 2D
# ============================================================

cantidad = len(armonicos)

n_filas = int(
    np.ceil(cantidad / n_columnas)
)

figura, ejes = plt.subplots(
    n_filas,
    n_columnas,
    figsize=(
        4 * n_columnas,
        4 * n_filas
    )
)

# Convertir ejes en arreglo plano, incluso si hay un solo gráfico
ejes = np.atleast_1d(
    ejes
).ravel()

for ax, (l, m, imagen) in zip(
    ejes,
    imagenes
):

    ax.imshow(imagen)

    ax.set_title(
        rf"$Y_{{{l},{m}}}$",
        fontsize=14
    )

    # Estos son ejes 2D normales, sin interacción 3D
    ax.axis("off")


# Ocultar lugares vacíos de la grilla
for ax in ejes[cantidad:]:
    ax.axis("off")


figura.suptitle(
    f"Armónicos esféricos — parte {parte}",
    fontsize=18
)

plt.tight_layout(
    rect=[0, 0, 1, 0.96]
)

plt.show()