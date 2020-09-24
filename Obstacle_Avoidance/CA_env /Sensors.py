#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

"""
传感器脚本
包含Simulation的传感器有：
1. 2D LaserScan
2.
"""

import numpy as np
import matplotlib.pyplot as plt
from env_config import *


import time

class Sensor(object):
    """
    传感器的标准写法
    """
    def __init__(self):
        pass

    def sense(self,agents,agent_index,top_down_map):
        """
        虚拟方法，每个Sensor的子类来重新实现
        每个传感器的sense方法不太一样
        """
        raise NotImplementedError

    def set_args(self,args):
        """
        用于设置参数
        Args:
            args(dict): {'arg_name1":new_value1, ...}
            sets : code : 'self.arg_name1 = new_value1'
        """
        # 提供参数的键值对的字典
        for arg,value in args.items():
            setattr(self,arg,value)

class LaserScanSensor(Sensor):
    """
    LaserScanSensor说明:
    #### Params Setting ####
    关于2D Scan的关键参数设置
    num_beams: -> int 多少束的
    num_to_store: -> int 多少次过去的激光扫描可以堆叠成一个测量量
    range_resolution: -> float 光束的分辨率 /m
    max_range: -> float 每个激光束的最大值 / m
    min_range: -> float 每个激光束的最小值 / m
    max_angle: -> float 注意是相对于robot当前heading方向的最大方向，第一个激光束/弧度
    min_angle: -> float .......,最后一个光束与heading之间的夹角
    ####
    """
    def __init__(self):
        Sensor.__init__(self)
        self.name = 'laserscan'
        self.num_beams = OA_Config.NUM_BEAMS
        self.num_to_store = OA_Config.NUM_TO_STORE
        self.range_resolution = OA_Config.RANGE_RESO
        self.max_range = OA_Config.MAX_RANGE
        self.min_range = OA_Config.MIN_RANGE
        self.max_angle = OA_Config.MAX_ANGLE
        self.min_angle = OA_Config.MIN_ANGLE

        # angles definition
        # np.array
        # angles ranges from min_angle to max_angle (LINEAR...)
        self.angles = np.linspace(self.min_angle,self.max_angle,self.num_beams)
        # ranges space : ranging from min_range to max_range
        # 0~6m reso:0.1m
        self.ranges = np.arange(self.min_range,self.max_range,self.range_resolution)

        self.debug = OA_Config.LADER_DEBUG
        # default shape(3,512)
        self.measurement_history = np.zeros((self.num_to_store,self.num_beams))
        self.num_measurements_made = 0

        if self.debug:
            plt.figure('lidar')

    def sense(self,agents,agent_index,top_down_map):
        """
        top_down_map来标记obstacles,sensor定位在agents[agent_index]的中心
        :param agents: -> list , Agent类
        :param agent_index: -> int, the index of this agent
        :param top_down_map: -> 2D np array , binary 图像
        :return:
            measurement_history (np.array): (num_to_store,num_beams)
            激光扫描的测量值存储空间
        """
        host_agent = agents[agent_index]

        # angles是相对angles，转为绝对angle得add heading angle
        angles = self.angles + host_agent.heading_global_frame
        ranges = self.ranges
        # 进行mesh
        angles_ranges_mesh = np.meshgrid(angles,ranges)

        # 建立激光雷达网格
        # 每一个(angle,range)都有对应的值
        # out_put (60,512,2)
        # 60: np.arange(max_range,min_range,reso)
        # 512: np.linspace(max_angle,min_angle,reso)
        # angles_ranges[:,:,0] -> 表示 激光束坐标系中的range值
        # angles_ranges[:,:,1] -> 表示 激光束坐标系中的angle值
        angles_ranges = np.dstack([angles_ranges_mesh[0],angles_ranges_mesh[1]])
        beam_coords = np.tile(host_agent.pos_global_frame,(len(angles),len(ranges),1)).astype(np.float64)
        # from beam_frame to global frame 从激光束坐标系到世界坐标系
        beam_coords[:,:,0] += (angles_ranges[:,:,1]*np.cos(angles_ranges[:,:,0])).T
        beam_coords[:,:,1] += (angles_ranges[:,:,1]*np.sin(angles_ranges[:,:,0])).T

        iis,jjs,in_maps = top_down_map.world_coordinates_to_map_indices_vec(beam_coords)

        # 在2D Laser图中进行标记
        ego_agent_mask = top_down_map.get_agent_mask(host_agent.pos_global_frame,host_agent.radius)
        lidar_hits = np.logical_and.reduce((top_down_map.map[iis,jjs],
                            np.invert(ego_agent_mask[iis,jjs]),in_maps)) # 将地图中hit障碍物的区域进行and操作
        lidar_hits_cumsum = np.cumsum(lidar_hits,axis=1)
        first_hits = np.where(lidar_hits_cumsum == 1)

        ranges = self.max_range*np.ones_like(self.angles)
        ranges[first_hits[0]] = self.ranges[first_hits[1]]

        # measurement_history(3,512)
        if self.num_measurements_made == 0:
            self.measurement_history[:,:] = ranges
        else:
            self.measurement_history = np.roll(self.measurement_history, 1, axis=0)
            self.measurement_history[0,:] = ranges
        self.num_measurements_made += 1

        if self.debug:
            in_map_inds = np.where(in_maps)
            iis_in_map = iis[in_map_inds]
            jjs_in_map = jjs[in_map_inds]
            lidar_map = top_down_map.map.copy()
            lidar_map[iis_in_map, jjs_in_map] = 1
            plt.figure('lidar')
            plt.imshow(lidar_map)
            plt.pause(0.01)

        return self.measurement_history.copy()

    def sense_old(self, agents, agent_index, top_down_map):
        host_agent = agents[agent_index]

        if self.debug:
            lidar_map = top_down_map.map.copy()

        ego_agent_mask = top_down_map.get_agent_mask(host_agent.pos_global_frame, host_agent.radius)
        ranges = self.max_range*np.ones_like(self.angles)
        for angle_i, angle in enumerate(self.angles+host_agent.heading_global_frame):
            for r in self.ranges:
                pos = host_agent.pos_global_frame+np.array([r*np.cos(angle), r*np.sin(angle)])
                [i, j], in_map = top_down_map.world_coordinates_to_map_indices(pos)
                if self.debug and in_map:
                    lidar_map[i,j]=1
                if not in_map or ego_agent_mask[i,j]:
                    continue
                if top_down_map.map[i, j]:
                    if self.debug:
                        print("Object at {}!!".format(r))
                    ranges[angle_i] = r
                    break
        if self.debug:
            plt.imshow(lidar_map)
            plt.pause(1)
        return ranges

if __name__ == "__main__":
    sensor = Sensor()
    sensor.sense()

