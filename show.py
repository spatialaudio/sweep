import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


def sweep(x, sweep_time, fs):

    t = np.arange(0, sweep_time, 1 / fs)
    p = 20 * np.log10(abs(sp.fft(x)))
    f = np.linspace(0, fs / 2, len(p))
    plt.figure(1)
    plt.subplot(211)
    plt.plot(t, x)
    plt.grid()
    plt.subplot(212)
    plt.plot(f, p)
    plt.xscale('log')
    plt.grid()
    plt.show()
