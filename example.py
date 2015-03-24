import generation
import show

""" Choose the excitation signal which you want to generate and fill in
the parameters xxx_sweep(fstart, fstop, sweep_time, fs),
where:

fstart is the start frequency
fstop  is the stop frequency
sweep_time is the total length of sweep
fs is the sampling frequency

Note that the stop frequency must not be greater than half the
sampling frequency (Nyquist-Shannon sampling theorem)

Save the return value in a new variable which is the sweep vector.
"""
# For example

x = generation.log_sweep(1, 1000, 2, 44100)

"""We created a vector which sweeps from 1 Hz to 1000 Hz in 2
seconds at a sampling frequency of 44.1 kHz and save the vector in x.
Now it is possible to figure the sweep vector in both the time and
frequency domain simultaneously, using the 'show' function:
show.sweep(x, sweep_time, fs).
Note that 'sweep_time' and 'fs' have the same values as in
'generation' function. """

# For example

show.sweep(x, 2, 44100)
