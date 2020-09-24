#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

from env_config import *
import math
import numpy as np
import matplotlib.pyplot as plt

class Agent(object):
    """

    """
    def __init__(self):
        pass

    def reset(self):
        pass

    def __deepcopy__(self):
        pass

    def _check_if_at_goal(self):
        pass

    def _update_state_history(self):
        pass

    def set_state(self):
        pass

    def take_action(self):
        pass

    def sense(self):
        pass

    def print_agent_info(self):
        """ Print out a summary of the agent's current state. """
        print('----------')
        print('Global Frame:')
        print('(px,py):', self.pos_global_frame)
        print('(vx,vy):', self.vel_global_frame)
        print('speed:', self.speed_global_frame)
        print('heading:', self.heading_global_frame)
        print('Body Frame:')
        print('(vx,vy):', self.vel_ego_frame)
        print('heading:', self.heading_ego_frame)
        print('----------')

    def to_vector(self):
        pass

    def get_sense_data(self):
        pass

    def get_agent_data_equiv(self):
        pass

    def get_observation_dict(self):
        pass

    def get_ref(self):
        pass

    def _store_past_velocities(self):
        pass

    def ego_pos_to_global_pos(self):
        pass

    def global_pos_to_ego_pos(self):
        pass

