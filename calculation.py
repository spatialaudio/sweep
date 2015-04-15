"""Calculation functions."""
from __future__ import division
import numpy as np


def spectral_division(signal_excitation, system_response):
    """Calculating impulse response.

    Parameters
    ----------
    signal_excitation : array_like
          Excitation signal in time or frequency domains
    system_response: array_like
          System response in time domain

    Returns
    -------
    result.real : array_like
          Returns an impulse response
    """
    if all(np.isreal(signal_excitation)):
        NFFT = _pow2(len(signal_excitation) + len(system_response) - 1)
        signal_excitation_f = np.fft.fft(signal_excitation, NFFT)

    else:
        NFFT = len(signal_excitation)
        signal_excitation_f = signal_excitation

    return (np.fft.ifft(np.fft.fft(system_response, NFFT)) / signal_excitation_f).real


def snr_db(signal, noise):
    """Calculating Signal-to-noise ratio.

    Parameters
    ----------
    signal : array_like
          Signal vector
    noise : array_like
          Noise vector

    Returns
    -------
    Returns SNR in dB
    """
    return 10 * np.log10(_mean_power(signal) / _mean_power(noise))


def _mean_power(signal):
    return np.mean(abs(signal ** 2))


def _pow2(n):
    i = 1
    while i < n:
        i *= 2
    return i
