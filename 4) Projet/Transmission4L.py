# Importations

import numpy as np
import matplotlib.pyplot as plt


# Constants

hbar, m, V0, a, E_min, E_max, N = 1.0, 1.0, 4.0, 1.0, 0.01, 12.0, 2000



# Functions

def transmission_analytique(E, V0 = V0, a = a):
    
    if E < V0:
        kappa = np.sqrt(2 * m * (V0 - E)) / hbar
        return 1 / (1 + (V0 ** 2 * np.sinh(kappa * a)**2) / (4 * E * (V0 - E)))

    elif E > V0:
        q = np.sqrt(2 * m * (E - V0)) / hbar
        return 1 / (1 + (V0 ** 2 * np.sin(q * a) ** 2) / (4 * E * (E - V0)))

    return 1.0



# Main code

E_values = np.linspace(E_min, E_max, N)
T_values = np.array([transmission_analytique(E) for E in E_values])

E0 = 2.0
Tan = transmission_analytique(E0)
Tnum = 0.0886

plt.figure(figsize=(10, 6))

plt.axvspan(0, V0, color = "red", alpha = 0.45)
plt.axvspan(V0, E_max, color = "green", alpha = 0.45)

plt.plot(E_values, T_values, color = "blue", linewidth = 3, label = r"$T(E)$ analytique")
plt.axvline(V0, color = "orange", linestyle = "--", linewidth = 2, label = rf"$V_0={V0}$")
plt.scatter([E0], [Tnum], s = 120, color = "red", edgecolors = "black", zorder = 5, label = rf"$T_{{num}} = {Tnum:.4f}$ $(E=2)$")
plt.scatter([E0], [Tan], s = 120, color = "green", edgecolors = "black", zorder = 5, label = rf"$T_{{an}} = {Tan:.4f}$ $(E=2)$")

plt.text(1.1, 0.88, r"Régime tunnel" + "\n" + r"$E<V_0$", color = "red", fontsize = 14, ha = "center")
plt.text(7.8, 0.88, r"Régime classique" + "\n" + r"$E>V_0$", color = "green", fontsize = 14, ha = "center")
plt.annotate(rf"$T_{{num}}={Tnum:.4f}$", xy = (E0, Tnum), xytext = (2.6, 0.16), color = "red", fontsize = 12, arrowprops = dict(arrowstyle = "->", color = "red", linewidth = 2))
plt.annotate(rf"$T_{{an}} = {Tan:.4f}$", xy = (E0, Tan), xytext = (2.6, 0.02), color = "green", fontsize = 12, arrowprops = dict(arrowstyle = "->", color = "green", linewidth = 2))

plt.xlabel(r"Énergie $E$ (u.r.)", fontsize = 13)
plt.ylabel(r"Coefficient de transmission $T(E)$", fontsize = 13)
plt.title(rf"Coefficient de transmission — barrière rectangulaire  $V_0={V0}$,  $a={a}$", fontsize = 15, fontweight = "bold")
plt.xlim(0, E_max)
plt.ylim(0, 1.05)

plt.grid(alpha=0.25)

plt.legend(loc="center right", fontsize=11)

plt.tight_layout()

plt.show()
