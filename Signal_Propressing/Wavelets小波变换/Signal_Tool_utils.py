#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He
# email: 1910646@tongji.edu.cn

import numpy as np
from scipy.fftpack import fft,rfft,fftshift,ifft
from scipy.fftpack import fftfreq

# Spectrum
def FFT(Fs,signal):
    # rfft对实时信号进行fft
    iSampleCounts = signal.shape[0] # 采样点数
    xFFT = np.abs(np.fft.rfft(signal)/iSampleCounts)
    xFreqs = np.linspace(0,Fs/2,int(iSampleCounts/2)+1)
    return xFFT,xFreqs

# ButterStop_for 50hz 工频
def butterBandStopFilter(signal,lowcut, highcut, samplerate, order):
    "生成巴特沃斯带阻滤波器"
    semiSampleRate = samplerate*0.5
    low = lowcut / semiSampleRate
    high = highcut / semiSampleRate
    b,a = signal.butter(order,[low,high],btype='bandstop')
    print("bandstop:","b.shape:",b.shape,"a.shape:",a.shape,"order=",order)
    print("b=",b)
    print("a=",a)
    return b,a

# wavelet
import pywt


def fft_func(signal,sample_points=None):
    if sample_points is None:
        fft_signal = fft(signal)
    else:
        fft_signal = fft(signal,sample_points)
    fft_signal = fftshift(fft_signal)
    fft_signal = fft_signal[fft_signal.size//2:] # postive部分
    return fft_signal