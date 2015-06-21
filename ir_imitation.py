""" Imitate a impulse response."""
import numpy as np
import measurement_chain
import calculation


def exponential_decay(duration_seconds,
                      db_decay,
                      noise_level_db,
                      fs,
                      seed=1):
    """ Imitate real IR.
    duration_seconds : IR duration
    db_decay : dB / sec
    noise_level: dB

    """
    t = np.arange(0, duration_seconds, 1 / fs)
    noise = calculation.awgn_noise(noise_level_db, duration_seconds * fs, seed)
    decay = 10 ** ((noise_level_db + db_decay) / 20)
    noise_level = 10 ** (noise_level_db / 20)
    lifetime = -1 / (np.log(decay / noise_level))
    exponential_fading_noise = noise * np.exp(-t / lifetime)
    exponential_fading_noise[0] = 1
    return exponential_fading_noise


def diracs(array):
    """Dirac-Array.

    """
    a = np.asarray(array)
    y = np.zeros(a.max() + 1)
    y[a] = 1
    return y


def bandstop(lower_bound, higher_bound, fs, order):
    b, a = measurement_chain._butter_bandstop(lower_bound,
                                              higher_bound,
                                              fs, order)
    return b, a
