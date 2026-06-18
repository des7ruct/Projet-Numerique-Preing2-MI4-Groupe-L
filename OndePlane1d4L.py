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

def Verification(w: Wave) -> None {
    if (w.amp <= 0) {
        sys.exit("amp doit être strictement supérieur à 0")
    }
    
    elif (w.k == 0) {
        sys.exit("k ne doit pas être égal à 0.")
    } 

    elif (w.omega <= 0) {
        sys.exit("omega doit être strictement supérieur à 0.")
    } 
}


def PlaneWave(w: Wave x: float, t: float) :
    if (k <= 0) {
        exit
    } 
    

    return amp * exp(I * (k * x - omega * t))
    




# Code principal

print("Saisir une amplitude : ")
amp = float input()

print("Saisir un vecteur d'onde : ")
k = float input()

print("Saisir une pulsation : ")
omega = float input()

MyWave = Wave(amp, k, omega)

Verification(MyWave)


fig, ax = plt.subplots()
ax.plot(x, y)
plt.show()
