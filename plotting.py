"""Plot Functions."""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import response


def plot_time(signal, fs=None, ax=None):
    """Plot in time domain.

    Parameters
    ----------
    signal  : signal vector
    fs : sampling frequency, optional
    ax : axis object, optional
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
    ax.grid()
    ax.set_ylabel('x(t)')
    ax.set_title('Time Domain')
    return ax


def plot_freq(signal, fs, ax=None):
    """Plot in frequency domain.

    Parameters
    ----------
    signal  : signal vector
    fs : sampling frequency
    ax : axis object, optional
    """
    p, f = _freq_vector(signal, fs)
    if ax is None:
        ax = plt.gca()
    ax.plot(f, p)
    ax.grid()
    ax.set_xscale('log')
    ax.set_xlabel('f / Hz')
    ax.set_ylabel('A / dB')
    ax.set_title('Frequency Domain')
    return ax


def plot_tf(signal, fs):
    """Plot in time and frequency domains simultaneously.

    Parameters
    ----------
    signal  : signal vector
    fs : sampling frequency
    """
    fig, (ax1, ax2) = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.4)
    plot_time(signal, fs, ax1)
    plot_freq(signal, fs, ax2)


def plot_iresponse(signal_excitation, signal_out, fs=None, ax=None):
    """Plot impulse response.

    Parameters
    -----------

    signal_excitation : vector of excitation signal
    signal_out        : vector of output signal
    fs                : sampling frequency, optional
    ax                : axis object, optional
    """
    h = response.calculate(signal_excitation, signal_out)
    if ax is None:
        ax = plt.gca()
    if fs is None:
        fs = 1
        ax.set_xlabel("Samples")
    else:
        ax.set_xlabel("t / s")
    t = _time_vector(signal_excitation, fs)
    ax.plot(t, h.real)
    ax.grid()
    ax.set_title("Impulse Response")
    ax.set_ylabel("h(t)")
    return ax


def plot_fresponse(signal_excitation, signal_out, fs, ax=None):
    """Plot frequency response.

    Parameters
    ----------

    signal_excitation : vector of excitation signal
    signal_out        : vector of oufput signal
    fs                : sampling frequency
    ax                : axis object, optional
    """
    h = response.calculate(signal_excitation, signal_out)
    p, f = _freq_vector(h.real, fs)
    if ax is None:
        ax = plt.gca()
    ax.plot(f, p)
    ax.grid()
    ax.set_xscale('log')
    ax.set_xlabel('f / Hz')
    ax.set_ylabel('A / dB')
    ax.set_title('Frequency Response')
    return ax


def plot_ifresponse(signal_excitation, signal_out, fs):
    """Plot impulse and frequency response simultaneously.

    Parameters
    ----------
    signal_excitation : vector of excitation signal
    signal_out        : vector of output signal
    fs                : sampling frequency
    """
    fig, (ax1, ax2) = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.4)
    plot_iresponse(signal_excitation, signal_out, fs, ax1)
    plot_fresponse(signal_excitation, signal_out, fs, ax2)


def _show_it():
    plt.show()


def _time_vector(signal, fs):
    t = np.arange(len(signal)) / fs
    return t


def _freq_vector(signal, fs):
    p = 20 * np.log10(np.abs(np.fft.rfft(signal)) / (len(signal)))
    f = np.linspace(0, fs / 2, len(signal) / 2 + 1)
    return p, f
