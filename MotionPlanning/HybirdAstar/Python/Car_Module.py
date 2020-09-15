#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He
# email: 1910646@tongji.edu.cn

"""
Car model for Hybrid A* path planning
author: Zheng Zh (@Zhengzh)
"""

from math import sqrt, cos, sin, tan, pi

import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial.transform import Rotation as Rot

class IrvingCar:
    # Car attributes(属性)
    wb = 3. # 前后轮轴之间的长度
    w = 2. # width of the car
    lf = 3.3 # 从车体坐标系原点到车前端的distance
    lb = 1.0 # 从车体坐标系原点到车后端的distance

    car_length = lf + lb

    max_steer = 0.6 # maximum steering angle / rad

    w_bubble_dist = (lf-lb)/2.0
    w_bubble_r = sqrt(((lf+lb)/2.0)**2+1)

    # vehicle rectangle vertices
    # body坐标系下，车体顶点连线
    # from [lf,w/2] to [lf,w/2]
    VRX = [lf,lf,-lb,-lb,lf]
    VRY = [w/2,-w/2,-w/2,w/2,w/2]


# -----------碰撞检测--------------
def check_car_collision():
    pass

def rectangle_check():
    pass
# -------------------------------

# -----------plotplot------------
def plot_car(x,y,yaw):
    car_color = "--r"
    c,s = cos(yaw),sin(yaw)

    # from global frame to local frame
    rot = Rot.from_euler('z',-yaw).as_dcm()[0:2,0:2] # 注意，源代码中as_matrix版本问题会报错

    car_outline_x,car_outline_y = [],[]
    for rx,ry in zip(IrvingCar.VRX,IrvingCar.VRY):
        converted_xy = np.stack([rx,ry]).T @ rot
        car_outline_x.append(converted_xy[0]+x)
        car_outline_y.append(converted_xy[1]+y)

    arrow_x,arrow_y,arrow_yaw = x, y, yaw  # params for plot arrow
    plot_arrow(arrow_x,arrow_y,arrow_yaw)

    plt.plot(x,y,'ko')
    plt.plot(car_outline_x,car_outline_y,car_color)

def plot_arrow(x, y, yaw, length=1.0, width=0.5, fc="r", ec="k"):
    """Plot arrow."""
    if not isinstance(x, float):
        for (i_x, i_y, i_yaw) in zip(x, y, yaw):
            plot_arrow(i_x, i_y, i_yaw)
    else:
        plt.arrow(x, y, length * cos(yaw), length * sin(yaw),
                  fc=fc, ec=ec, head_width=width, head_length=width)

# -------------------------------

# ---------Generalutils----------
def pi_2_pi(angle):
    """instructions:
    A 属于 0~pi + 2k*pi ---> 0~pi
    B 属于 pi~2*pi + 2k*pi ---> -pi~0
    """
    return(angle+pi)%(2*pi) - pi

# Car move --- simple car module
def move(x,y,yaw,distance,steer,L=IrvingCar.wb):
    """distance: △T时间内前进的距离"""
    # kinodynamics
    x += distance * cos(yaw)
    y += distance * sin(yaw)
    yaw += pi_2_pi(distance*tan(steer)/L)
    return x,y,yaw
# -------------------------------

if __name__ == "__main__":
    # test for utils
    angle = 2/3*pi + 2*pi
    angle2 = 4/3*pi + 2*pi
    print(np.rad2deg(pi_2_pi(angle2)))

    # test for car plotting module
    x,y,yaw = 0.,0.,np.pi/3
    plt.axis('equal')
    plot_car(x,y,yaw)
    plt.show()


