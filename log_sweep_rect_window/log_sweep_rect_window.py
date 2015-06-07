#!/usr/bin/env python3

"""The influence of windowing of sweep signals when using a
   Rect Window.

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


def get_results():
    akf = np.correlate(excitation, excitation, 'full')
    plotting.plot_time(akf,
                       scale='db',
                       title='AKF log. Sweep with Rect Window')
    plt.savefig('akf_log_sweep_rect.png')
    plt.close()
    excitation_zeropadded = generation.zero_padding(
        excitation, pad, fs)
    system_response = system(excitation_zeropadded)
    ir = calculation.deconv_process(excitation_zeropadded,
                                    system_response,
                                    fs)
    return calculation.snr_db(ir[0], ir[1:4 * fs]), akf.max()


with open("log_sweep_rect_window.txt", "w") as f:
    snr, akf_max = get_results()
    f.write("AKF_max(dB): " +
            str(plotting._db_calculation(akf_max)) +
            " SNR(dB): " + str(snr) + " \n")
