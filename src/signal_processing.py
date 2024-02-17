import numpy as np
from scipy import signal
import matplotlib.pyplot as plt


def get_analytic_signal(data, fs):

    analytic_signal = signal.hilbert(data, axis = 0)
    amplitude_envelope = np.abs(analytic_signal)
    instantaneous_phase = np.unwrap(np.angle(analytic_signal))
    instantaneous_frequency = (np.diff(instantaneous_phase) /
                            (2.0*np.pi) * (fs))
    
    return analytic_signal, amplitude_envelope, instantaneous_frequency


def apply_bandpass_filter(samples, lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    sos = signal.butter(order, [low, high], btype='band', analog=False, output='sos')
    return signal.sosfiltfilt(sos, samples, axis=0)

def preprocess(samples, ds=50, low_pass_cutoff=100, fs=25000, filter_order=5):
    samples = apply_butter_lowpass_filter(samples, cutoff=low_pass_cutoff, fs=fs, order=filter_order)
    samples = downsample(samples, ds)
    samples = demean(samples)
    return samples

def demean(samples):
    return samples - np.mean(samples, axis=0)

def downsample(samples, factor):
    if samples.ndim == 1:
        return samples[::factor]

    return samples[::factor, :]

def apply_butter_lowpass_filter(samples, cutoff, fs, order=5):
    nyq = 0.5 * fs 
    normalized_cutoff = cutoff / nyq
    sos = signal.butter(order, cutoff, fs=fs, btype='low', analog=False, output='sos')
    return signal.sosfiltfilt(sos, samples, axis=0)

def apply_moving_average_filter(samples, N):
    return np.convolve(samples, np.ones(N)/N, mode='same')



def get_fft(samples,fs, norm=True):
    n = samples.shape[0]
    bins = np.fft.fftfreq(n, 1/(fs))
    lfp_fft = np.fft.fft(samples, axis = 0)
    lfp_magnitude = np.abs(lfp_fft)
    lfp_power = np.abs(lfp_fft)**2

    if not norm:
        return bins, lfp_power
    
    return bins, lfp_power / n**2
