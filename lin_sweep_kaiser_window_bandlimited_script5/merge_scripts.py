#!/usr/bin/env python3
""" Script to merge scripts"""

import numpy as np
import matplotlib.pyplot as plt

script5 = np.genfromtxt('lin_sweep_kaiser_window_bandlimited_script5.txt')

script5_1 = np.genfromtxt('lin_sweep_kaiser_window_bandlimited_script5_1.txt')

fade_in_list = script5[:, 0]

# Script5

pnr_list = script5[:, 1]
spectrum_distance_list = script5[:, 2]

# Script5_1 (unwindowed deconvolution)

pnr_unwindowed_deconvolution_list = script5_1[:, 1]
spectrum_distance_unwindowed_deconvolution_list = script5_1[:, 2]


plt.plot(fade_in_list, pnr_list, label='Deconvolution: Excitation windowed')

plt.plot(
    fade_in_list,
     pnr_unwindowed_deconvolution_list,
     label='Deconvolution: Excitation unwindowed')
plt.grid()
plt.title('Peak to noise ratio depending on Fade in')
plt.xlabel('Fade in / ms')
plt.ylabel('Peak to noise ratio / dB')
plt.ticklabel_format(useOffset=False)
plt.legend(loc='lower left')
plt.xlim([-10, 1000])
plt.savefig('pnr.png')
plt.close()


NFFT_dirac = 88201
max_measurement = 5974410.59739

plt.plot(fade_in_list, -10 * np.log10(1 / NFFT_dirac *
         np.asarray(spectrum_distance_list) / max_measurement), label='Deconvolution: Excitation windowed')

plt.plot(fade_in_list,
         -10 * np.log10(1 / NFFT_dirac * np.asarray(spectrum_distance_unwindowed_deconvolution_list) /
                        max_measurement), label='Deconvolution: Excitation unwindowed')


plt.grid()
plt.title('Spectrum Distance depending on Fade in')
plt.xlabel('Fade in / ms')
plt.ylabel('(Spectrum Distance / max(Spectrum Distance)) / dB')
plt.ticklabel_format(useOffset=False)
plt.legend(loc='lower right')
plt.xlim([-10, 1000])
plt.savefig('spectral_distance.png')
