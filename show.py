import numpy as np
import matplotlib.pyplot as plt


def sweep(x, sweep_time, fs, domain):
    """You can figure the sweep vector in both the time and frequency
    domains simultaneously or separately, using the 'show' function
    show.sweep(x, sweep_time, fs, domain). For the domain you can select
    between three options:
    tdomain (time domain)
    fdomain (frequency domain)
    tfdomain (in both the time and frequency domains)

    Note that 'sweep_time' and 'fs' have the same values as in
    'generation' function. """

    t = np.arange(0, sweep_time, 1 / fs)
    p = 20 * np.log10(abs(np.fft.rfft(x)))
    f = np.linspace(0, fs / 2, len(p))

    if domain == "tdomain":
        fig, ax1 = plt.subplots()
        ax1.plot(t, x)
        ax1.grid()
        ax1.set_xlabel('t / s')
        ax1.set_ylabel('x(t)')
        ax1.set_title('time domain')
        plt.show()

    elif domain == "fdomain":
        fig, ax2 = plt.subplots()
        ax2.plot(f, p)
        ax2.grid()
        ax2.set_xscale('log')
        ax2.set_xlabel('f / Hz')
        ax2.set_ylabel('A / dB')
        ax2.set_title('frequency domain')
        plt.show()

    elif domain == "tfdomain":
        fig, (ax1, ax2) = plt.subplots(2, 1)
        plt.subplots_adjust(hspace=0.4)
        ax1.plot(t, x)
        ax1.grid()
        ax1.set_xlabel('t / s')
        ax1.set_ylabel('x(t)')
        ax1.set_title('time domain')
        ax2.plot(f, p)
        ax2.grid()
        ax2.set_xscale('log')
        ax2.set_xlabel('f / Hz')
        ax2.set_ylabel('A / dB')
        ax2.set_title('frequency domain')
        plt.show()

    else:
        raise NameError("'%s' is not defined" % domain)
