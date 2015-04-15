#!/usr/bin/env python3
"""A list of examples."""

import generation
import plotting
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import calculation


x = generation.log_sweep(1, 1000, 1, 44100)

# We created a vector which sweeps from 1 Hz to 1000 Hz in 1
# second at a sampling frequency of 44.1 kHz. Now you can plot it
# in several domains.


ax = plotting.plot_freq(
    x,
     fs=44100,
     scale='dB',
     side='onesided',
     bode='mag')
ax.set_xscale('log')  # if side = 'twosided' you have to disable this line
plt.show()


# Test functions for response and snr calculations.

y = generation.log_sweep(1, 1000, 1, 44100)
noise = np.random.normal(0, 0.3, len(y))
noisy_signal = y + noise
z = calculation.spectral_division(x, noisy_signal)

# print(calculation.snr_db(x,noise))
# ax = plotting.plot_freq(z, fs =44100, scale = 'dB')
# ax.set_xscale('log')
# plt.show()
