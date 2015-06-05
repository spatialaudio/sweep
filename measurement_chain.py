from scipy.signal import butter, lfilter, fftconvolve
import numpy as np
from . import generation
from . import calculation


def bandpass(lower_bound, higher_bound, fs, order):
    def inner(data):
        b, a = _butter_bandpass(lower_bound, higher_bound, fs, order)
        return lfilter(b, a, data)
    inner.name = "{}.-order bandpass with lower_bound = {} Hz and higher_bound = {} Hz".format(
        order, lower_bound, higher_bound)
    inner.filename = "bp{}_{}_{}".format(order, lower_bound, higher_bound)
    return inner


def additive_noise(noise_level_db, seed=1):
    def inner(data):
        return data + calculation.awgn_noise(noise_level_db, len(data), seed)
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


def add_gain(gain_level_db):
    def inner(data):
        return 10 ** (gain_level_in_dB / 20) * data
    inner.name = "add {} dB to the signal".format(gain_level_db)
    inner.filename = "addgain{}dB".format(gain_level_db)
    return inner


def moving_average(N):
    # for more information:
    # http://stackoverflow.com/questions/13728392/moving-average-or-running-mean
    def inner(data):
        cumsum = np.cumsum(np.insert(data, 0, 0))
        return (cumsum[N:] - cumsum[:-N]) / N
    inner.name = "moving average filter with {} samples".format(N)
    inner.filename = "maf{}".format(N)
    return inner


def convolution(ir):  # TODO: set string
    def inner(data):
        return fftconvolve(data, ir)[:len(data)]
    inner.name = "{}".format("IR")  # inner.name = string
    inner.filename = "{}".format("IR")
    return inner


def lfilter_new(b, a): # TODO: add to fir-filter
    def inner(data):
        return lfilter(b, a, data)[:len(data)]
    inner.name = "{}".format("IR")  # inner.name = string
    inner.filename = "{}".format("IR")
    return inner


def exponential_decay(duration_seconds,
                      lifetime_seconds,
                      noise_level_db,
                      fs,
                      seed=1):
    t = np.arange(0, duration_seconds, 1 / fs)
    noise = calculation.noise_db(noise_level_db, duration_seconds * fs, seed)
    exponential_fading_noise = noise * np.exp(-t / lifetime_seconds)
    exponential_fading_noise[0] = 1
    return exponential_fading_noise


def diracs(array):
    a = np.asarray(array)
    y = np.zeros(a.max() + 1)
    y[a] = 1
    return y


def bandstop(lower_bound, higher_bound, fs, order):
    b, a = _butter_bandstop(lower_bound, higher_bound, fs, order)
    return b, a


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
    b, a = butter(order, wc, btype='lowpass')
    return b, a


def _butter_bandpass(lower_bound, higher_bound, fs, order):
    wl = lower_bound / (fs / 2)
    wh = higher_bound / (fs / 2)
    b, a = butter(order, [wl, wh], btype='bandpass')
    return b, a


def _butter_bandstop(lower_bound, higher_bound, fs, order):
    wl = lower_bound / (fs / 2)
    wh = higher_bound / (fs / 2)
    b, a = butter(order, [wl, wh], btype='bandstop')
    return b, a
