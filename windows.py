import numpy as np


def window_rectangle(N):
    return ones(N)


def window_poisson(N, fade_in, fade_out, fs, alpha=2):

    L, K, n1, n2, n3 = fade_vector_linspace(N, fade_in, fade_out, fs)

    w1 = np.exp(-alpha * np.abs(n1) / (L / 2.))[:L / 2]
    w2 = np.ones(len(n2))
    w3 = np.exp(-alpha * np.abs(n3) / (K / 2.))[K / 2:K]
    return np.concatenate((w1, w2, w3))


def window_kaiser(N, fade_in, fade_out, fs, beta=3):

    L, M, n_ones = fade_vector_arange(N, fade_in, fade_out, fs)

    w1 = np.kaiser(L, beta)[:L / 2]
    w2 = np.ones(len(n_ones))
    w3 = np.kaiser(M, beta)[M / 2:M]
    return np.concatenate((w1, w2, w3))


def window_bartlett(N, fade_in, fade_out, fs):

    L, M, n_ones = fade_vector_arange(N, fade_in, fade_out, fs)

    w1 = np.bartlett(L)[:L / 2]
    w2 = np.ones(len(n_ones))
    w3 = np.bartlett(M)[M / 2: M]
    return np.concatenate((w1, w2, w3))


def fade_vector_arange(N, fade_in, fade_out, fs):

    L = np.floor(fade_in / 1000 * fs)
    M = np.floor(fade_out / 1000 * fs)
    L = L * 2
    M = M * 2

    n_ones = np.arange(L / 2, N - M / 2)
    return L, M, n_ones


def fade_vector_linspace(N, fade_in, fade_out, fs):

    L = np.floor(fade_in / 1000 * fs)
    K = np.floor(fade_out / 1000 * fs)
    L = L * 2
    K = K * 2
    n1 = np.linspace(-L / 2., (L) / 2., L)
    n2 = np.arange(L / 2, N - K / 2)
    n3 = np.linspace(-K / 2., (K) / 2., K)
    return L, K, n1, n2, n3
