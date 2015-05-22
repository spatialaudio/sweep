"""Calculation functions."""
from __future__ import division
import numpy as np
from scipy.signal import butter, freqz
import matplotlib.pyplot as plt


def deconv_process(excitation, system_response, fs):
    NFFT = _pow2(len(excitation) + len(system_response) - 1)
    excitation_f = np.fft.fft(excitation, NFFT)
    excitation_f_inv = 1 / excitation_f
    #butter_w, butter_h = butter_bandpass(20, 20000, fs, NFFT, order=2)
    return np.fft.ifft(np.fft.fft(system_response, NFFT) * excitation_f_inv).real


def snr_db(signal, noise):
    """Calculating Signal-to-noise ratio.

    Parameters
    ----------
    excitation : array_like
          Signal vector
    system_response : array_like
          Noise vector

    Returns
    -------
    Return SNR in dB
    """
    return 10 * np.log10(_mean_power(signal) / _mean_power(noise))


def _mean_power(signal):
    return np.mean(np.abs(signal ** 2))


def _pow2(n):
    i = 1
    while i < n:
        i *= 2
    return i


def coherency(excitation, system_response):
    Rxx = np.correlate(excitation, excitation, 'full')
    Ryy = np.correlate(system_response, system_response, 'full')
    Ryx = np.correlate(system_response, excitation, 'full')
    return np.abs(Ryx) ** 2 / (Rxx * Ryy)


def butter_bandpass(lower_bound, higher_bound, fs, NFFT, order):
    wl = lower_bound / (fs / 2)
    wh = higher_bound / (fs / 2)
    b, a = butter(order, [wl, wh], btype='band')
    butter_w, butter_h = freqz(b, a, worN=NFFT, whole=True)
    return butter_w, butter_h


def limiter(signal, threshold_dB):
    array_positions = np.where(signal < threshold_dB)
    signal[array_positions] = threshold_dB
    return signal
