# Importations

from numpy import linspace, pi, sqrt, zeros, exp, abs, real
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation



# Constants

HBAR, M, NX, NT, I, DT = 1.0, 1.0, 600, 6000, 1j, 0.0002
K0, A = 4.0, 2.0
V_HEIGHT, X_START, X_END = 12.0, 4.0, 6.0



# Functions

def init():
    
    line_density.set_data([], [])
    line_real.set_data([], [])
    return line_density, line_real


def animate(i):

    i_t = i * 20
    if i_t >= NT:
        i_t = NT - 1
        
    density, real_part = abs(psi[:, i_t]) ** 2, real(psi[:, i_t])
    line_density.set_data(x, density)
    line_real.set_data(x, real_part)
    return line_density, line_real



# Main Code

x = linspace(-30, 30, NX)
dx = x[1] - x[0]

factor, squareroot = (1.0 / (8.0 * pi ** 3)) ** 0.25, sqrt((4.0 * pi * M * A) / (M * A ** 2))
psi_initial = factor * squareroot * exp(I * K0 * x - (x ** 2) / (A ** 2))
psi = zeros((NX, NT), dtype = complex)
psi[:, 0] = psi_initial

V = zeros(NX)
V[(x >= X_START) & (x <= X_END)] = V_HEIGHT

for j in range(0, NT - 1):
    d2psi = zeros(NX, dtype = complex)
    d2psi[1:-1], d2psi[0], d2psi[-1] = (psi[2:, j] - 2 * psi[1:-1, j] + psi[:-2, j]) / (dx ** 2), d2psi[1], d2psi[-2]
    kinetic, potential = (I * HBAR / (2 * M)) * d2psi, (-I / HBAR) * V * psi[:, j]
    psi[:, j+1] = psi[:, j] + DT * (kinetic + potential)


'''
for j in range(0, NT - 1):
    d2psi = zeros(NX, dtype=complex)
    d2psi[1:-1], d2psi[0], d2psi[-1] = (psi[2:, j] - 2 * psi[1:-1, j] + psi[:-2, j]) / (dx**2), d2psi[1], d2psi[-2]
    
    psi[:, j+1] = psi[:, j] + DT * (I * HBAR / (2 * M)) * d2psi
'''

fig, ax = plt.subplots(figsize=(10, 10))
ax.set_xlim(-30, 30)
ax.set_ylim(-0.05, 0.6)
ax.set_xlabel("Position x", fontsize = 10)
ax.set_ylabel("Densité de probabilité |Psi|^2", fontsize = 10)
ax.set_title("Evolution temporelle et étalement du paquet d'ondes libre", fontsize=12)
ax.grid(True, linestyle=":", alpha=0.5)

line_density, = ax.plot([], [], color = "black", linewidth = 2, label = r"|psi|^2")
line_real, = ax.plot([], [], color = "blue", alpha = 0.3, label = "Re(psi)")

ax.legend(loc = "upper left")

ani = FuncAnimation(fig, animate, init_func = init, frames = NT // 20, interval = 25, blit = True)
plt.show()