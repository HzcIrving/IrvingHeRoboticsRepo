#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

import numpy as np
import matplotlib.pyplot as plt
import pywt
import pywt.data

ecg = pywt.data.ecg()
plt.plot(ecg)
plt.show()

mode = pywt.Modes.smooth

def plot_signal_decomp(data,w,title):
    """
    分解并可视化
    S = An + Dn + Dn-1 + ... + D1
    """
    w = pywt.Wavelet(w)
    a = data
    ca = []
    cd = []
    for i in range(5):
        (a,d) = pywt.dwt(a,w,mode)
        ca.append(a)
        cd.append(d)

    rec_a = []
    rec_d = []

    for i,coeff in enumerate(ca):
        coeff_list = [coeff,None]+[None]*i
        rec_a.append(pywt.waverec(coeff_list,w))

    for i, coeff in enumerate(cd):
        coeff_list = [None, coeff] + [None] * i
        rec_d.append(pywt.waverec(coeff_list, w))

    fig = plt.figure()
    ax_main = fig.add_subplot(len(rec_a) + 1, 1, 1)
    ax_main.set_title(title)
    ax_main.plot(data)
    ax_main.set_xlim(0, len(data) - 1)

    for i, y in enumerate(rec_a):
        ax = fig.add_subplot(len(rec_a) + 1, 2, 3 + i * 2)
        ax.plot(y, 'r')
        ax.set_xlim(0, len(y) - 1)
        ax.set_ylabel("A%d" % (i + 1))

    for i, y in enumerate(rec_d):
        ax = fig.add_subplot(len(rec_d) + 1, 2, 4 + i * 2)
        ax.plot(y, 'g')
        ax.set_xlim(0, len(y) - 1)
        ax.set_ylabel("D%d" % (i + 1))


if __name__ == "__main__":
    plot_signal_decomp(ecg, 'sym5', "DWT: Ecg sample - Symmlets5")
    plt.show()


