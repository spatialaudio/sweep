#!/usr/bin/env python3

"""Software-Test with a known IR.
h[k] = dirac[k] + dirac[k-1050]
Please note: For Frequency Response is scaling to 2 / len(signal)
             before FFT invalid
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


# Parameters of the measuring system

fs = 44100

fstart = 1
fstop = 22050
pad = 7


# Excitation signal

excitation = np.zeros(44100)
excitation[0] = 1
excitation_zeropadded = generation.zero_padding(excitation, pad, fs)


system_response = measurement_chain.convolution(ir_imitation.diracs([0, 1050]))(excitation_zeropadded)

h = calculation.deconv_process(excitation,
                               system_response, fs)[:len(excitation)]


# Plot impulse response

plotting.plot_time(h)
plt.xlim(-500, 10000)
plt.xticks([0, 1050, 2000, 4000, 6000, 8000, 10000])
plt.savefig('impulse_response.png')
plt.close()

# Plot frequency response

plotting.plot_freq(h, fs, scale='db', title=' ')
plt.xscale('log')
plt.xlim(1, 23000)
plt.savefig('frequency_response.png')
plt.close()

# Plot phase response

plotting.plot_freq(h, fs, mode='phase', title=' ')
plt.xscale('log')
plt.savefig('phase_response.png')
plt.close()
