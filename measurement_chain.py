from scipy.signal import butter, lfilter, fftconvolve
import numpy as np
import generation
import calculation


# superior DUT begin


def bandpass(lower_bound, higher_bound, fs, order):
    def inner(data):
        b, a = _butter_bandpass(lower_bound, higher_bound, fs, order)
        return lfilter(b, a, data)
    inner.name = "{}.-order bandpass with lower_bound = {} Hz and higher_bound = {} Hz".format(
        order, lower_bound, higher_bound)
    inner.filename = "bp{}_{}_{}".format(order, lower_bound, higher_bound)
    return inner


def additive_noise(noise_level_db, seed=None):
    def inner(data):
        return data + calculation.noise_db(noise_level_db, len(data), seed)
    inner.name = "additive noise with {} dB noise level".format(
        noise_level_db)
    inner.filename = "{}noise".format(noise_level_db)
    return inner


def anti_aliasing_filter(cutoff, fs, order):
    def inner(data):
        b, a = _butter_lowpass(cutoff, fs, order=order)
        return lfilter(b, a, data)
    inner.name = "anti-aliasing filter with fc = {} and {}.order".format(
        cutoff, order)
    inner.filename = "aaf_fc{}_order{} ".format(cutoff, order)
    return inner


def add_gain(gain_level_dB):
    def inner(data):
        return 10 ** (gain_level_in_dB / 20) * data
    inner.name = "add {} dB to the signal".format(gain_level_dB)
    inner.filename = "addgain{}dB".format(gain_level_dB)
    return inner


# subordinate DUT begin

def moving_average(N):
    # for more information:
    # http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    def inner(data):
        cumsum = np.cumsum(np.insert(data, 0, 0))
        return (cumsum[N:] - cumsum[:-N]) / N
    inner.name = "moving average filter with {} samples".format(N)
    inner.filename = "maf{}".format(N)
    return inner


def take_ir(ir):  # string übergeben
    def inner(data):
        return fftconvolve(data, ir)[:len(data)]
    inner.name = "{}".format("IR")  # inner.name = string
    inner.filename = "{}".format("IR")
    return inner

# subordinate DUT end


# superior DUT end


# generate some impulse responses begin

def exponential_decay(
    duration_seconds,
     lifetime_seconds,
     noise_level_db,
     fs,
     seed=1):
    t = np.arange(0, duration_seconds, 1 / fs)
    noise = calculation.noise_db(noise_level_db, duration_seconds * fs, seed)
    exponential_fading_noise = noise * np.exp(-t / lifetime_seconds)
    exponential_fading_noise[0] = 1
    return exponential_fading_noise


def diracs(duration_seconds, dirac_positions_array, fs):
    h = np.zeros(duration_seconds * fs)
    for i in dirac_positions_array:
        h[i] = 1
    return h

# generate some impulse responses end

# Help functions


def chained(*systems):
    def inner(arg):
        for system in systems:
            arg = system(arg)
        return arg
    inner.name = " and ".join([x.name for x in systems])
    return inner


def _butter_lowpass(cutoff, fs, order):
    wc = cutoff / (fs / 2)
    b, a = butter(order, wc, btype='low')
    return b, a


def _butter_bandpass(lower_bound, higher_bound, fs, order):
    wl = lower_bound / (fs / 2)
    wh = higher_bound / (fs / 2)
    b, a = butter(order, [wl, wh], btype='band')
    return b, a
