#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

"""
Lattice Plannar --- Kinodynamic Path Finding!
1. Sample in control space
2. Sample in state space

Refs:
State Space Sampling of Feasible Motions for --
High-Performance Mobile Robot Navigation in Complex Environments

Build Lattice Graph
Methods for solving the BVP
1.Model Predictive (Sample in state space)
2.Pontryain's Minimum Principle(optimal control)
"""

import sys

sys.path.append("../ModelPredictiveTrajectoryGenerator")

try:
    import Model_Trajectory_generator as plannar
    import motion_model
    from Lookup_table_generator import *
except:
    raise

import os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math

absolute_path = os.path.dirname(os.path.abspath(__file__))
table_path = "lookuptable.csv"
show_animation = True

def get_loopup_table():
    data = pd.read_csv(table_path)
    return np.array(data)

def generate_path(target_states,k0):
    """
    产生路径
    :param target_states: 目标状态
    :param k0: 出事curvature
    :return:
    """
    # x,y,yaw,s,km,kf (lookuptable[i])
    lookup_table = get_loopup_table()
    result = []

    for state in target_states:
        # from current state to target_state
        bestp = search_nearest_one_from_lookuptable(
            state[0],
            state[1],
            state[2],
            lookup_table
        ) # best control factor --- (s,km,kf)

        target = motion_model.State(x=state[0],y=state[1],yaw=state[2])
        # initial state
        init_p = np.array(
            [math.sqrt(state[0] ** 2 + state[1] ** 2), bestp[4], bestp[5]]).reshape(3, 1)

        x,y,yaw,p = planner.optimization_trajectory(target,k0,init_p)

        if x is not None:
            print("find good path")
            result.append(
                [x[-1], y[-1], yaw[-1], float(p[0]), float(p[1]), float(p[2])])

    print("finish path generation")
    return result

def sample_states(angle_samples,a_min,a_max,d,p_max,p_min,nh):
    states = []
    for i in angle_samples:
        # angle step
        a = a_min + (a_max-a_min)*i
        for j in range(nh):
            xf = d*math.cos(a)
            yf = d*math.sin(a)
            if nh == 1:
                yawf = (p_max-p_min)/2+a
            else:
                yawf = p_min + (p_max-p_min)*j/(nh-1)+a
            states.append([xf,yf,yawf])

def clac_uniform_polar_states(nxy,nh,d,a_min,a_max,p_min,p_max):
    """
    计算uniform state
    p[s,km,kf]
    :param nxy: position采样的数量
    :param nh: heading采样的数量
    :param d: 终点状态terminal state距离
    :param a_min: position sampling min angle 状态采样的最小angle
    :param a_max: position sampling max angle 状态采样的最大angle
    :param p_min: heading sampling min angle
    :param p_max: heading sampling max angle
    :return: states list
    """
    angle_samples = [i/(nxy-1) for i in range(nxy)]
    states = sample_states(angle_samples,a_min,a_max,d,p_max,p_min,nh)