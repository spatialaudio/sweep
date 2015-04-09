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
    t = np.arange(0, sweep_time, 1 / fs)
    return np.sin(
        2 * np.pi * ((fstop - fstart) /
                     (2 * sweep_time) * t ** 2 + fstart * t))


def log_sweep(fstart, fstop, sweep_time, fs):
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
    t = np.arange(0, sweep_time, 1 / fs)
    return np.sin(2 * np.pi * sweep_time * fstart / np.log(fstop / fstart) *
                  np.exp(t / (sweep_time) * np.log(fstop / fstart) - 1))
