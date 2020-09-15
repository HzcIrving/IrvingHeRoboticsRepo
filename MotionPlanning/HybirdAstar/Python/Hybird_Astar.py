#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# original author: Zheng Zh(@Zhengzh)
# author: Irving He 
# email: 1910646@tongji.edu.cn

# An algorithm for kinodynamic path planning task
# - Main Framework
# -- 1.

import heapq
import math
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree

from Car_Module import *

class Config:
    # Params Config class
    XY_Grid_reso = 2.0 #[m] 分辨率2m
    Yaw_Grid_reso = np.deg2rad(15) # yaw角分辨率15°
    Motion_reso = 0.1 #[m]
    N_steer = 20 # steer command

    # robot radius
    Vr = 1.0 # m
