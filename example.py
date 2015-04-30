#!/usr/bin/env python3
"""A list of examples."""

import generation
import plotting
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.mlab as ml
import calculation


x = generation.log_sweep(1, 20050, 1, 44100)

# We created a vector which sweeps from 1 Hz to 1000 Hz in 1
# second at a sampling frequency of 44.1 kHz. Now you can plot it
# in several domains.


#~ ax = plotting.plot_freq(
     #~ x,
     #~ fs=44100,
     #~ scale='dB',
     #~ side='onesided',
     #~ mode='magnitude')
# ~ ax.set_xscale('log')  # if side = 'twosided' you have to disable this line
#~ plt.show()


# Test functions for response and snr calculations.

y = generation.log_sweep(1, 22050, 1, 44100)
noise = np.random.normal(0, 0.3, len(y))
noisy_signal = y + noise  # a random system response

z = calculation.deconv_process(x, noisy_signal, 44100)
# print(calculation.snr_db(x,x))
ax = plotting.plot_freq(
    z,
     fs=44100,
     scale='dB',
     side='onesided',
     mode='magnitude')
ax.set_xscale('log')
plt.show()
