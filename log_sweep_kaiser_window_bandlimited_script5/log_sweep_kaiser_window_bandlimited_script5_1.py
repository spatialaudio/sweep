#!/usr/bin/env python3

"""The influence of windowing of log. bandlimited sweep signals when using a
   Kaiser Window by fixing beta (=2) and fade_out (=0).
   fstart = 100 Hz
   fstop = 5000 Hz

"""


import sys
sys.path.append('..')

import measurement_chain
import plotting
import calculation
import generation
import matplotlib.pyplot as plt
import windows
from scipy.signal import lfilter
import numpy as np


# Parameters of the measuring system

fs = 44100

fstart = 100
fstop = 5000
duration = 1
pad = 4

# Generate excitation signal

excitation = generation.log_sweep(fstart, fstop, duration, fs)
N = len(excitation)


# Noise in measurement chain

noise_level_db = -30
noise = measurement_chain.additive_noise(noise_level_db)

# FIR-Filter-System

dirac_system = measurement_chain.convolution([1.0])

# Combinate system elements

system = measurement_chain.chained(dirac_system, noise)

# Spectrum of dirac for reference

dirac = np.zeros(pad * fs)
dirac[0] = 1
dirac_f = np.fft.rfft(dirac)

# Lists
beta = 7
fade_in_list = np.arange(0, 1001, 1)
fade_out = 0


def get_results(fade_in):
    excitation_windowed = excitation * windows.window_kaiser(N,
                                                             fade_in,
                                                             fade_out,
                                                             fs, beta)
    excitation_windowed_zeropadded = generation.zero_padding(
        excitation_windowed, pad, fs)
    excitation_zeropadded = generation.zero_padding(excitation, pad, fs)
    system_response = system(excitation_windowed_zeropadded)
    ir = calculation.deconv_process(excitation_zeropadded,
                                    system_response,
                                    fs)
    return ir


with open("log_sweep_kaiser_window_bandlimited_script5_1.txt", "w") as f:
    for fade_in in fade_in_list:
        ir = get_results(fade_in)
        pnr = calculation.pnr_db(ir[0], ir[1:4 * fs])
        spectrum_distance = calculation.vector_distance(
            dirac_f, np.fft.rfft(ir[:pad * fs]))
        f.write(
            str(fade_in) + " " + str(pnr) +
            " " + str(spectrum_distance) + " \n")
