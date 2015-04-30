"""Calculation functions."""
from __future__ import division
import numpy as np
from scipy.signal import butter, lfilter, freqz
import matplotlib.pyplot as plt


def deconv_process(excitation, system_response, fs):
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
    if all(np.isreal(excitation)):
        NFFT = _pow2(len(excitation) + len(system_response) - 1)
        butter_w, butter_h = butter_bandpass(20, 10000, 44100, NFFT, order=2)
        excitation_f = np.fft.fft(excitation, NFFT)
        excitation_f_inv = 1 / excitation_f
    else:
        NFFT = len(excitation)
        butter_w, butter_h = butter_bandpass(20, 10000, 44100, NFFT, order=2)
        excitation_f_inv = 1 / excitation
    return np.fft.ifft(np.fft.fft(system_response, NFFT) * excitation_f_inv * butter_h).real


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
    return np.mean(np.abs(signal ** 2))


def _pow2(n):
    i = 1
    while i < n:
        i *= 2
    return i


def butter_bandpass(lower_bound, higher_bound, fs, NFFT, order):
    low = lower_bound / (fs / 2)
    high = higher_bound / (fs / 2)
    b, a = butter(order, [low, high], btype='band')
    butter_w, butter_h = freqz(b, a, worN=NFFT, whole=True)
    return butter_w, butter_h
