#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

# 原author: Atsushi Sakai (@Atsushi_twi), Göktuğ Karakaşlı

# Iterative Closest Point
# 2D ICP 匹配算法
# 基本方法 : Singular Value Decomposition 奇异值分解

import math
import matplotlib.pyplot as plt
import numpy as np

# ICP PARAMS
EPS = 0.0001
MAX_ITER = 100

show_animation =  True

"""
step1 : 从两组点云中选择匹配的点云，形成匹配两组点云(欧式距离)(错误匹配判定---Dth>N*Avg(D) 
step2 : 利用奇异值分解求解R,t 
step3 : 根据迭代误差决定是否继续迭代
"""

def icp_matching(prev_pts,cur_pts):
    """
    ICP匹配
    :param prev_pts: 上一frame的2D pts
    :param cur_pts: 当前frame的2D pts
    :return: R:旋转矩阵; t:平移矩阵
    """
    pass

def update_homogeneous_matrix(Hin,R,T):
    #  H = |  R  | t |
    #      |0 0 0| 1 | # 3D homo-mtx
    H = np.zeros((3,3))
    H[0,0] = R[0,0]
    H[1,0] = R[1,0]
    H[0,1] = R[0,1]
    H[1,1] = R[1,1]
    H[2,2] = 1.0 # for 2D

    H[0,1] = T[0]
    H[1,2] = T[1]
    if Hin is None:
        return H
    else:
        return Hin @ H

def nearest_neighbor_association(prev_pts,cur_pts):
    # 计算总的残留误差
    delta_pts = prev_pts - cur_pts
    d = np.linalg.norm(delta_pts,axis=0)
    error = sum(d)

    # 计算最近点的索引
    d = np.linalg.norm(np.repeat(cur_pts,prev_pts.shape[1],axis=1),
                       -np.tile(prev_pts,(1,cur_pts.shape[1]),axis=0))
    indexes = np.argmin(d.reshape(cur_pts.shape[1],prev_pts.shape[1]),axis=1)
    return indexes,error

def svd_motion_est(prev_pts,cur_pts):
    pm = np.mean()



