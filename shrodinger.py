import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy.sparse
import scipy.sparse.linalg

HBAR = 1.0
MASS = 1.0

K0 = 2.0
SIGMA = 1.5
X0 = -25.0

V0 = 4.0
A_BARR = 1.0
X_BARR = 0.0

X_MIN = -60.0
X_MAX = 60.0
N_X = 1000

T_MAX = 25.0
N_T = 800

x = np.linspace(X_MIN, X_MAX, N_X)
dx = x[1] - x[0]

t_grid = np.linspace(0, T_MAX, N_T)
dt = t_grid[1] - t_grid[0]


def paquet_initial(x):
    facteur = np.power(2 * np.pi * SIGMA**2, -0.25)
    enveloppe = np.exp(-(x - X0)**2 / (4 * SIGMA**2))
    phase = np.exp(1j * K0 * x)
    return facteur * enveloppe * phase


def potentiel_barriere(x):
    V = np.zeros_like(x)
    masque = (x >= X_BARR) & (x <= X_BARR + A_BARR)
    V[masque] = V0
    return V


def norme(psi):
    return scipy.integrate.simpson(np.abs(psi)**2, x=x)


def construire_matrices_CN(V):
    n = len(V)

    coeff = HBAR**2 / (2 * MASS * dx**2)

    diagonale = 2 * coeff + V
    hors_diagonale = -coeff * np.ones(n - 1)

    H = scipy.sparse.diags(
        [hors_diagonale, diagonale, hors_diagonale],
        [-1, 0, 1],
        format="csc"
    )

    I = scipy.sparse.identity(n, format="csc")

    facteur = 1j * dt / (2 * HBAR)

    A = I + facteur * H
    B = I - facteur * H

    return A, B


def resoudre_CN(psi0, V):
    psi = np.empty((N_T, N_X), dtype=complex)
    psi[0] = psi0

    A, B = construire_matrices_CN(V)

    solveur = scipy.sparse.linalg.splu(A)

    normes = np.zeros(N_T)
    normes[0] = norme(psi0)

    for n in range(N_T - 1):
        second_membre = B.dot(psi[n])
        psi[n + 1] = solveur.solve(second_membre)
        normes[n + 1] = norme(psi[n + 1])

    return psi, normes


def afficher_norme(normes):
    plt.figure(figsize=(9, 5))

    plt.plot(
        t_grid,
        normes,
        color="#1d3557",
        linewidth=2.5,
        label="Norme numérique"
    )

    plt.axhline(
        1,
        color="#e63946",
        linestyle="--",
        linewidth=2,
        label="Norme attendue = 1"
    )

    plt.xlabel("Temps t")
    plt.ylabel(r"Norme $\int |\Psi(x,t)|^2 dx$")

    plt.title("Conservation de la norme avec Crank-Nicolson")

    plt.ylim(0.999, 1.001)
    plt.grid(alpha=0.3)
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    V = potentiel_barriere(x)
    psi0 = paquet_initial(x)

    psi, normes = resoudre_CN(psi0, V)

    print("Norme initiale :", normes[0])
    print("Norme finale   :", normes[-1])
    print("Écart maximal  :", np.max(np.abs(normes - 1)))

    afficher_norme(normes)
