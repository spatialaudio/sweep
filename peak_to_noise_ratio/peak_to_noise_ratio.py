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

ir = ir_imitation.exponential_decay(ir_duration, ir_db_decay,
                                    ir_noise_level, fs, seed=1)
ir_awgn = ir + calculation.awgn_noise(awgn, len(ir), seed=1)


plotting.plot_time(ir, fs)
plt.xlim([-0.02, 2])
plt.savefig('ir.png')
plt.close()


plotting.plot_time(ir, fs, scale='db')
plt.xlim([-0.02, 2])
plt.savefig('ir_db.png')
plt.close()


plotting.plot_time(ir_awgn, fs)
plt.xlim([-0.02, 2])
plt.savefig('ir_awgn.png')
plt.close()


plotting.plot_time(ir_awgn, fs, scale='db')
plt.xlim([-0.02, 2])
plt.savefig('ir_awgn_db.png')
plt.close()


pnr = calculation.peak_to_noise_ratio(ir_awgn, t*fs, fs)
print(pnr)
