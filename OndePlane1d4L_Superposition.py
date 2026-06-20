# Importations :

from numpy import pi, exp, real, imag, linspace, cos, sin

import matplotlib.pyplot as plt

import sys


# Constants :

I = 1j

NB_POINTS = 1000

T_INIT = 0


# Classes :

class Wave:

    amp: float 
    k0: float
    omega: float


# Functions :

def verification(w: Wave, delta_k: float) -> None :
    if (w.amp <= 0) :
        sys.exit("amp doit être strictement supérieur à 0")
    
    elif (w.k0 == 0) :
        sys.exit("k0 ne doit pas être égal à 0.")

    elif (delta_k == 0) :
        sys.exit("delta k ne doit pas être égal à 0.")

    elif (w.omega < 0) :
        sys.exit("omega doit être supérieur ou égal à 0.")

    return None


def planeWave(w: Wave, x) :
    return w.amp * exp(I * (w.k0 * x - w.omega * T_INIT))
    

def makeWave() -> Wave :

    w1 = w2 = w3 = Wave()

    print("Saisir une amplitude : ")
    w1.amp = float(input())

    print("Saisir un nombre d'onde : ")
    w1.k0 = float(input()) * pi

    print("Saisir un second nombre d'onde : ")
    delta_k = float(input()) * pi

    print("Saisir une pulsation : ")
    w1.omega = float(input()) * pi

    verification(w1, delta_k)

    w2.amp = w3.amp = w1.amp / 2

    w2.k0, w3.k0 = w1.k0 - (delta_k / 2), w1.k0 + (delta_k / 2)
    
    w2.omega = w3.omega = w1.omega

    return (w1, w2, w3, delta_k)


def graph(waves) -> None:

    w1, w2, w3, delta_k = waves

    x = linspace(-pi / delta_k, pi / delta_k, NB_POINTS)

    psi1, psi2, psi3 = planeWave(w1, x), planeWave(w2, x), planeWave(w3, x)

    psi_sum = psi1 + psi2 + psi3
    sup = inf = w1.amp * (1 + cos(delta_k / 2 * x))
    inf *= -1

    fig, ax = plt.subplots(figsize = (10, 10))

    ax.plot(x, real(psi1), color = "blue")
    ax.plot(x, real(psi2), color = "orange", linestyle = "dashdot")
    ax.plot(x, real(psi3), color = "orange", linestyle = "dashdot")

    ax.plot(x, real(psi_sum), color = "black", linewidth = 2, linestyle = "dashed", alpha = 0.5)

    ax.plot(x, sup, color = "red", linewidth = 1.5, linestyle = "dashdot")
    ax.plot(x, inf, color = "red", linewidth = 1.5, linestyle = "dashdot")

    ax.set_title(f"Superposition de 3 ondes planes et son enveloppe à t = {T_INIT}", fontsize=12)
    ax.set_xlabel("Position x", fontsize = 10)
    ax.set_ylabel("Amplitude", fontsize = 10)

    ax.grid(True)

    plt.show()

    return None


# Main Code

graph(makeWave())
