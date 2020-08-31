#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He
# email: 1910646@tongji.edu.cn

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Solve the problem of not displaying plot
import matplotlib
matplotlib.use('TkAgg')
import warnings
warnings.filterwarnings("ignore")
import sys
sys.path.append("original_data")

from Signal_Tool_utils import *
from IIR_utils import *

plt.style.use(['science','no-latex'])

df_data = pd.read_table('/Volumes/SSDIrving/AAAArobotics_rivingHe/IrvingHeRoboticsRepo/Signal_Propressing/Wavelets小波变换/original_data/set3(9).txt',header=None)

# add columns name
df_data.columns = ['time','data']

Time = df_data['time']
Signal = df_data['data']

# get key params
# 1. sample freq
Fs = 1/(Time[2]-Time[1])
print("Sample Frequency:",int(Fs),"HZ")

# 2. Spectrum (频谱)
fft,freq = FFT(Fs,Signal)
# ----------------------------------
# visual block
plt.figure(figsize=(10,6))
plt.subplot(211) # time-domain
plt.xlabel("Time/s")
plt.ylabel("Acc/g")
plt.plot(Time,Signal,'k-')

plt.subplot(212) # time-domain
plt.xlabel("Freq/hz")
plt.ylabel("Power")
plt.plot(freq,fft,'b-')
plt.show()
# -----------------------------------

# 3. Filter for 50hz noise
FilterMains = IIR2Filter(
    order=4,
    cutoff=[48, 52],
    filterType='bandpass',  # 带阻
    design='butter',  # butterworth
    # rp=0.001,
    fs=Fs
)
FilterSignal = np.zeros((Signal.shape))
for i in range(len(Signal)):
    FilterSignal[i] = FilterMains.filter(Signal[i])

plt.figure(figsize=(10,6))
plt.subplot(211) # time-domain
plt.xlabel("Time/s")
plt.ylabel("Acc/g")
plt.plot(Time,Signal,'k-',label='before filter')
plt.plot(Time,FilterSignal,'r-',label='after filter')

plt.subplot(212)

# plt.show()

# pre-processing


