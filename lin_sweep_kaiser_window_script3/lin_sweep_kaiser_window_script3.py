#!/usr/bin/env python3

"""The influence of windowing of lin. sweep signals when using a
   Kaiser Window by fixing beta (=7) and fade_out (=0).
   fstart = 1 Hz
   fstop = 22050 Hz
   FIR-Filter: Bandstop
   Deconvolution: Unwindowed Excitation
"""


import sys
sys.path.append('..')

import measurement_chain
import plotting
import calculation
import generation
import ir_imitation
import matplotlib.pyplot as plt
import windows
from scipy.signal import lfilter
import numpy as np


# Parameters of the measuring system

fs = 44100

fstart = 1
fstop = 22050
duration = 1
pad = 4

# Generate excitation signal

excitation = generation.lin_sweep(fstart, fstop, duration, fs)
N = len(excitation)


# Noise in measurement chain

awgn = -30
noise_system = measurement_chain.additive_noise(awgn)

# FIR-Filter-System

f_low = 5000
f_high = 6000
order = 2

bandstop_system = measurement_chain.bandstop(f_low, f_high, fs, order)


# Combinate system elements

system = measurement_chain.chained(bandstop_system, noise_system)

# Lists
beta = 7
fade_in_list = np.arange(0, 1001, 1)
fade_out = 0
t_noise = 0.004

# Spectrum of bandstop for reference

bandstop_f = calculation.butter_bandstop(f_low, f_high, fs, N * 2 + 1, order)


def get_results(fade_in):
    excitation_windowed = excitation * windows.window_kaiser(N,
                                                             fade_in,
                                                             fade_out,
                                                             fs, beta)
    excitation_windowed_zeropadded = generation.zero_padding(
        excitation_windowed, pad, fs)
    system_response = system(excitation_windowed_zeropadded)
    ir = calculation.deconv_process(excitation_windowed_zeropadded,
                                    system_response,
                                    fs)
    return ir


with open("lin_sweep_kaiser_window_script3.txt", "w") as f:
    for fade_in in fade_in_list:
        ir = get_results(fade_in)
        pnr = calculation.pnr_db(ir[0], ir[t_noise * fs:pad * fs])
        spectrum_distance = calculation.vector_distance(
            bandstop_f, np.fft.rfft(ir[:pad * fs]))
        f.write(
            str(fade_in) + " " + str(pnr) +
            " " + str(spectrum_distance) + " \n")
