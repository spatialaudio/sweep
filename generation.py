"""Signal Generation."""

import numpy as np


def lin_sweep(fstart, fstop, duration, fs):
    """Generation of a linear sweep signal.

    Parameters
    ----------
    fstart : int
           Start frequency in Hz
    fstop  : int
           Stop frequency in Hz
    duration : float
           Total length of signal in s
    fs : int
           Sampling frequency in Hz

    Returns
    -------
    array_like
         generated signal vector

    Note that the stop frequency must not be greater than half the
    sampling frequency (Nyquist-Shannon sampling theorem).

    """
    if fstop > fs / 2:
        raise ValueError("fstop must not be greater than fs/2")
    t = np.arange(0, duration, 1 / fs)
    excitation = np.sin(
        2 * np.pi * ((fstop - fstart) /
                     (2 * duration) * t ** 2 + fstart * t))
    # excitation = excitation - np.mean(excitation)  # remove direct component
    return excitation


def log_sweep(fstart, fstop, duration, fs):
    """Generation of a logarithmic sweep signal.

    Parameters
    ----------
    fstart : int
           Start frequency in Hz
    fstop  : int
           Stop frequency
    duration : float
           Total length of signal in s
    fs : int
           Sampling frequency in Hz

    Returns
    -------
    array_like
           Generated signal vector

    Note that the stop frequency must not be greater than half the
    sampling frequency (Nyquist-Shannon sampling theorem).

    """
    if fstop > fs / 2:
        raise ValueError("fstop must not be greater than fs/2")
    t = np.arange(0, duration, 1 / fs)
    excitation = np.sin(2 * np.pi * duration * fstart / np.log(fstop / fstart) *
                        (np.exp(t / duration * np.log(fstop / fstart)) - 1))
    # excitation = excitation - np.mean(excitation)  # remove direct component
    return excitation


def noise(noise_level_dB, duration, fs, seed=None):
    if seed is None:
        seed = 1
    np.random.seed(seed)
    standard_deviation = 10 ** (noise_level_dB / 20)
    return np.random.normal(0, standard_deviation, duration * fs)


def zero_padding(signal, fs, appending_time=None):
    """Zeropadding a signal."""
    if appending_time is None:
        appending_time = 5
    number_of_zeros = appending_time * fs
    return np.concatenate((signal, np.zeros(number_of_zeros)))
