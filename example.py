#!/usr/bin/env python3
"""A list of examples."""

import generation
import plotting
import numpy as np
import matplotlib.pyplot as plt
import calculation


x = generation.log_sweep(1, 1000, 1, 44100)

# We created a vector which sweeps from 1 Hz to 1000 Hz in 1
# second at a sampling frequency of 44.1 kHz. Now you can plot it
# in several domains.

# plotting.plot_time(x,44100)


# Test functions for response and snr calculations.

y = generation.log_sweep(1, 1000, 1, 44100)
noise = np.random.normal(0, 0.07, len(y))
noisy_signal = y + noise
z = calculation.spectral_division(x, noisy_signal)
# print(calculation.snr_db(x,noise))
plotting.plot_tf(z, 44100)
plt.show()
