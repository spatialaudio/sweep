#!/usr/bin/env python3
""" Script to merge scripts"""

import numpy as np
import matplotlib.pyplot as plt

script2 = np.genfromtxt(
    'lin_sweep_kaiser_window_script2.txt')

script2_1 = np.genfromtxt(
    'lin_sweep_kaiser_window_script2_1.txt')

fade_out_list = script2[:, 0]

# Script2

pnr_list = script2[:, 1]
spectrum_distance_list = script2[:, 2]

# Script2_1 (unwindowed deconvolution)

pnr_unwindowed_deconvolution_list = script2_1[:, 1]
spectrum_distance_unwindowed_deconvolution_list = script2_1[:, 2]


plt.plot(fade_out_list, pnr_list, label='Deconvolution: Excitation windowed')

plt.plot(
    fade_out_list,
    pnr_unwindowed_deconvolution_list,
    label='Deconvolution: Excitation unwindowed')
plt.grid()
plt.title('Peak to noise ratio depending on Fade out')
plt.xlabel('Fade out / ms')
plt.ylabel('Peak to noise ratio / dB')
plt.ticklabel_format(useOffset=False)
plt.legend(loc='upper right')
plt.xlim([-10, 1000])
plt.savefig('pnr.png')
plt.close()


NFFT_dirac = 88201
max_measurement = 6.79601317575

plt.plot(fade_out_list, -10 * np.log10(1 / NFFT_dirac *
         np.asarray(spectrum_distance_list) / max_measurement), label='Deconvolution: Excitation windowed')

plt.plot(fade_out_list,
         -10 * np.log10(1 / NFFT_dirac * np.asarray(spectrum_distance_unwindowed_deconvolution_list) /
                        max_measurement), label='Deconvolution: Excitation unwindowed')


plt.grid()
plt.title('Spectrum Distance depending on Fade in')
plt.xlabel('Fade out / ms')
plt.ylabel('(Spectrum Distance / max(Spectrum Distance)) / dB')
plt.ticklabel_format(useOffset=False)
plt.legend(loc='upper right')
plt.savefig('spectral_distance.png')
