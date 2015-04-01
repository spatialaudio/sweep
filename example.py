"""A list of examples."""

#!/usr/bin/env python3
import generation
import plotting
import numpy as np


x = generation.log_sweep(1, 1000, 1, 44100)
"""We created a vector which sweeps from 1 Hz to 1000 Hz in 1
second at a sampling frequency of 44.1 kHz. Now you can plot it
in several domains."""

# plotting.plot_freq(x,44100)
# plotting._show_it()

"""Test functions for response calculation."""

y = generation.log_sweep(1, 1000, 1, 44100)
noise = np.random.normal(0, 0.07, len(y))
noisy_signal = y + noise
plotting.plot_ifresponse(x, noisy_signal, 44100)
plotting._show_it()
