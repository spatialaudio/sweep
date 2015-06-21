#!/usr/bin/env python3

"""The influence of excitation length.

"""


import sys
sys.path.append('..')

import measurement_chain
import plotting
import calculation
import ir_imitation
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
pad = 4

duration_list = np.arange(1, 50, 1)

# Noise in measurement chain

noise_level_db = -13.5
noise = measurement_chain.additive_noise(noise_level_db)

# FIR-Filter-System

dirac_system = measurement_chain.convolution([1.0])

# Combinate system elements

system = measurement_chain.chained(dirac_system, noise)


def get_results(duration):
    excitation = generation.log_sweep(fstart, fstop, duration, fs)
    excitation_zeropadded = generation.zero_padding(excitation,
                                                    duration + pad, fs)
    system_response = system(excitation_zeropadded)
    ir = calculation.deconv_process(excitation_zeropadded,
                                    system_response,
                                    fs)
    return ir

pnr_array = []

with open("pnr_depends_on_excitation_length.txt", "w") as f:
    for duration in duration_list:
        ir = get_results(duration)
        pnr = calculation.pnr_db(ir[0], ir[1:4 * fs])
        pnr_array.append(pnr)
        f.write(
            str(duration) + " " + str(pnr) + " \n")

plt.plot(duration_list, pnr_array)
plt.ticklabel_format(useOffset=False)
plt.title('PNR depends on Averaging Length')
plt.xlabel('Duration Length / s')
plt.ylabel('PNR / dB')
plt.grid(True)
xticks = [1, 10, 20, 30, 40, 50]
plt.xticks(xticks)
plt.xlim([1, 50])
plt.savefig('pnr_depends_on_averaging_length')
