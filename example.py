#!/usr/bin/env python3
import generation
import show
import deconvolution
import numpy as np


# For example

"""Save the return value in a new variable which is the sweep
 vector. """

x = generation.log_sweep(1, 1000, 1, 44100)

"""We created a vector which sweeps from 1 Hz to 1000 Hz in 1
second at a sampling frequency of 44.1 kHz.
"""
# show.plot_tf(x, 44100)

"""Test functions for deconvolution"""

y = generation.log_sweep(1, 1000, 1, 44100)
noise = np.random.normal(0, 0.07, len(y))
noisy_signal = y + noise
deconvolution.deconv(x, noisy_signal, 44100)
