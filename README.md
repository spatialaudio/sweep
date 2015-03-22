*Warning*: Repository is work in progress! 

This repository deals with the generation of a simulation environment for room impulse response measurements. 
It contains a measuring chain, which simulates parameters occurring in reality (microphone, preamp, DAC, ...).
Here, we consider only lineare time-invariant systems (LTI). The user can choose between different parameters (type
of excitation signals, length of signal, type of windowing, intensity and type of noise, sampling frequency, ...), which excite the fictitous "Device Under Test" (DUT). As output the tool returns impulse response, frequency response, power spectral density and signal quality by mathematical functions (FFT, deconvolution, averaging, ...). Thus, results can
be validated by known analytical LTI systems. The software environment will be programmed in Python3 by using packages 
for scientific computing, e.g. numpy.
