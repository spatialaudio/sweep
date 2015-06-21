#!/usr/bin/env python3

"""AKF of windowed log. sweep.

"""


import sys
sys.path.append('..')

import plotting
import generation
import matplotlib.pyplot as plt
import windows
from scipy.signal import lfilter, fftconvolve
import numpy as np


# Parameters of the measuring system

fs = 44100

fstart = 1
fstop = 22050
duration = 1


# Generate excitation signal

excitation = generation.log_sweep(fstart, fstop, duration, fs)
N = len(excitation)

excitation_windowed_beta2 = excitation * windows.window_kaiser(N,
                                                               500,
                                                               500,
                                                               fs, beta=2)
excitation_windowed_beta7 = excitation * windows.window_kaiser(N,
                                                               500,
                                                               500,
                                                               fs, beta=7)


# Windowed Sweep-Signal

plotting.plot_time(excitation, fs)
plt.savefig('log_excitation.png')
plt.close()

plotting.plot_time(excitation_windowed_beta7, fs)
plt.savefig('log_excitation_windowed')
plt.close()

# AKF

akf_excitation_rect = fftconvolve(excitation, excitation[::-1])
akf_excitation_kaiser_beta2 = fftconvolve(excitation_windowed_beta2,
                                          excitation_windowed_beta2[::-1])
akf_excitation_kaiser_beta7 = fftconvolve(excitation_windowed_beta7,
                                          excitation_windowed_beta7[::-1])


plotting.plot_time(akf_excitation_rect, scale='db', label='AKF Rect Window')
plotting.plot_time(akf_excitation_kaiser_beta2, scale='db',
                   label=r'AKF Kaiser Window $\beta=2$')
plotting.plot_time(akf_excitation_kaiser_beta7, scale='db',
                   label=r'AKF Kaiser Window $\beta=7$')


plt.legend(loc='lower left')
plt.savefig('log_AKFs.png')
