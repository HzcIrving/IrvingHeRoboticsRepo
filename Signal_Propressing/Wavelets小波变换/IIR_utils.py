#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He
# email: 1910646@tongji.edu.cn

"""
数字滤波工具
butterworth
chebyI
chebyII
"""
import scipy.signal as signal
import numpy as np

def Filter_PF50Hz(My_signal,order,cutoff,filterType,design,Rp,Rs,Fs):
    FilterMains = IIR2Filter(
        order=order,
        cutoff=cutoff,
        filterType=filterType,  # 带阻
        design=design,  # butterworth
        rp=Rp,
        rs=Rs,
        fs=Fs
    )
    My_signal_filter = np.zeros((My_signal.shape))
    for i in range(len(My_signal)):
        My_signal_filter[i] = FilterMains.filter(My_signal[i])
    return My_signal_filter

class IIR2Filter(object):
    def createCoeffs(self, order, cutoff, filterType, design='butter', rp=1, rs=1, fs=0):
        """rp---切比1， rs---切比2"""

        # 滤波器类型参数
        self.designs = ['butter', 'cheby1', 'cheby2']
        self.filterTypes1 = ['lowpass', 'highpass', 'Lowpass', 'Highpass', 'low', 'high']
        self.filterTypes2 = ['bandstop', 'bandpass', 'Bandstop', 'Bandpass']

        # Error handling: other errors can arise too, but those are dealt with
        # in the signal package.
        self.isThereAnError = 1  # if there was no error then it will be set to 0
        self.COEFFS = [0]  # with no error this will hold the coefficients

        if design not in self.designs:
            print('Gave wrong filter design! Remember: butter, cheby1, cheby2.')
        elif filterType not in self.filterTypes1 and filterType not in self.filterTypes2:
            print('Gave wrong filter type! Remember: lowpass, highpass',
                  ', bandpass, bandstop.')
        elif fs < 0:
            print('The sampling frequency has to be positive!')
        else:
            self.isThereAnError = 0

        # if fs was given then the given cutoffs need to be normalised to Nyquist
        if fs and self.isThereAnError == 0:
            for i in range(len(cutoff)):
                cutoff[i] = cutoff[i] / fs * 2

        if design == 'butter' and self.isThereAnError == 0:
            self.COEFFS = signal.butter(order, cutoff, filterType, output='sos')
        elif design == 'cheby1' and self.isThereAnError == 0:
            self.COEFFS = signal.cheby1(order, rp, cutoff, filterType, output='sos')
        elif design == 'cheby2' and self.isThereAnError == 0:
            self.COEFFS = signal.cheby2(order, rs, cutoff, filterType, output='sos')

        return self.COEFFS

    def __init__(self, order, cutoff, filterType, design='butter', rp=1, rs=1, fs=0):
        self.COEFFS = self.createCoeffs(order, cutoff, filterType, design, rp, rs, fs)
        self.acc_input = np.zeros(len(self.COEFFS))
        self.acc_output = np.zeros(len(self.COEFFS))
        self.buffer1 = np.zeros(len(self.COEFFS))
        self.buffer2 = np.zeros(len(self.COEFFS))
        self.input = 0
        self.output = 0

    def filter(self, input):

        # len(COEFFS[0,:] == 1 means that there was an error in the generation
        # of the coefficients and the filtering should not be used
        if len(self.COEFFS[0, :]) > 1:

            self.input = input
            self.output = 0

            # The for loop creates a chain of second order filters according to
            # the order desired. If a 10th order filter is to be created the
            # loop will iterate 5 times to create a chain of 5 second order
            # filters.
            for i in range(len(self.COEFFS)):
                self.FIRCOEFFS = self.COEFFS[i][0:3]
                self.IIRCOEFFS = self.COEFFS[i][3:6]

                # Calculating the accumulated input consisting of the input and
                # the values coming from the feedbaack loops (delay buffers
                # weighed by the IIR coefficients).
                self.acc_input[i] = (self.input + self.buffer1[i]
                                     * -self.IIRCOEFFS[1] + self.buffer2[i] * -self.IIRCOEFFS[2])

                # Calculating the accumulated output provided by the accumulated
                # input and the values from the delay bufferes weighed by the
                # FIR coefficients.
                self.acc_output[i] = (self.acc_input[i] * self.FIRCOEFFS[0]
                                      + self.buffer1[i] * self.FIRCOEFFS[1] + self.buffer2[i]
                                      * self.FIRCOEFFS[2])

                # Shifting the values on the delay line: acc_input->buffer1->
                # buffer2
                self.buffer2[i] = self.buffer1[i]
                self.buffer1[i] = self.acc_input[i]

                self.input = self.acc_output[i]

            self.output = self.acc_output[i]

        return self.output


