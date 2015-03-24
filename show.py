import numpy as np
import matplotlib.pyplot as plt


def sweep(x, sweep_time, fs):

    plt.subplots_adjust(hspace=0.4)
    t = np.arange(0, sweep_time, 1 / fs)
    p = 20 * np.log10(abs(np.fft.rfft(x)))
    f = np.linspace(0, fs / 2, len(p))
    plt.figure(1)
    plt.subplot(211)
    plt.plot(t, x)
    plt.grid()
    plt.xlabel('t / s')
    plt.ylabel('x(t)')
    plt.title('time domain')
    plt.subplot(212)
    plt.plot(f, p)
    plt.xscale('log')
    plt.grid()
    plt.xlabel('f / Hz')
    plt.ylabel('A / dB')
    plt.title('frequency domain')
    plt.show()
