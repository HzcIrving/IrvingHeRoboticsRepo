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
EPS = 0.0001 # 收敛阈值
MAX_ITER = 100
show_animation =  True

"""
step1 : 从两组点云中选择匹配的点云，形成匹配两组点云(欧式距离)(错误匹配判定---Dth>N*Avg(D) 
step2 : 利用奇异值分解求解R,t 
step3 : 根据迭代误差决定是否继续迭代
"""

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
    d = np.linalg.norm(np.repeat(cur_pts,prev_pts.shape[1],axis=1) \
                       - np.tile(prev_pts,(1,cur_pts.shape[1])),axis=0)
    indexes = np.argmin(d.reshape(cur_pts.shape[1],prev_pts.shape[1]),axis=1)
    return indexes,error

def svd_motion_est(prev_pts,cur_pts):
    #1. 先求两组点云的质心
    pm = np.mean(prev_pts,axis=1)
    cm = np.mean(cur_pts,axis=1)
    #2.计算偏移量p',c'
    p_s = prev_pts - pm[:,np.newaxis]
    c_s = cur_pts - cm[:,np.newaxis]
    #3.得到W
    W = c_s @ p_s.T
    #4.对W进行SVD
    u,s,vh = np.linalg.svd(W)
    #5.计算R,t
    R = (u@vh).T
    t = pm - (R@cm)
    return R,t

def icp_matching(prev_pts,cur_pts):
    """
    ICP匹配
    :param prev_pts: 上一frame的2D pts
    :param cur_pts: 当前frame的2D pts
    :return: R:旋转矩阵; t:平移矩阵
    """
    H = None # homogeneous 变化矩阵
    dE = 1000.0 # dError
    pE = 1000.0  # prevError
    count = 0
    while dE >= EPS:
        count += 1
        if show_animation:
            plt.cla()
            # 通过"ESC"退出仿真
            plt.gcf().canvas.mpl_connect('key_release_event',
                        lambda event: [exit(0) if event.key == 'escape' else None])
            plt.plot(prev_pts[0, :], prev_pts[1, :], ".r",label="previous pts")
            plt.plot(cur_pts[0, :], cur_pts[1, :], ".b",label="current pts")
            plt.plot(0.0, 0.0, "xr")
            plt.axis("equal")
            plt.legend()
            # plt.show()
            plt.show()
            plt.pause(0.1)
            # plt.close()
        # plt.show()

        indexes,error =nearest_neighbor_association(prev_pts,cur_pts)
        Rt,Tt = svd_motion_est(prev_pts,cur_pts)

        # 更新当前pts
        cur_pts = (Rt@cur_pts)+Tt[:,np.newaxis]

        # Homo变换
        H = update_homogeneous_matrix(H,Rt,Tt)

        dE = abs(pE - error)
        pE = error
        print("误差:",error)

        if dE <= EPS:
            print("收敛，当前误差：", error, dE, count)
            break
        elif MAX_ITER <= count:
            print("达最大迭代次数，不收敛!,此时误差：",error,dE,count)
            break

    R = np.array(H[0:2,0:2])
    T = np.array(H[0:2,2])
    return R,T

def main():
    print(__file__ +"start!")

    # 仿真参数
    nPts = 1000
    fieldLength = 50.0 # 点云区域参数
    motion = [0.5, 2.0, np.deg2rad(-10.0)]  # movement [x[m],y[m],yaw[deg]]

    nsim = 5

    for _ in range(nsim):

        # 创造仿真点
        # 之前的pts
        px = (np.random.rand(nPts) - 0.5) * fieldLength
        py = (np.random.rand(nPts) - 0.5) * fieldLength
        prev_pts = np.vstack((px,py))
        # 当前pts
        cx = [math.cos(motion[2]) * x - math.sin(motion[2]) * y + motion[0]
              for (x, y) in zip(px, py)]
        cy = [math.sin(motion[2]) * x + math.cos(motion[2]) * y + motion[1]
              for (x, y) in zip(px, py)]
        cur_pts = np.vstack((cx, cy))

        R, T = icp_matching(prev_pts, cur_pts)
        print("R:", R)
        print("T:", T)

if __name__ == "__main__":
    main()





