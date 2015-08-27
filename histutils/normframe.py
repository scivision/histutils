from __future__ import division
from numpy import float32 #memory saving

"""
inputs:
-------
I: 2-D Numpy array of grayscale image data
Clim: length 2 of tuple or numpy 1-D array specifying lowest and highest expected values in grayscale image
"""

def normframe(I,Clim):
    Vmin = Clim[0]; Vmax = Clim[1]

    return (I.astype(float32).clip(Vmin, Vmax) - Vmin) / (Vmax - Vmin) #stretch to [0,1]
