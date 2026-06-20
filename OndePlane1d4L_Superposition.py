from numpy import pi, exp, real, linspace, cos
import matplotlib.pyplot as plt
import sys

I = 1j
NB_POINTS = 1000
T_INIT = 0


class Wave:
    amp: float
    k: float
    omega: float


def verification(w: Wave, delta_k: float) -> None:
    if w.amp <= 0:
        sys.exit("amp doit être strictement supérieur à 0.")
    if w.k == 0:
        sys.exit("k ne doit pas être égal à 0.")
    if delta_k == 0:
        sys.exit("delta_k ne doit pas être égal à 0.")
    if w.omega < 0:
        sys.exit("omega doit être supérieur ou égal à 0.")


def planeWave(w: Wave, x, t):
    return w.amp * exp(I * (w.k * x - w.omega * t))


def makeWave():
    w1 = Wave()
    w2 = Wave()
    w3 = Wave()

    print("Saisir une amplitude : ")
    w1.amp = float(input())

    print("Saisir un nombre d'onde : ")
    w1.k = float(input()) * pi

    print("Saisir un second nombre d'onde : ")
    delta_k = float(input()) * pi

    print("Saisir une pulsation : ")
    w1.omega = float(input()) * pi

    verification(w1, delta_k)

    w2.amp = w1.amp / 2
    w3.amp = w1.amp / 2

    w2.k = w1.k - delta_k / 2
    w3.k = w1.k + delta_k / 2

    w2.omega = w1.omega
    w3.omega = w1.omega

    return w1, w2, w3, delta_k


def graphique(waves) -> None:
    w1, w2, w3, delta_k = waves

    x = linspace(-pi / delta_k, pi / delta_k, NB_POINTS)
    t = T_INIT

    psi1 = planeWave(w1, x, t)
    psi2 = planeWave(w2, x, t)
    psi3 = planeWave(w3, x, t)

    psi_sum = psi1 + psi2 + psi3

    envelope = w1.amp * (1 + cos(delta_k / 2 * x))

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(x, real(psi1), color="purple", linewidth=1, label="Re[onde 0]")
    ax.plot(x, real(psi2), color="teal", linewidth=1, label="Re[onde 1]")
    ax.plot(x, real(psi3), color="olive", linewidth=1, label="Re[onde 2]")

    ax.plot(x, real(psi_sum), color="crimson", linewidth=2, label="Re[somme]")

    ax.plot(x, envelope, color="black", linestyle="--", linewidth=1.5, label="enveloppe")
    ax.plot(x, -envelope, color="black", linestyle="--", linewidth=1.5)

    ax.set_title("Superposition d'ondes planes")
    ax.set_xlabel("x [m]")
    ax.set_ylabel("amplitude")

    ax.grid(True)
    ax.legend(fontsize=8)

    plt.tight_layout()
    plt.show()


graphique(makeWave())
