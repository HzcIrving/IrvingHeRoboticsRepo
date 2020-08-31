#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn


"""
A2C
Advantage Actor Critic
Advantage --- A(s,a) = Q(s,a) - V(s）
反应衡量选取动作值和所有动作平均值好坏的指标
"""

import math
import random

import gym
import numpy as np

import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F
from torch.distributions import Categorical

import matplotlib.pyplot as plt

import multiprocessing

from multi_processing_envs import SubprocVecEnv # 子进程环境

use_cuda = torch.cuda.is_available()
device = torch.device("cuda" if use_cuda else "cpu")

print("Current device name:",device)
print("Current cpu nums:",multiprocessing.cpu_count())

num_envs = 4
env_name = "CartPole-v0"

def make_env():
    def _thunk():
        env = gym.make(env_name)
        return env
    return _thunk

plt.ion()
envs = [make_env() for i in range(num_envs)]

envs = SubprocVecEnv(envs) # 8 envs
env = gym.make(env_name) # a single env

class ActorCritic(nn.Module):
    """Actor输入:o,a"""
    def __init__(self, num_inputs, num_outputs, hidden_size, std=0.0):
        super(ActorCritic, self).__init__()

        self.critic = nn.Sequential(
            nn.Linear(num_inputs, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, 1) # output Q value
        )

        self.actor = nn.Sequential(
            nn.Linear(num_inputs, hidden_size),
            nn.ReLU(),
            nn.Linear(hidden_size, num_outputs),
            nn.Softmax(dim=1), # output probs
        )

    def forward(self, x):
        value = self.critic(x)
        probs = self.actor(x)  #
        dist = Categorical(probs) # 按照probs来进行采样
        return dist, value

def test_env(vis=False):

    num_inputs = envs.observation_space.shape[0]
    num_outputs = envs.action_space.n

    # hyper params
    hidden_size = 256
    lr = 1e-3
    num_steps = 5

    model = ActorCritic(num_inputs,num_outputs,hidden_size).to(device)

    state = env.reset()
    if vis:
        env.render() # 可视化
    done = False
    total_reward = 0
    while not done:
        state = torch.FloatTensor(state).unsqueeze(0).to(device)
        dist,_ = model(state)
        # dist.sample() -- 按照概率密度采样
        next_state,reward,done,_ = env.step(dist.sample().cpu().numpy()[0])
        state = next_state
        if vis:
            env.render()
        total_reward += reward
    return total_reward

def compute_return(next_value,rewards,masks,gamma=0.99):
    R = next_value
    returns = []
    for step in reversed(range(len(rewards))):
        R = rewards[step] + gamma*R*masks[step]
        returns.insert(0,R)
    return returns

def plot(frame_idx,rewards):
    plt.plot(rewards,'b-')
    plt.title("frame %s. reward: %s"%(frame_idx,rewards[-1]))
    plt.pause(0.0001)

def main():
    num_inputs = envs.observation_space.shape[0]
    num_outputs = envs.action_space.n

    # hyper params
    hidden_size = 256
    lr = 1e-3
    num_steps = 50

    model = ActorCritic(num_inputs,num_outputs,hidden_size).to(device)
    optimizer = optim.Adam(model.parameters())

    max_frames = 10000
    frame_idx = 0
    test_rewards = []

    state = envs.reset()

    while frame_idx < max_frames:
        print("Current frame_idx:",frame_idx)
        log_probs = []
        values = []
        rewards = []
        masks = []
        entropy = 0

        # rollout trajectory
        for _ in range(num_steps):
            state = torch.FloatTensor(state).to(device)
            dist,value = model(state)

            action = dist.sample() # 采样
            next_state,reward,done,_ = envs.step(action.cpu().numpy())

            log_prob = dist.log_prob(action)
            entropy += dist.entropy().mean() # 熵正则化

            log_probs.append(log_prob)
            values.append(value)
            rewards.append(torch.FloatTensor(reward).unsqueeze(1).to(device))
            masks.append(torch.FloatTensor(1-done).unsqueeze(1).to(device))

            state = next_state
            frame_idx += 1

            if frame_idx % 100 == 0:
                test_rewards.append(np.mean([test_env() for _ in range(10)]))
                test_env(vis=True)
                plot(frame_idx,test_rewards)

        next_state = torch.FloatTensor(next_state).to(device)
        _,next_value = model(next_state)
        returns = compute_return(next_value,rewards,masks) #Q_value

        log_probs = torch.cat(log_probs)
        returns = torch.cat(returns).detach()
        values = torch.cat(values)

        # 优势函数
        advantage = returns - values

        # policy gradient
        actor_loss = -(log_probs*advantage.detach()).mean()

        # TD error
        # mse
        critic_loss = advantage.pow(2).mean()

        # 这里同时学习了actor与critic
        # 其实应该分开来学习，会比较好 --- by Google Deepmind
        loss = actor_loss + 0.5*critic_loss - 0.001*entropy

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # test_env(True)

if __name__ == "__main__":
    # test
    # test_env(vis=True)
    main()