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
     mode=None,
     sides=None,
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

    result, freqs = _spectral_helper(
        signal, fs, scale=scale, mode=mode, sides=sides, **kwargs)

    if ax is None:
        ax = plt.gca()

    if scale is None or scale == 'linear':
        ax.set_ylabel('Magnitude (linear)')
    elif scale == 'dB':
        ax.set_ylabel('Magnitude (dB)')
    if mode is None or mode == 'magnitude':
        ax.set_title('Magnitude Spectrum')
    elif mode == 'phase':
        ax.set_title('Phase Spectrum')
        ax.set_ylabel('Phase (rad)')
    elif mode == 'psd':
        ax.set_title('Power Density Spectrum')
        ax.set_ylabel('dB / Hz')
    ax.plot(freqs, result)
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
    if config is None or config == 'time+freq':
        plot_time(signal, fs, ax1)
        plot_freq(signal, fs, ax2, scale='dB')
        ax2.set_xscale('log')
    if config == 'freq+freq':
        plot_freq(signal, fs, ax1, scale='dB')
        plot_freq(signal, fs, ax2, mode='phase')


def _time_vector(signal, fs):
    return np.arange(len(signal)) / fs


def _spectral_helper(signal, fs, scale=None, mode=None, sides=None, **kwargs):

# modified function 'magnitude_spectrum' from matplotlib.pyplot


# we have to distinguish bewteen even or odd numbers of samples by
# calculating freqcenters
    if len(signal) % 2:
        freqcenter = (len(signal) - 1) // 2 + 1
    else:
        freqcenter = len(signal) // 2

    result = np.fft.fft(signal)
    freqs = np.fft.fftfreq(len(signal), 1 / fs)

    if mode == 'psd':
        result = np.abs(result) ** 2 / (len(signal) * fs)
    if mode is None or mode == 'magnitude':
        result = 2 / len(signal) * np.abs(result)
    if mode == 'phase':
        result = np.angle(result)
    if sides is None or sides == 'onesided':
        freqs = freqs[:freqcenter]
        result = result[:freqcenter]
    if sides == 'twosided':
        freqs = np.concatenate((freqs[freqcenter:], freqs[:freqcenter]))
        result = np.concatenate((result[freqcenter:], result[:freqcenter]))
    if mode == 'phase':
        result = np.unwrap(result, axis=0)
    if scale == 'dB' and mode != 'phase':
        result = 20 * np.log10(result)
    elif mode == 'psd':
        result = result / 2
    return result, freqs
