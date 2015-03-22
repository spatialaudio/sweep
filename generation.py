import numpy as np
import show


def lin_sweep(fstart, fstop, sweep_time, fs):
    if fs / 2 < fstop:
        print("fstop must be less than fs/2")
    t = np.arange(0, sweep_time, 1 / fs)
    x = np.sin(
        2 * np.pi * ((fstop - fstart) /
                     (2 * sweep_time) * t ** 2 + fstart * t))
    return (x, sweep_time, fs)


def log_sweep(fstart, fstop, sweep_time, fs):
    if fs / 2 < fstop:
        print("fstop must be less than fs/2")
    t = np.arange(0, sweep_time, 1 / fs)
    x = np.sin(2 * np.pi * sweep_time * fstart / np.log(fstop / fstart)
               * np.exp(t / (sweep_time) * np.log(fstop / fstart) - 1))
    return (x, sweep_time, fs)


x, y, z = lin_sweep(10, 10000, 1, 20000)
show.sweep(x, y, z)
