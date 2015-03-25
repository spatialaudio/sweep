#!/usr/bin/env python3
import generation
import show

# For example

"""Save the return value in a new variable which is the sweep
 vector. """

x = generation.log_sweep(1, 1000, 2, 44100)

"""We created a vector which sweeps from 1 Hz to 1000 Hz in 2
seconds at a sampling frequency of 44.1 kHz.
"""
show.sweep(x, 2, 44100, "tfdomain")
