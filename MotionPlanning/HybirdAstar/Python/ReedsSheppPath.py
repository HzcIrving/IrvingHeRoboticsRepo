#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

# Original Author : Atsushi Sakai(@Atsushi_twi)


"""
This is Reeds Shepp Based Path Planning script

Reeds Shepp Car Model:
velocity : v ∈ {-v_max,v_max}
yaw: np.abs(yaw) <= yaw_max < pi/2

Reeds Shepp 6 primitives
L+ --- turn left forward
R+ --- turn right forward
L- --- turn left backward
R- --- turn right backward
S+ --- go ahead
S- --- Back

CSC: curve + stright + curve ...
CCC: curve + curve + curve ...

Reeds Shepp可以通过对称性进行求解!
"""

import math
import matplotlib.pyplot as plt
import numpy as np

try:
    from Car_Module import plot_arrow,pi_2_pi
except Exception:
    raise

# Global Var
show_animation = True

# Path attributes
class Path:
    def __init__(self):
        self.lengths = []
        self.ctypes = []
        self.L = 0.0
        self.x = []
        self.y = []
        self.yaw = []
        self.directions = []

def mod2pi(x):
    pass

def reeds_shepp_path_planning(sx,sy,syaw,gx,gy,gyaw,maxc,step_size=0.2):
    """
    Reeds and Shepps Path Planning algorithm
    :param sx: start point x
    :param sy: start point y
    :param syaw: start point yaw
    :param gx: goal point x
    :param gy: goal point y
    :param gyaw: goal point yaw
    :param maxc: max_curvature: 1/m 最大曲率
    :param step_size: reso / m
    :return: path.x, path.y,path.yaw, path.ctypes, path.lengths 类中的属性
    """
    paths = calc_path(sx,sy,syaw,gx,gy,gyaw,maxc,step_size)

def calc_path(sx,sy,syaw,gx,gy,gyaw,maxc,step_size):
    q0 = [sx,sy,syaw]
    q1 = [gx,gy,gyaw]

    paths = generate_path(q0,q1,maxc)

def generate_path(q0,q1,max_curvature):
    """
    用于产生常用的几种基于6个RS基元的路径
    """
    # Goal x,y,yaw=dth
    x,y,dth = start_end_point_regularization(q0,q1,maxc)

    paths = []
    paths = SCS(x,y,dth,paths) # SCS 先直行、转弯、直行
    paths = CSC(x,y,dth,paths) # CSC 转,直,转
    paths = CCC(x,y,dth,paths) # CCC 转,转,转

    return paths

# ===========SCS Module===============
def SCS(x,y,phi,paths):
    """
    straight_curve_straight
    Two Situations:
    --- 1. SLS: go straight →  turn left →  go straight(包括倒退的情况)
    --- 2. STS: go straight →  turn right → go straight
    :param x: goal x
    :param y: goal y
    :param phi: goal phi
    :param paths:
    :return:
    """
    pass

def SLS(x,y,phi):
    phi = mod2pi(phi) # limit the range of phi between (pi~-pi)
    if y > 0.0 and 0.0 < phi < math.pi * 0.99: # avoid zero-division problem
        xd = -y/math.tan(phi) + x
        t = xd - math.tan(phi/2.0)
        u = phi
        v = math.sqrt((x-xd)**2 + y**2)-math.tan(phi/2.0)
        return True,t,u,v
    elif y < 0.0 < phi < math.pi * 0.99:
        xd = -y / math.tan(phi) + 

# ====================================




def start_end_point_regularization(q0,q1,maxc):
    """对初始点与末尾目标点的初始化操作"""
    dx = q1[0] - q0[0]  # x2-x1 = dx
    dy = q1[1] - q0[1]
    dth = q1[2] - q0[2] # theta2 - theta1 = yaw
    c = np.cos(q0[2])
    s = np.sin(q0[2])
    x = (c*dx+s*dy) * maxc
    y = (-s*dx+c*dy)* maxc
    return x,y,dth

# 极坐标转换
def polar(x,y):
    r = math.sqrt(x**2+y**2)
    theta = math.atan2(y,x)
    return r,theta

# mod2pi utils
def mod2pi(x):
    v = np.mod(x,2.0*np.pi)
    if v < -np.pi:
        v += 2.0*np.pi
    else:
        if v > np.pi:
            v -= 2.0*np.pi
    return v

if __name__ == "__main__":
    phi = 1111111/3*np.pi
    print(np.rad2deg(mod2pi(phi)))