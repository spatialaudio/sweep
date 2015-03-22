*Warning*: Repository is work in progress! 

This repository deals with the generation of a simulation environment for room impulse response measurements. 
It contains a measuring chain which simulates parameters occuring in reality (microphone, preamp, DAC, ...).
It will be considered only linear time-invariant systems (LTI). The user can choose between different parameters (type
of exication signals, length of signal, type of windowing, intensity and type of noise, sampling frequency, ...), which exicate the fictitous "Device Under Test" (DUT). As output the tool returns impulse response, frequency response, power spectral density and signal quality by mathematical functions (FFT, deconvolution, averaging, ...). Thus, results can
be validated by known analytical LTI systems. 
