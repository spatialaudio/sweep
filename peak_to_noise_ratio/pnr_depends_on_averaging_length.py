import sys
sys.path.append('..')

import calculation
import random
import plotting
import generation
import ir_imitation
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np


# IR parameters
fs = 44100
ir_duration = 2
ir_noise_level = -15
ir_db_decay = -200

# AWGN
awgn = -50

t = calculation.start_time_noise_floor(ir_noise_level, ir_db_decay, awgn)

acc = 0
ir_array = []

mean_length_list = np.arange(1, 101)

for i in range(1, max(mean_length_list) + 1):
    ir = ir_imitation.exponential_decay(ir_duration, ir_db_decay,
                                        ir_noise_level, fs, seed=i)
    ir_awgn = ir + calculation.awgn_noise(awgn, len(ir), seed=i)
    acc += ir_awgn
    if i in mean_length_list:
        ir_array.append(acc/i)

pnr_array = []


for i in range(len(mean_length_list)):
    pnr_array.append(calculation.peak_to_noise_ratio(ir_array[i], t*fs, fs))


plt.plot(mean_length_list, pnr_array)
plt.ticklabel_format(useOffset=False)
plt.title('SNR depends on Averaging Length')
plt.xlabel('Averaging Length')
plt.ylabel('PNR / dB')
plt.grid(True)
plt.savefig('pnr_depends_on_averaging_length.png')
