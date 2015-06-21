from scipy.signal import butter, lfilter, fftconvolve
import numpy as np
import generation
import calculation


def bandpass(lower_bound, higher_bound, fs, order):
    def inner(data):
        b, a = _butter_bandpass(lower_bound, higher_bound, fs, order)
        return lfilter(b, a, data)
    inner.name = "{}.-order bandpass with f_L = {} Hz, f_H = {} Hz".format(
                 order, lower_bound, higher_bound)
    inner.filename = "bp{}_{}_{}".format(order, lower_bound, higher_bound)
    return inner


def bandstop(lower_bound, higher_bound, fs, order):
    def inner(data):
        b, a = _butter_bandstop(lower_bound, higher_bound, fs, order)
        return lfilter(b, a, data)
    inner.name = "{}.-order bandstop with f_L = {} Hz, f_H = {} Hz".format(
                 order, lower_bound, higher_bound)
    inner.filename = "bs{}_{}_{}".format(order, lower_bound, higher_bound)
    return inner


def additive_noise(noise_level_db, seed=1):
    def inner(data):
        return data + calculation.awgn_noise(noise_level_db, len(data), seed)
    inner.name = "additive noise with {} dB noise level".format(
        noise_level_db)
    inner.filename = "{}noise".format(noise_level_db)
    return inner


def lowpass(cutoff, fs, order):
    def inner(data):
        b, a = _butter_lowpass(cutoff, fs, order=order)
        return lfilter(b, a, data)
    inner.name = "lowpass-filter with fc = {} and {}.order".format(
        cutoff, order)
    inner.filename = "lpf_fc{}_order{} ".format(cutoff, order)
    return inner


def highpass(cutoff, fs, order):
    def inner(data):
        b, a = _butter_highpass(cutoff, fs, order=order)
        return lfilter(b, a, data)
    inner.name = "high-filter with fc = {} and {}.order".format(
        cutoff, order)
    inner.filename = "hpf_fc{}_order{} ".format(cutoff, order)
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


def convolution(ir):
    def inner(data):
        return fftconvolve(data, ir)[:len(data)]
    inner.name = "{}".format("IR")
    inner.filename = "{}".format("IR")
    return inner


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


def _butter_highpass(cutoff, fs, order):
    wc = cutoff / (fs / 2)
    b, a = butter(order, wc, btype='highpass')
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
