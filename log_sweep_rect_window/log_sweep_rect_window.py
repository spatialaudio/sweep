#!/usr/bin/env python3

"""On the influence of windowing of sweep signals.

"""

# Parameters of the measuring system

fs = 44100

fstart = 1
fstop = 22050
duration = 1
pad = 4

import sys
sys.path.append('..')

import measurement_chain
import plotting
import calculation
import generation
import numpy as np
import matplotlib.pyplot as plt
import windows
from scipy.signal import lfilter

excitation = generation.log_sweep(fstart, fstop, duration, fs)
N = len(excitation)
excitation_zeropadded = generation.zero_padding(excitation, pad, fs)

# Noise in measurement chain

noise_level_db = -20.
noise = measurement_chain.additive_noise(noise_level_db)

# FIR-Filter

ir = measurement_chain.convolution([1.0])


def get_results(system):

    print("Processing {}".format(system.name))

    system_response = system(excitation_zeropadded)

    ir = calculation.deconv_process(excitation_zeropadded, system_response, fs)

    return calculation.snr_db(ir[0], ir[1:4 * fs])


f = open("log_sweep_rect_window.txt", "w")

plotting.plot_time(
    np.correlate(excitation,
                 excitation,
                 'full'),
     scale='dB',
     title="Rect-windowed log_sweep")
plt.savefig("akf_fig.png")
plt.close()
# plt.show()

snr = get_results(measurement_chain.chained(ir, noise))
f.write("SNR: " + str(snr) + " dB \n")
