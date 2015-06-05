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
import windows
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import lfilter

excitation = generation.log_sweep(fstart, fstop, duration, fs)
N = len(excitation)


# Noise in measurement chain

noise_level_db = -20.
noise = measurement_chain.additive_noise(noise_level_db)

# FIR-Filter

ir = measurement_chain.convolution([1.0])


def get_results(system, excitation_windowed_zeropadded):

    print("Processing {}".format(system.name))

    system_response = system(excitation_windowed_zeropadded)

    ir = calculation.deconv_process(
        excitation_windowed_zeropadded,
        system_response,
        fs)

    return calculation.snr_db(ir[0], ir[1:4 * fs])


fade_in_list = [1, 2, 20, 50]
fade_out_list = [1, 2, 10, 600]
beta_list = [2, 4, 12]
i = 1

f = open("log_sweep_kaiser_window_script1.txt", "w")
for beta in beta_list:
    for fade_in in fade_in_list:
        for fade_out in fade_out_list:
            excitation_windowed = excitation * \
                windows.window_kaiser(N, fade_in, fade_out, fs, beta)
            akf = np.correlate(
                excitation_windowed,
                excitation_windowed,
                'full')
            plotting.plot_time(
                akf,
                scale='dB',
                title="Fade-in:{}, Fade-out:{}, Beta:{}".format(
                    fade_in,
                    fade_out,
                    beta))
            plt.savefig("akf_fig{}.png".format(i))
            plt.close()
            i += 1
            excitation_windowed_zeropadded = generation.zero_padding(
                excitation_windowed, pad, fs)
            snr = get_results(
                measurement_chain.chained(ir,
                                          noise),
                excitation_windowed_zeropadded)
            f.write(
                "Beta: " + str(
                    beta) + " Fade_in (ms): " + str(
                        fade_in) + " Fade_out (ms): " + str(
                            fade_out) + " AKF_max (dB): " + str(
                    plotting._db_calculation(
                        akf.max(
                        ))) + " SNR: " + str(
                                snr) + " dB \n")
