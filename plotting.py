"""Plot Functions."""

from __future__ import division
import numpy as np
import matplotlib.pyplot as plt
import calculation


def plot_time(
    signal,
     fs=None,
     ax=None,
     scale='linear',
     sides='onesided',
     title=None,
     **kwargs):
    if ax is None:
        ax = plt.gca()
    if fs is None:
        fs = 1
        ax.set_xlabel("Samples")
    else:
        ax.set_xlabel("t (s)")
    t = _time_vector_onesided(signal, fs)
    if scale == 'linear':
        ax.set_ylabel('x(t) (linear)')
    elif scale == 'dB':
        signal = _dB_calculation(signal)
        ax.set_ylabel('x(t) (dB)')
    else:
        raise NameError("Invalid scale")
    if sides == 'onesided':
        ax.plot(t, signal)
    elif sides == 'twosided':
        ax.plot(time_vector_twosided(signal, fs), np.fft.fftshift(signal))
    else:
        raise NameError("Invalid sides")
    if title is None:
            ax.set_title('')
    ax.set_title(title)
    ax.grid(True)
    # ax.set_xlim([-1, (len(t)/fs)/5])
    return ax


def plot_freq(
    signal,
     fs,
     ax=None,
     scale='linear',
     mode='magnitude',
     sides=None,
     **kwargs):

    result, freqs = _spectral_helper(
        signal, fs, scale=scale, mode=mode, **kwargs)

    if ax is None:
        ax = plt.gca()

    if scale == 'linear':
        ax.set_ylabel('Magnitude (linear)')
    elif scale == 'dB':
        ax.set_ylabel('Magnitude (dB)')
    else:
        raise NameError("Invalid scale")
    if mode == 'magnitude':
        ax.set_title('Magnitude Spectrum')
    elif mode == 'phase':
        ax.set_title('Phase Spectrum')
        ax.set_ylabel('Phase (rad)')
    elif mode == 'psd':
        ax.set_title('Power Density Spectrum')
        ax.set_ylabel('dB / Hz')
    else:
        raise NameError("Invalid mode")
    ax.plot(freqs, result)
    ax.set_xlabel('f (Hz)')
    ax.grid(True)
    return ax


def plot_tf(signal, fs, config='time+freq', **kwargs):
    fig, (ax1, ax2) = plt.subplots(2, 1)
    plt.subplots_adjust(hspace=0.6)
    if config == 'time+freq':
        plot_time(signal, fs, ax1)
        plot_freq(signal, fs, ax2, scale='dB')
        ax2.set_xscale('log')
    elif config == 'mag+pha':
        plot_freq(signal, fs, ax1, scale='dB')
        plot_freq(signal, fs, ax2, mode='phase')
    else:
        raise NameError("Invalid config")


def _spectral_helper(signal, fs, scale=None, mode=None, sides=None, **kwargs):

    result = np.fft.rfft(signal)
    freqs = np.fft.rfftfreq(len(signal), 1 / fs)

    if mode == 'psd':
        result = np.abs(result) ** 2 / (len(signal) * fs)
    if mode is None or mode == 'magnitude':
        result = 2 / len(signal) * np.abs(result)
    if mode == 'phase':
        result = np.angle(result)
        result = np.unwrap(result, axis=0)
    if scale == 'dB' and mode != 'phase':
        result = _dB_calculation(result)
    elif mode == 'psd':
        result = result / 2
    return result, freqs


def _dB_calculation(signal):
    return 20 * np.log10(np.abs(signal))


def _time_vector_onesided(signal, fs):
    return np.arange(len(signal)) / fs


def _time_vector_twosided(signal, fs):
    return np.linspace(-len(signal) // 2, len(signal) // 2, len(signal)) / fs
