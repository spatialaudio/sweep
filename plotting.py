"""Plot Functions."""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import calculation


def plot_time(signal, fs=None, ax=None, **kwargs):
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
        ax.set_xlabel("t (s)")
    t = _time_vector(signal, fs)
    ax.plot(t, signal)
    ax.grid(True)
    ax.set_ylabel('x(t)')
    ax.set_title('Time Domain')
    return ax


def plot_freq(
    signal,
     fs,
     ax=None,
     scale=None,
     bode=None,
     side=None,
     **kwargs):
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
    mag_onesided, mag_twosided, pha_onesided, pha_twosided = _mag_pha_vector(
        signal)
    f_onesided = _freq_vector_onesided(signal, fs)
    f_twosided = _freq_vector_twosided(signal, fs)
    if ax is None:
        ax = plt.gca()
    if side is None or side == 'onesided':
        f = f_onesided
        mag = mag_onesided
        pha = pha_onesided
    elif side == 'twosided':
        f = f_twosided
        mag = mag_twosided
        pha = pha_twosided
        ax.set_xscale = 'symlog'
    if scale is None or scale == 'linear':
        mag = mag
        ax.set_ylabel('Magnitude (linear)')
    elif scale == 'dB':
        mag = 20 * np.log10(mag)
        ax.set_ylabel('Magnitude (dB)')
    if bode is None or bode == 'mag':
        ax.plot(f, mag)
        ax.set_title('Magnitude Spectrum')
    elif bode == 'phase':
        ax.plot(f, pha)
        ax.set_ylabel('Phase (rad)')
        ax.set_title('Phase Spectrum')
    ax.set_xlabel('f (Hz)')
    ax.grid(True)
    return ax


def plot_tf(signal, fs, config=None, **kwargs):
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
    if config is None:
        plot_time(signal, fs, ax1)
        plot_freq(signal, fs, ax2, scale='log')
    if config == 'freq+freq':
        plot_freq(signal, fs, ax1, scale='log')
        plot_freq(signal, fs, ax2, scale='log', bode='phase')


def _time_vector(signal, fs):
    return np.arange(len(signal)) / fs


def _freq_vector_onesided(signal, fs):
    f_onesided = np.linspace(0, fs / 2, len(signal) // 2 + 1)
    return f_onesided


def _freq_vector_twosided(signal, fs):
    f_twosided = np.linspace(-fs / 2, fs / 2, len(signal))
    return f_twosided


def _mag_pha_vector(signal):
    signal_f_onesided = np.fft.rfft(signal)
    signal_f_twosided = np.fft.fftshift(np.fft.fft(signal))
    mag_onesided = 2 / len(signal) * np.abs(signal_f_onesided)
    mag_twosided = 2 / len(signal) * np.abs(signal_f_twosided)
    pha_onesided = np.unwrap(
        np.arctan2(signal_f_onesided.imag,
                   signal_f_onesided.real))
    pha_twosided = np.unwrap(
        np.arctan2(signal_f_twosided.imag,
                   signal_f_twosided.real))
    return mag_onesided, mag_twosided, pha_onesided, pha_twosided
