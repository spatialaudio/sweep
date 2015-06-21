"""Calculation functions."""
from __future__ import division
import numpy as np
import plotting
from scipy.signal import butter, freqz


def deconv_process(excitation, system_response, fs):
    """Deconvolution.

    It is a necessity to zeropadd the excitation signal
    to avoid zircular artifacts, if the system response is longer
    than the excitation signal.
    """
    NFFT = _pow2(len(excitation) + len(system_response) - 1)
    excitation_f = np.fft.rfft(excitation, NFFT)
    return np.fft.irfft(np.fft.rfft(system_response, NFFT) / excitation_f)


def pnr_db(peak, noise):
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
    return 10 * np.log10(peak**2 / _mean_power(noise))


def _mean_power(signal):
    return np.mean(np.square(signal))


def peak_to_noise_ratio(ir, noise_bound_begin, fs):
    peak = ir[0]
    noise = ir[noise_bound_begin:]
    return pnr_db(peak, noise)


def _pow2(n):
    i = 1
    while i < n:
        i *= 2
    return i


def butter_bandpass_regularisation(lower_bound, higher_bound, fs, NFFT, order):
    wl = lower_bound / (fs / 2)
    wh = higher_bound / (fs / 2)
    b, a = butter(order, [wl, wh], btype='bandpass')
    butter_w, butter_h = freqz(b, a, worN=NFFT, whole=True)
    return butter_h


def butter_bandstop(lower_bound, higher_bound, fs, NFFT, order):
    wl = lower_bound / (fs / 2)
    wh = higher_bound / (fs / 2)
    b, a = butter(order, [wl, wh], btype='bandstop')
    butter_w, butter_h = freqz(b, a, worN=NFFT, whole=True)
    return butter_h


def butter_lowpass(fc, fs, NFFT, order):
    wc = fc / (fs / 2)
    b, a = butter(order, wc, btype='lowpass')
    butter_w, butter_h = freqz(b, a, worN=NFFT, whole=True)
    return butter_h


def awgn_noise(level, size=None, seed=1):
    scale = 10 ** (level / 20.)
    np.random.seed(seed)
    return np.random.normal(scale=scale, size=size)


def vector_distance(transfer_function_ideal, transfer_function_deconv):
    return np.sum(
        np.abs((transfer_function_ideal - transfer_function_deconv))**2)


def start_time_noise_floor(ir_noise_level, ir_db_decay, system_noise):
    m = ir_db_decay + np.abs(ir_noise_level)
    return (system_noise + np.abs(ir_noise_level))/m


def estimation_function(excitation, system_response, fs):
    NFFT = _pow2(len(excitation) + len(system_response) - 1)
    excitation_f = np.fft.rfft(excitation, NFFT)
    system_response_f = np.fft.rfft(system_response, NFFT)
    Rxx = np.conjugate(excitation_f)*excitation_f
    Ryy = np.conjugate(system_response_f)*system_response_f
    Rxy = excitation_f*np.conjugate(system_response_f)
    Ryx = system_response_f*np.conjugate(excitation_f)
    H1 = Ryx / Rxx
    H2 = Ryy / Rxy
    return np.fft.irfft(H1), np.fft.irfft(H2)
