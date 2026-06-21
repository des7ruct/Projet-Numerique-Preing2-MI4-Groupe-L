# Importations

import numpy as np
from numpy import zeros, linspace, abs, max


# Constants

NB_POINTS = 1000

DX = 0.01


# Functions

def firstDerivative(y):

    npts = len(y)
    dy = zeros(npts)
    
    dy[0], dy[1:-1], dy[-1] = (y[1] - y[0]) / DX, (y[2:] - y[:-2]) / (2 * DX), (y[-1] - y[-2]) / DX
    
    return dy


def secondDerivative(y):

    npts = len(y)
    d2y = zeros(npts)
    
    d2y[1:-1], d2y[0] = (y[2:] - 2 * y[1:-1] + y[:-2]) / (DX**2), d2y[1]
    
    return d2y


# Main Code

f, f_derivative = lambda x: x**2, lambda x: 2 * x

x = linspace(-5, 5, NB_POINTS)
y = f(x)

y_numerical, y_theorical, y_d2_numerical = firstDerivative(y), f_derivative(x), secondDerivative(y)

x = x != 0

error, errorbis = abs((y_numerical[x] - y_theorical[x]) / y_theorical[x]), abs(y_d2_numerical[1:-1] - 2.0)

print(f"Erreur relative maximale (dérivée 1ère) : {max(error):.2e}")
print(f"Erreur absolue maximale (dérivée seconde) : {np.max(errorbis):.2e}")