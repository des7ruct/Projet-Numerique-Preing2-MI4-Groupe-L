# Importations :

from numpy import pi, exp, sqrt, real, imag, linspace, abs
import matplotlib.pyplot as plt
import sys



# Constants :

I, HBAR, M, T_INIT, NB_POINTS = 1j, 1.0, 1.0, 0, 1000

#HBAR = 1.05457182 * 10 ** (-34)
#M = 9.1093837 * 10 ** (-31)



# Functions :

def GaussWP(k0, a, x):

    factor, squareroot = (1 / (8 * pi ** 3)) ** 0.25, sqrt((4 * pi * M * a) / (M * a ** 2 + 2 * I * HBAR * T_INIT))
    num, den, rest = M * (a ** 2 * k0 + 2 * I * x) ** 2, 4 * (M * a ** 2 + 2 * I * HBAR * T_INIT), (a ** 2 * k0 ** 2) / 4
    
    return factor * squareroot * exp(num / den - rest)


def verification(k0, a) -> None :

    if (a <= 0) :
        sys.exit("amp doit être strictement supérieur à 0")
    
    elif (k0 == 0) :
        sys.exit("k0 ne doit pas être égal à 0.")

    return None


def makePacket():

    print("Saisir une amplitude : ")
    a = float(input())

    print("Saisir un nombre d'onde : ")
    k0 = float(input()) * pi

    verification(k0, a)

    return (k0, a)


def graph(k0, a):

    x = linspace(-5, 5, NB_POINTS)
    psi = GaussWP(k0, a, x)
    
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.set_xlim(-5, 5)

    ax.plot(x, real(psi), color = "blue", linewidth = 2)
    ax.plot(x, imag(psi), color = "red", linestyle = "dashed")
    ax.plot(x, abs(psi), color = "black", linestyle = "dotted", linewidth = 1.5)

    ax.set_title(f"Paquet d'ondes gaussien à t = {T_INIT}", fontsize = 12)
    ax.set_xlabel("Position x", fontsize=10)
    ax.set_ylabel("Amplitude", fontsize=10)
    
    ax.grid(True)

    plt.show()

    return None

  

# Main Code

k0, a = makePacket()
graph(k0, a)