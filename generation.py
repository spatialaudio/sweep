import numpy as np


def lin_sweep(fstart, fstop, sweep_time, fs):
    if fstop > fs / 2:
        raise ValueError("fstop must not be greater than fs/2")
    t = np.arange(0, sweep_time, 1 / fs)
    x = np.sin(
        2 * np.pi * ((fstop - fstart) /
                     (2 * sweep_time) * t ** 2 + fstart * t))
    return x


def log_sweep(fstart, fstop, sweep_time, fs):
    if fstop > fs / 2:
        raise ValueError("fstop must not be greater than fs/2")
    t = np.arange(0, sweep_time, 1 / fs)
    x = np.sin(2 * np.pi * sweep_time * fstart / np.log(fstop / fstart) *
               np.exp(t / (sweep_time) * np.log(fstop / fstart) - 1))
    return x
