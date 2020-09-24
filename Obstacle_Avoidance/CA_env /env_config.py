#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

"""
@inproceedings{Everett18_IROS,
  address = {Madrid, Spain},
  author = {Everett, Michael and Chen, Yu Fan and How, Jonathan P.},
  booktitle = {IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS)},
  date-modified = {2018-10-03 06:18:08 -0400},
  month = sep,
  title = {Motion Planning Among Dynamic, Decision-Making Agents with Deep Reinforcement Learning},
  year = {2018},
  url = {https://arxiv.org/pdf/1805.01956.pdf},
  bdsk-url-1 = {https://arxiv.org/pdf/1805.01956.pdf}
}
"""

"""
Env 环境参数配置脚本
基于 gym-collision-env 的脚本 进行二次编写

可以设置参数有：

"""
import numpy as np

class OA_Config(object):
    def __init__(self):
        # 1. 一般参数
        # self.COLLISION_AVOID

        # 2. 传感器参数
        # ---- LaserScan ----
        self.NUM_BEAMS = 512 #  num range readings in one scan
        self.NUM_TO_STORE = 3
        self.RANGE_RESO = 0.1 # radians between each beam
        self.MAX_RANGE = 6 # meters
        self.MIN_RANGE = 0 # meters
        self.MAX_ANGLE = np.pi/2  #  relative to agent's current heading, angle of the first beam (radians)
        self.MIN_ANGLE = -self.MAX_ANGLE #  relative to agent's current heading, angle of the last beam (radians)
        self.LADER_DEBUG = False # debug plot flag
