from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


def deconv(x, y, fs):
    X = np.fft.fft(x)
    Y = np.fft.fft(y)
    H = Y / X
    h = np.fft.ifft(H)
    print("h =", h)  # complex vector?
    t = np.arange(len(x)) / fs
    plt.plot(t, h.real)
    plt.grid()
    plt.title("impulse response")
    plt.show()
