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
    return zero_padding(excitation, fs)


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
    return zero_padding(excitation, fs)


def noise(standard_deviation, duration, fs, seed):
    t = np.arange(0, duration, 1 / fs)
    np.random.seed(seed)
    return zero_padding(np.random.normal(0, standard_deviation, len(t)), fs)


def zero_padding(signal, fs):
    """Zeropadding a signal.

    It is a necessity to zeropadd the excitation signal
    to avoid zircular artifacts, if the system response is longer
    than the excitation signal. Therfore, the excitation signal has
    been extended for freely chosen 5 seconds. If you want to simulate
    the 'Cologne Cathedral', feel free to zeropadd more seconds.
    """
    number_of_zeros = 5 * fs
    return np.concatenate((signal, np.zeros(number_of_zeros)))
