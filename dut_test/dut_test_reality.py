#!/usr/bin/env python3

"""Software-Test with a known IR in real-life conditions.
h[k] = dirac[k] + dirac[k-1050]
"""

import sys
sys.path.append('..')

import matplotlib.pyplot as plt
import numpy as np
import generation
import plotting
import calculation
import measurement_chain
import ir_imitation


fs = 44100

fstart = 1
fstop = 22050
pad = 7


# Noise in measurement chain

noise_level_db = -50.
noise = measurement_chain.additive_noise(noise_level_db)

# FIR-Filter-System

dirac_system = measurement_chain.convolution(ir_imitation. diracs([0, 1050]))

# Combinate system elements

system = measurement_chain.chained(dirac_system, noise)


excitation = np.zeros(44100)
excitation[0] = 1
excitation_zeropadded = generation.zero_padding(excitation, pad, fs)


system_response = system(excitation_zeropadded)

h = calculation.deconv_process(excitation,
                               system_response, fs)[:len(excitation)]

# Plot impulse response

plotting.plot_time(h, title='')
plt.xlim(-1000, fs)
plt.savefig('impulse_response_reality.png')
plt.close()

# Plot frequency response

plotting.plot_freq(h, fs, scale='db', title='')
plt.xscale('log')
plt.savefig('frequency_response_reality.png')
plt.close()

# Plot phase response

plotting.plot_freq(h, fs, mode='phase', title='')
plt.xscale('log')
plt.savefig('phase_response_reality.png')
plt.close()
