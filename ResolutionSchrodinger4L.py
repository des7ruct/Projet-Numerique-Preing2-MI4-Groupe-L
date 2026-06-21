# Importations

from numpy import linspace, zeros, pi, sqrt, exp, trapezoid, abs
import matplotlib.pyplot as plt

# Constants

HBAR, M, V0, NX, NT, I, DT = 1.0, 1.0, 0.0, 500, 2000, 1j, 0.0005

K0, A = 3.0, 2.0


# Functions

def GaussWP_initial(x):

    factor, squareroot = (1.0 / (8.0 * pi ** 3)) ** 0.25, sqrt((4.0 * pi * M * A) / (M * A ** 2))
    return factor * squareroot * exp(I * K0 * x - (x ** 2) / (A ** 2))



# Main Code

x, t = linspace(-20, 20, NX), linspace(0, NT * DT, NT)
dx, psi = x[1] - x[0], zeros((NX, NT), dtype=complex)

psi[:, 0] = GaussWP_initial(x)


for j in range(0, NT - 1):

    d2psi = zeros(NX, dtype=complex)

    d2psi[1:-1], d2psi[0], d2psi[-1] = (psi[2:, j] - 2 * psi[1:-1, j] + psi[:-2, j]) / (dx ** 2), d2psi[1], d2psi[-2]
    
    terme_cinetique, terme_potentiel = (I * HBAR / (2 * M)) * d2psi, (-I * V0 / HBAR) * psi[:, j]
    
    psi[:, j+1] = psi[:, j] + DT * (terme_cinetique + terme_potentiel)


densite_initiale, densite_finale = trapezoid(abs(psi[:, 0]) ** 2, x), trapezoid(abs(psi[:, -1]) ** 2, x)

print(f"Conservation de la norme (Idéal = 1.0) :")
print(f"t = 0 : {densite_initiale:.4f}")
print(f"t_fin : {densite_finale:.4f}")