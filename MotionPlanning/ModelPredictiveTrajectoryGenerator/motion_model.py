#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

"""
运动模型
"""

import math
import numpy as np
import scipy.interpolate

import matplotlib.pyplot as plt


# motion parameter
L = 1.0 # wheel base
ds = 0.1 # course distance
v = 10.0/3.6 # m/s 10km/h

class State:
    def __init__(self,x=0.0,y=0.0,yaw=0.0,v=0.0):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v

def pi_2_pi(angle):
    # if angle is bigger than 2*pi, this function will rescale
    # the abs of the angle to [0,pi]
    # input np.pi/3 ---> return np.pi/3
    # input np.pi+np.pi/3 ---> return -2*np.pi/ 3
    # input 2*np.pi + np.pi/3 ---> return np.pi/3
    return (angle+math.pi)%(2*math.pi)-math.pi

def update(state,v,delta,dt,L):
    # the update of robot model
    # state is the class of STATE
    # the model is the classical BICYCLE model
    state.v = v
    state.x = state.x + state.v*np.cos(state.yaw)*dt
    state.y = state.y + state.v*np.sin(state.yaw)*dt
    state.yaw = state.yaw + state.v/L * np.tan(delta)*dt  # delta --> steer
    state.yaw = pi_2_pi(state.yaw) # avoid the abs value of angle is bigger than 2pi
    return state

def generate_trajectory(s,km,kf,k0):
    # u = [v(p,t), k(p,s)] T
    # k(p,s) curvature
    # 路程曲率方程

    # a v
    # generate trajectory
    # ds : the increment on the course direction
    n = s/ds  # resolution
    time = s/v # Time

    # Forced Type Conversion
    if isinstance(time,type(np.array([]))):
        time = time[0]
    if isinstance(km,type(np.array([]))):
        km = km[0]
    if isinstance(kf,type(np.array([]))):
        kf = kf[0]

    #
    tk = np.array([0.0,time/2.0,time])
    kk = np.array([k0,km,kf]) # 曲率 k0,k1,k2 在这3点之间进行插值

    # Time Discretization
    t = np.arange(0.0,time,time/n)
    dt = float(time/n)

    # quadratic
    # 插值出路程曲率方程
    fkp = scipy.interpolate.interp1d(tk,kk,kind="quadratic")
    kp = [fkp(ti) for ti in t ] # 离散化的路径点集

    # plot model
    # --------------
    # plt.plot(t,kp)
    # plt.grid(True)
    # plt.show()
    # --------------

    # get current state
    state = State()
    x,y,yaw = [state.x],[state.y],[state.yaw]

    for ikp in kp:
        # 根据输入的曲率方程、速度配置来更新State
        # [v]、[ikp] --- > update State
        state = update(state,v,ikp,dt,L)
        x.append(state.x)
        y.append(state.y)
        yaw.append(state.yaw)

    return x,y,yaw

def generate_last_state(s,km,kf,k0):
    """
    k0 : initial curvature point
    km : middle curvature point
    kf : final curvature point
    """

    n = s/ds
    time = s/v # [s] # 匀速条件下..

    # Forced Type Conversion
    if isinstance(time,type(np.array([]))):
        time = time[0]
    if isinstance(km,type(np.array([]))):
        km = km[0]
    if isinstance(kf,type(np.array([]))):
        kf = kf[0]

    tk = np.array([0.0, time / 2.0, time])
    kk = np.array([k0, km, kf])

    t = np.arange(0.0, time, time / n)

    fkp = scipy.interpolate.interp1d(tk, kk, kind="quadratic")
    kp = [fkp(ti) for ti in t]

    dt = time / n

    state = State()
    _ = [update(state,v,ikp,dt,L) for ikp in kp]

    return state.x,state.y,state.yaw  # x,y,yaw ...

def test():
    # -------------
    s = State(x=10,y=10)
    print(s.x)
    print(s.y)
    print("="*20)
    # -------------
    a = np.pi/3
    a = 2*np.pi/3
    a = 4*np.pi + np.pi/3
    a = np.pi + np.pi/3
    a_1 = pi_2_pi(a)
    print(a_1)
    print(a_1/np.pi*180) # 60 # 120 # 60
    print("=" * 20)
    # -------------

if __name__ == "__main__":
    test()
