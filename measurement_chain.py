from scipy.signal import butter, lfilter, fftconvolve
import numpy as np


# superior DUT begin


def bandpass(lower_bound, higher_bound, fs, order):
    def dummy(data):
        b, a = _butter_bandpass(lower_bound, higher_bound, fs, order)
        return lfilter(b, a, data)
    dummy.name = "{}.-order bandpass with lower_bound = {} Hz and higher_bound = {} Hz".format(
        order, lower_bound, higher_bound)
    dummy.filename = "bp{}_{}_{}".format(order, lower_bound, higher_bound)
    return dummy


def additive_noise(standard_deviation, seed):
    def dummy(data):
        np.random.seed(seed)
        return data + np.random.normal(0, standard_deviation, len(data))
    dummy.name = "additive noise with {} standard deviation".format(
        standard_deviation)
    dummy.filename = "{}noise".format(standard_deviation)
    return dummy


def anti_aliasing_filter(cutoff, fs, order):
    def dummy(data):
        b, a = _butter_lowpass(cutoff, fs, order=order)
        return lfilter(b, a, data)
    dummy.name = "anti-aliasing filter with fc = {} and {}.order".format(
        cutoff, order)
    dummy.filename = "aaf_fc{}_order{} ".format(cutoff, order)
    return dummy


def add_gain(gain_level_dB):
    def dummy(data):
        return 10 ** (gain_level_in_dB / 20) * data
    dummy.name = "add {} dB to the signal".format(gain_level_dB)
    dummy.filename = "addgain{}dB".format(gain_level_dB)
    return dummy


# subordinate DUT begin

def diracs(dirac_positions_array):
    def dummy(data):
        h = np.zeros(len(data))
        for i in dirac_positions_array:
            h[i] = 1
        return fftconvolve(data, h)[:len(data)]
    dummy.name = "dirac-filter positions:{}".format(dirac_positions_array)
    dummy.filename = "dirac{}".format(dirac_positions_array)
    return dummy


def moving_average(N):
    # for more information:
    # http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    def dummy(data):
        cumsum = np.cumsum(np.insert(data, 0, 0))
        return (cumsum[N:] - cumsum[:-N]) / N
    dummy.name = "moving average filter with {} samples".format(N)
    dummy.filename = "maf{}".format(N)
    return dummy


def exponential_decay(standard_deviation, lifetime, seed):
    def dummy(data):
        t = np.arange(len(data)) / len(data)
        np.random.seed(seed)
        noise = np.random.normal(0, standard_deviation, len(data))
        exponential_fading_noise = noise * np.exp(-t / lifetime)
        exponential_fading_noise[0] = 1
        return fftconvolve(data, exponential_fading_noise)[:len(data)]
    dummy.name = "exponential decay with {} standard deviation and {} lifetime".format(
        standard_deviation, lifetime)
    dummy.filename = "exponential_decay_{}sd_{}lt".format(
        standard_deviation, lifetime)
    return dummy

# subordinate DUT end


# superior DUT end


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
