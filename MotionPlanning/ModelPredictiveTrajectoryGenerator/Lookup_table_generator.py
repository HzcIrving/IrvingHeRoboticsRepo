#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

import Model_Trajectory_generator as planner
from motion_model import *
import pandas as pd
import math
import numpy as np

import matplotlib.pyplot as plt

def calc_states_list():
    # 计算状态列表
    # from start to final
    # t0~tf
    maxyaw = np.deg2rad(-30.0) # yaw角max约束

    x = np.arange(10.0,35.0,5.0) # 间隔 5.0 10～30
    y = np.arange(0.0,25.0,5.0) # 间隔 5.0 0～20

    # -max_yaw,-max_yaw/2,0,max_yaw/2
    yaw = np.arange(-maxyaw,maxyaw,maxyaw/2) # [-maxyaw,0]

    states = []
    for iyaw in yaw:
        for iy in y:
            for ix in x:
                states.append([ix,iy,iyaw])
    print("nstates:", len(states))
    return states

def search_nearest_one_from_lookuptable(tx,ty,tyaw,lookuptable):
    """
    :param tx: target x
    :param ty: target y
    :param tyaw: target yaw
    :param lookuptable:
    :return: 可以达到最小距离的lookuptable中的数据
    """
    mind = float("inf")   # initial distance
    minid = -1
    for (i,table) in enumerate(lookuptable):
        dx = tx-table[0]
        dy = ty-table[1]
        dyaw = tyaw-table[2]
        # update distance
        d = math.sqrt(dx**2+dy**2+dyaw**2)
        if d <= mind:
            minid = i
            mind = d
    return lookuptable[minid]

def save_lookup_table(fname,table):
    mt = np.array(table)
    print(mt)
    # save csv
    df = pd.DataFrame()
    df["x"] = mt[:,0]
    df["y"] = mt[:,1]
    df["yaw"] = mt[:,2]
    df["s"] = mt[:,3]
    df["km"] = mt[:,4]
    df["kf"] = mt[:,5]
    df.to_csv(fname,index=None)

def generate_lookup_table():
    states = calc_states_list()
    k0 = 0.0

    # x,y,yaw,s,km,kf
    lookuptable = [[1.0,0.0,0.0,1.0,0.0,0.0]]

    for state in states:
        bestp = search_nearest_one_from_lookuptable(
            state[0],
            state[1],
            state[2],
            lookuptable
        )

        # state = [xi,yi,yawi]
        target = State(x=state[0],y=state[1],yaw=state[2])

        # s,km,kf
        init_p = np.array(
            [math.sqrt(state[0]**2+state[1]**2),bestp[4],bestp[5]]
        ).reshape(3,1)

        # update p and state
        x,y,yaw,p = planner.optimization_trajectory(target,k0,init_p)

        if x is not None:
            print("find good path")

            lookuptable.append(
                [x[-1],y[-1],yaw[-1],float(p[0]),float(p[1]),float(p[2])]
            )

    print("finish lookup table generation")

    save_lookup_table("lookuptable.csv",lookuptable)

    for table in lookuptable:
        # k0 = 0.0
        xc,yc,yawc = generate_trajectory(
            table[3],table[4],table[5],k0
        )

        # xc1,yc1,yawc1 = generate_trajectory(
        #     table[3],-table[4],table[5],k0
        # )
        plt.plot(xc,yc,"-b")
        # plt.plot(xc1, yc1, "-r")

    plt.grid(True)
    plt.axis("equal")
    plt.show()

    print("Done")

def main():
    generate_lookup_table()

if __name__ == "__main__":
    main()



