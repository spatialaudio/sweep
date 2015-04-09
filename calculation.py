"""Response calculation."""
from __future__ import division
import numpy as np


def calculate(signal_excitation, signal_out):
    """Function returns impulse response."""
    X = np.fft.fft(signal_excitation)
    Y = np.fft.fft(signal_out)
    H = Y / X
    h = np.fft.ifft(H)
    return h
