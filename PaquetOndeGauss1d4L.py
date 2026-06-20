import numpy as np
import matplotlib.pyplot as plt

k0 = 1
a = 5
x0 = 0

xmin = -20
xmax = 100

N = 3000

x = np.linspace(xmin, xmax, N)

psi = np.exp(-(x - x0)**2 / a**2) * np.exp(1j * k0 * x)

norme = np.trapz(np.abs(psi)**2, x)

psi = psi / np.sqrt(norme)

rho = np.abs(psi)**2

plt.figure(figsize=(8,5))

plt.plot(
    x,
    np.real(psi),
    color='royalblue',
    linewidth=2,
    label='Partie réelle'
)

plt.plot(
    x,
    np.imag(psi),
    '--',
    color='orange',
    linewidth=2,
    label='Partie imaginaire'
)

plt.plot(
    x,
    rho,
    color='green',
    linewidth=2,
    label=r'$|\Psi|^2$'
)

plt.grid(alpha=0.3)

plt.xlim(-20, 40)

plt.xlabel("Position x")
plt.ylabel("Amplitude")

plt.title("Paquet d'ondes gaussien normalisé")

plt.legend()

plt.tight_layout()

plt.show()
