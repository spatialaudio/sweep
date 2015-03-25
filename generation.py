import numpy as np


def lin_sweep(fstart, fstop, sweep_time, fs):
    """Choose the excitation signal which you want to generate and fill
    in the parameters lin_sweep(fstart, fstop, sweep_time, fs),
    where:
    fstart is the start frequency
    fstop  is the stop frequency
    sweep_time is the total length of sweep
    fs is the sampling frequency

    Note that the stop frequency must not be greater than half the
    sampling frequency (Nyquist-Shannon sampling theorem)
    """

    if fstop > fs / 2:
        raise ValueError("fstop must not be greater than fs/2")
    t = np.arange(0, sweep_time, 1 / fs)
    x = np.sin(
        2 * np.pi * ((fstop - fstart) /
                     (2 * sweep_time) * t ** 2 + fstart * t))
    return x


def log_sweep(fstart, fstop, sweep_time, fs):
    """Choose the excitation signal which you want to generate and fill
    in the parameters log_sweep(fstart, fstop, sweep_time, fs),
    where:
    fstart is the start frequency
    fstop  is the stop frequency
    sweep_time is the total length of sweep
    fs is the sampling frequency

    Note that the stop frequency must not be greater than half the
    sampling frequency (Nyquist-Shannon sampling theorem).
    """

    if fstop > fs / 2:
        raise ValueError("fstop must not be greater than fs/2")
    t = np.arange(0, sweep_time, 1 / fs)
    x = np.sin(2 * np.pi * sweep_time * fstart / np.log(fstop / fstart) *
               np.exp(t / (sweep_time) * np.log(fstop / fstart) - 1))
    return x
