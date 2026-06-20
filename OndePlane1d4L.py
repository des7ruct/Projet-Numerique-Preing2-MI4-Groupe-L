# Importations :

from numpy import pi, exp, sqrt, real, imag, zeros, linspace

import matplotlib.pyplot as plt


# Constantes :

I = 1j



# Classes :

class Wave:

    amp: float 
    k: float
    omega: float


# Fonctions :

def verification(w: Wave) -> None :
    if (w.amp <= 0) :
        sys.exit("amp doit être strictement supérieur à 0")
    
    elif (w.k == 0) :
        sys.exit("k ne doit pas être égal à 0.")

    elif (w.omega <= 0) :
        sys.exit("omega doit être strictement supérieur à 0.")

    return None


def planeWave(w: Wave, x, t) :
    return w.amp * exp(I * (w.k * x - w.omega * t))
    

def makeWave() -> Wave :

    w = Wave()

    print("Saisir une amplitude : ")
    w.amp = float(input())

    print("Saisir un vecteur d'onde : ")
    w.k = float(input()) * pi

    print("Saisir une pulsation : ")
    w.omega = float(input()) * pi

    verification(w)

    return w


def graphique(w: Wave) -> None:
    x = linspace(0, 1, 500)
    t = 0

    psi = planeWave(w, x, t)

    psiReal = real(psi)
    psiImag = imag(psi)

    fig, ax = plt.subplots()


    ax.plot(x, psiReal, color="blue", linewidth=2)
    ax.plot(x, psiImag, color="red", linestyle="--", linewidth=2)

    ax.set_xlabel("Position x (m)", fontsize=10)
    ax.set_ylabel("Amplitude", fontsize=10)

    ax.grid(True)

    plt.show()


# Code principal

graphique(makeWave())


