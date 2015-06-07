#!/usr/bin/env python3

"""The influence of windowing of sweep signals when using a
   Kaiser Window.

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

fstart = 1
fstop = 22050
duration = 1
pad = 4

# Generate excitation signal

excitation = generation.log_sweep(fstart, fstop, duration, fs)
N = len(excitation)


# Noise in measurement chain

noise_level_db = -20.
noise = measurement_chain.additive_noise(noise_level_db)

# FIR-Filter-System

dirac_system = measurement_chain.convolution([1.0])

# Combinate system elements

system = measurement_chain.chained(dirac_system, noise)

# Lists
fade_in_list = [1, 2, 20, 50]
fade_out_list = [1, 2, 10, 600]
beta_list = [2, 4, 12]


def get_results(fade_in, fade_out, beta):
    excitation_windowed = excitation * windows.window_kaiser(N,
                                                             fade_in,
                                                             fade_out,
                                                             fs, beta)
    akf = np.correlate(excitation_windowed, excitation_windowed, 'full')
    excitation_windowed_zeropadded = generation.zero_padding(
        excitation_windowed, pad, fs)
    system_response = system(excitation_windowed_zeropadded)
    ir = calculation.deconv_process(excitation_windowed_zeropadded,
                                    system_response,
                                    fs)
    return calculation.snr_db(ir[0], ir[1:4 * fs]), akf.max()


with open("log_sweep_kaiser_window_script1.txt", "w") as f:
    for beta in beta_list:
        for fade_in in fade_in_list:
            for fade_out in fade_out_list:
                snr, akf_max = get_results(fade_in, fade_out, beta)
                f.write("Beta: " + str(beta) + " Fade_in(ms): " +
                        str(fade_in) + " Fade_out(ms): " +
                        str(fade_out) + " AKF_max(dB): " +
                        str(plotting._db_calculation(akf_max)) +
                        " SNR(dB): " + str(snr) + " \n")
