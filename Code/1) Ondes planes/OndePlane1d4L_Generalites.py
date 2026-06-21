# Importations :

from numpy import pi, exp, real, imag, linspace

import matplotlib.pyplot as plt

import sys


# Constants :

I, NB_POINTS, T_INIT = 1j, 500, 0


# Classes :

class Wave:

    amp: float 
    k: float
    omega: float


# Functions :

def verification(w: Wave) -> None :
    if (w.amp <= 0) :
        sys.exit("amp doit être strictement supérieur à 0")
    
    elif (w.k == 0) :
        sys.exit("k ne doit pas être égal à 0.")

    elif (w.omega < 0) :
        sys.exit("omega doit être supérieur ou égal à 0.")

    return None


def planeWave(w: Wave, x) :
    return w.amp * exp(I * (w.k * x - w.omega * T_INIT))
    

def makeWave() -> Wave :

    w = Wave()

    print("Saisir une amplitude : ")
    w.amp = float(input())

    print("Saisir un nombre d'onde : ")
    w.k = float(input()) * pi

    print("Saisir une pulsation : ")
    w.omega = float(input()) * pi

    verification(w)

    return w


def graph(w: Wave) -> None:
    x = linspace(0, 5, NB_POINTS)

    psi = planeWave(w, x)

    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(0, 5)


    ax.plot(x, real(psi), color = "blue", linewidth = 2, label="partie réelle (cos)")
    ax.plot(x, imag(psi), color = "red", linestyle = "dashed", linewidth = 2, label="partie imaginaire (sin)")

    ax.set_title(f"Parties réelle et imaginaire de l'onde plane à t = {T_INIT}", fontsize=12)
    ax.set_xlabel("Position x", fontsize=10)
    ax.set_ylabel("Amplitude", fontsize=10)

    ax.grid(True)

    plt.show()

    return None


# Main Code

graph(makeWave())
