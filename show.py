"""You can figure the signal vector in both the time and frequency
domains simultaneously or separately, using the 'show' function
show.plot_y(x, fs).

Note that 'fs' has the same value as in
'generation' function. """

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt


def plot_t(x, fs, ax1=None):
    """Plot in time domain"""
    t = np.arange(len(x)) / fs
    h = 0
    if ax1 is None:
        fig, ax1 = plt.subplots()
        h = 1
    ax1.plot(t, x)
    ax1.grid()
    ax1.set_xlabel('t / s')
    ax1.set_ylabel('x(t)')
    ax1.set_title('time domain')
    if h == 1:
        plt.show()


def plot_f(x, fs, ax2=None):
    """Plot in frequency domain"""
    p = 20 * np.log10(abs(np.fft.rfft(x)))
    f = np.linspace(0, fs / 2, len(p))
    if ax2 is None:
        fig, ax2 = plt.subplots()
    ax2.plot(f, p)
    ax2.grid()
    ax2.set_xscale('log')
    ax2.set_xlabel('f / Hz')
    ax2.set_ylabel('A / dB')
    ax2.set_title('frequency domain')
    plt.show()


def plot_tf(x, fs):
    """Plot in both the time and frequency domains simultaneously"""
    fig, (ax1, ax2) = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.4)
    plot_t(x, fs, ax1)
    plot_f(x, fs, ax2)
