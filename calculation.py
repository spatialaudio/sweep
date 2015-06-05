"""Calculation functions."""
from __future__ import division
import numpy as np
from . import plotting
import matplotlib.pyplot as plt
from scipy.signal import butter, freqz


def deconv_process(excitation, system_response, fs):
    """Deconvolution.

    It is a necessity to zeropadd the excitation signal
    to avoid zircular artifacts, if the system response is longer
    than the excitation signal.
    """
    NFFT = _pow2(len(excitation) + len(system_response) - 1)
    excitation_f = np.fft.rfft(excitation, NFFT)
    excitation_f_inv = 1 / excitation_f
    # butter_w, butter_h = butter_bandpass(10, 22049, fs, NFFT//2+1, order=2)
    return np.fft.irfft(np.fft.rfft(system_response, NFFT) * excitation_f_inv)


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
    Return SNR in dB
    """
    return 10 * np.log10(_mean_power(signal) / _mean_power(noise))


def _mean_power(signal):
    return np.mean(np.square(signal))


def _pow2(n):
    i = 1
    while i < n:
        i *= 2
    return i


def butter_bandpass(lower_bound, higher_bound, fs, NFFT, order):
    wl = lower_bound / (fs / 2)
    wh = higher_bound / (fs / 2)
    b, a = butter(order, [wl, wh], btype='band')
    butter_w, butter_h = freqz(b, a, worN=NFFT, whole=True)
    return butter_w, butter_h

#~ def limiter(signal_f_inv, threshold_dB):
    #~ signal_f_inv_abs = np.abs(signal_f_inv)
    #~ signal_f_inv_phase = np.angle(signal_f_inv)
    #~ signal_f_inv_abs_dB = plotting._dB_calculation(signal_f_inv_abs)
    #~ array_positions = np.where(signal_f_inv_abs_dB > signal_f_inv_abs_dB.max() + threshold_dB)
    #~ threshold = 10**((signal_f_inv_abs_dB.max()+threshold_dB)/20)
    #~ signal_f_inv_abs[array_positions] = threshold
    #~ signal_f_inv = signal_f_inv_abs * np.exp(1j*signal_f_inv_phase)
    #~ return signal_f_inv


def awgn_noise(level, size=None, seed=1):
    scale = 10 ** (level / 20.)
    np.random.seed(seed)
    return np.random.normal(scale=scale, size=size)

#~ def coherency(excitation, system_response):
    #~ Rxx = np.correlate(excitation, excitation, 'full')
    #~ Ryy = np.correlate(system_response, system_response, 'full')
    #~ Ryx = np.correlate(system_response, excitation, 'full')
    #~ return np.abs(Ryx) ** 2 / (Rxx * Ryy)
