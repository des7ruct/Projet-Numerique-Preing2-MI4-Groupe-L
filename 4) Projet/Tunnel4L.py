# Importations

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate
import scipy.sparse
import scipy.sparse.linalg



# Constantes

HBAR = 1.0
HBAR2 = HBAR * HBAR
MASS = 1.0
K0 = 2.0
SIGMA = 1.5
X0 = -25.0
V0 = 4.0
A_BARR = 1.0
X_BARR = 0.0
X_MIN = -60.0
X_MAX = 60.0
N_X = 2000

x = np.linspace(X_MIN, X_MAX, N_X)
DX = x[1] - x[0]

T_MAX = 30.0
N_T = 1500

t_grid = np.linspace(0.0, T_MAX, N_T)
DT = t_grid[1] - t_grid[0]



# Functions

def Compute_energy(k0=K0):
    return HBAR2 * k0**2 / (2 * MASS)


def Compute_kappa(v0=V0, k0=K0):
    energy = Compute_energy(k0)

    if v0 > energy:
        return np.sqrt(2 * MASS * (v0 - energy)) / HBAR

    return float("nan")


def Compute_group_velocity(k0=K0):
    return HBAR * k0 / MASS


def Compute_potential(x_array, v0=V0, a=A_BARR, x_barr=X_BARR):
    potential = np.zeros_like(x_array)
    inside = (x_array >= x_barr) & (x_array <= x_barr + a)
    potential[inside] = v0

    return potential


def Compute_ini_gaussian_wp(x_array, sigma=SIGMA, k0=K0, x0=X0):
    norm_factor = np.power(2 * np.pi * sigma**2, -0.25)
    enveloppe = np.exp(-(x_array - x0)**2 / (4 * sigma**2))
    phase = np.exp(1j * k0 * x_array)

    return norm_factor * enveloppe * phase


def Check_normalization(density_array, x_interval):
    return scipy.integrate.simpson(density_array, x=x_interval)


def Compute_transmitted_probability(density_array, x_array, x_right):
    mask = x_array > x_right

    return scipy.integrate.simpson(density_array[mask], x=x_array[mask])


def Build_cn_matrices(potential, dx=DX, dt=DT):
    n = len(potential)
    coeff_kin = HBAR2 / (2 * MASS * dx**2)
    main_diag = 2 * coeff_kin + potential
    off_diag = -coeff_kin * np.ones(n - 1)
    hamiltonian = scipy.sparse.diags([off_diag, main_diag, off_diag], [-1, 0, 1], format="csc")
    identity = scipy.sparse.identity(n, format="csc")
    factor = 1j * dt / (2 * HBAR)
    matrix_a = identity + factor * hamiltonian
    matrix_b = identity - factor * hamiltonian

    return matrix_a, matrix_b


def Solve_schrodinger(psi_ini, potential, n_t=N_T, dx=DX, dt=DT):
    n_x = len(psi_ini)
    psi = np.empty((n_t, n_x), dtype=complex)
    psi[0] = psi_ini
    matrix_a, matrix_b = Build_cn_matrices(potential, dx, dt)
    solver = scipy.sparse.linalg.splu(matrix_a.tocsc())
    print("Résolution de l'équation de Schrödinger avec Crank-Nicolson...")

    for n in range(n_t - 1):
        rhs = matrix_b.dot(psi[n])
        psi[n + 1] = solver.solve(rhs)

    print("Calcul terminé.")

    return psi


def Compute_tau_free(k0=K0, a=A_BARR):
    return a / Compute_group_velocity(k0)


def Compute_tau_crossing_numeric(psi, x_array, t_array, x_barr=X_BARR, a=A_BARR):
    x_in = x_barr
    x_out = x_barr + a
    v_g = Compute_group_velocity()
    t_entry = (x_in - X0) / v_g
    t_exit = None

    for n, t_val in enumerate(t_array):
        if t_val < t_entry:
            continue

        density = np.abs(psi[n])**2
        mask = x_array > x_out
        prob_trans = scipy.integrate.simpson(density[mask], x=x_array[mask])

        if prob_trans > 1e-3:
            pos_trans = scipy.integrate.simpson(x_array[mask] * density[mask], x=x_array[mask]) / prob_trans

            if pos_trans >= x_out:
                t_exit = t_val
                break

    if t_exit is None:
        return float("nan")

    return t_exit - t_entry


def plot_tunnel_snapshots(psi, potential, x_array, t_array):
    density_all = np.abs(psi)**2
    y_max = density_all.max() * 1.2
    indices = [0, int(0.38 * len(t_array)), int(0.45 * len(t_array)), int(0.55 * len(t_array)), int(0.70 * len(t_array))]
    fig, axes = plt.subplots(5, 1, figsize=(10, 12), sharex=True)

    for ax, idx in zip(axes, indices):
        density = density_all[idx]
        v_scaled = potential / V0 * y_max * 0.45
        ax.set_facecolor("pink")
        ax.fill_between(x_array, 0, v_scaled, color="orange", alpha=0.45, label="Barrière")
        ax.axvline(X_BARR, color="orange", linestyle="--", linewidth=1.5)
        ax.axvline(X_BARR + A_BARR, color="orange", linestyle="--", linewidth=1.5)
        ax.plot(x_array, density, color="green", linewidth=2.5, label=r"$|\psi(x,t)|^2$")
        x_max = x_array[np.argmax(density)]
        y_max_point = density.max()
        ax.plot(x_max, y_max_point, "o", color="red", markersize=5)
        trans = Compute_transmitted_probability(density, x_array, X_BARR + A_BARR)
        ax.set_ylabel(r"$|\psi|^2$")
        ax.set_title(f"t = {t_array[idx]:.2f}  |  probabilité transmise = {trans:.4f}", fontsize=10)
        ax.grid(alpha=0.25)

    axes[-1].set_xlabel("Position x")

    fig.suptitle("Effet tunnel : évolution du paquet d'ondes", fontsize=14, fontweight="bold")

    plt.xlim(-35, 20)
    plt.tight_layout()
    plt.show()



# Code principal

if __name__ == "__main__":

    energy = Compute_energy()
    kappa = Compute_kappa()

    print("")
    print("=== Paramètres de la simulation ===")
    print(f"k0 = {K0}")
    print(f"E = {energy:.4f}")
    print(f"V0 = {V0}")
    print(f"a = {A_BARR}")
    print(f"κ = {kappa:.4f}")
    print(f"v_g = {Compute_group_velocity():.4f}")
    print(f"régime = {'tunnel E<V0' if energy < V0 else 'classique E>V0'}")
    print("")

    potential = Compute_potential(x)
    psi_ini = Compute_ini_gaussian_wp(x)
    norm_ini = Check_normalization(np.abs(psi_ini)**2, x)
    print(f"Norme initiale = {norm_ini:.6f}")
    psi = Solve_schrodinger(psi_ini, potential)
    norm_fin = Check_normalization(np.abs(psi[-1])**2, x)
    print(f"Norme finale = {norm_fin:.6f}")
    tau_free_th = Compute_tau_free()
    tau_cross = Compute_tau_crossing_numeric(psi, x, t_grid)
    prob_trans = Compute_transmitted_probability(np.abs(psi[-1])**2, x, X_BARR + A_BARR)

    print("")
    print("=== Résultats ===")
    print(f"τ0 libre analytique = {tau_free_th:.4f}")
    print(f"τt tunnel numérique = {tau_cross:.4f}")
    print(f"Probabilité transmise finale = {prob_trans:.4f}")

    plot_tunnel_snapshots(psi, potential, x, t_grid)
