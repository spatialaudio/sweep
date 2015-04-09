"""Plot Functions."""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import calculation


def plot_time(signal, fs=None, ax=None):
    """Plot in time domain.

    Parameters
    ----------
    signal : array_like
          Signal vector
    fs : int, optional
          Sampling frequency in Hz. If None (default),
          fs switches to number of bins.
    ax : axis object, optional

    Returns
    ------
    ax : axis object
    """
    if ax is None:
        ax = plt.gca()
    if fs is None:
        fs = 1
        ax.set_xlabel("Samples")
    else:
        ax.set_xlabel("t / s")
    t = _time_vector(signal, fs)
    ax.plot(t, signal)
    ax.grid(True)
    ax.set_ylabel('x(t)')
    ax.set_title('Something in Time Domain')
    # plt.savefig('myplot_t.png')
    return ax


def plot_freq(signal, fs, ax=None):
    """Plot in frequency domain.

    Parameters
    ----------
    signal : array_like
          Signal vector
    fs : int
      Sampling frequency in Hz
    ax : axis object, optional

    Returns
    -------
    ax: axis object
    """
    mag, pha, f = _freq_vector(signal, fs)
    if ax is None:
        ax = plt.gca()
    ax.plot(f, mag)
    # ax.plot(f, pha)
    ax.grid(True)
    ax.set_xscale('log')
    ax.set_xlabel('f / Hz')
    ax.set_ylabel('Something')
    ax.set_title('Something in Frequency Domain')
    # plt.savefig('myplot_f.pdf')
    return ax


def plot_tf(signal, fs):
    """Plot in time and frequency domains simultaneously.

    Parameters
    ----------
    signal : array_like
          Signal vector
    fs : int
          Sampling Frequency in Hz
    """
    fig, (ax1, ax2) = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.6)
    plot_time(signal, fs, ax1)
    plot_freq(signal, fs, ax2)
    # plt.savefig('myplot_tf.pdf')


def _time_vector(signal, fs):
    return np.arange(len(signal)) / fs


def _freq_vector(signal, fs):
    mag = 20 * np.log10(np.abs(np.fft.rfft(signal)) / (len(signal)))
    pha = np.unwrap(
        np.arctan2(np.fft.rfft(signal).imag,
                   np.fft.rfft(signal).real))
    f = np.linspace(0, fs / 2, len(signal) // 2 + 1)
    return mag, pha, f
