#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

"""
A3C
Pytorch + multiprocessing
我认为 A3C中的异步，体现在，只要worker做完一个episode的活动，就进行push and pull
这里是异步的行为
"""

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.multiprocessing as mp  # torch
from torch.distributions import Normal

import gym
import math,os
# "OMP_NUM_THREADS" The number of threads the program executes
os.environ["OMP_NUM_THREADS"] = "1" # environ:get the infos of the system

from Morvan_utils import *

# Hyper Params
UPDATE_GLOBAL_ITER = 5 # the freq of updating the global nets
GAMMA = 0.9 # 0.9
MAX_EP = 5000
MAX_EP_STEP = 200

env = gym.make('Pendulum-v0') # a single env
N_S = env.observation_space.shape[0]
N_A = env.action_space.shape[0]
print("state dim: {}".format(N_S))
print("action dim: {}".format(N_A))

class Net(nn.Module):
    def __init__(self,s_dim,a_dim):
        super(Net,self).__init__()
        self.s_dim = s_dim
        self.a_dim = a_dim
        # actor
        self.a1 = nn.Linear(s_dim,256)
        self.mu = nn.Linear(256,a_dim)
        self.sigma = nn.Linear(256,a_dim)
        # critic
        self.c1 = nn.Linear(s_dim,256)
        self.v = nn.Linear(256,1)

        # distribution --> normal
        self.distribution = Normal

    def forward(self,x):
        # actor
        a1 = F.relu6(self.a1(x))
        mu = 2*F.tanh(self.mu(a1)) # -2~2
        sigma = F.softplus(self.sigma(a1)) + 0.001 # avoid 0

        # critic
        c1 = F.relu6(self.c1(x))
        values = self.v(c1) # value
        return mu,sigma,values # output a dist

    def choose_action(self,s):
        self.training = False
        mu,sigma,_ = self.forward(s)
        m = self.distribution(mu.view(1, ).data,sigma.view(1, ).data)
        return m.sample().numpy() # distribution

    def loss_func(self,s,a,v_t):
        # v_t : t step value
        self.train()
        mu,sigma,values = self.forward(s)

        # TD error
        td = v_t - values
        c_loss = td.pow(2) # td loss

        m = self.distribution(mu,sigma)
        log_prob = m.log_prob(a) # get -log pi(x_t|s_t)

        # calculate the entropy of policy pi
        # entropy --- for exploration
        entropy = 0.5 + 0.5*math.log(2*math.pi) + torch.log(m.scale) # exploration
        exp_v = log_prob*td.detach() + 0.005*entropy

        a_loss = -exp_v

        total_loss = (a_loss+c_loss).mean()
        return total_loss

# Every work's job
class Worker(mp.Process):
    def __init__(self,gnet,opt,global_ep,global_ep_r,res_queue,name):
        super(Worker,self).__init__()
        self.name = 'w%i' % name # worker index
        self.g_ep,self.g_ep_r,self.res_queue = global_ep,global_ep_r,res_queue
        self.gnet = gnet
        self.opt = opt
        self.lnet = Net(N_S,N_A) # local net
        self.env = gym.make('Pendulum-v0').unwrapped

    def run(self):
        # the main job that each worker needs to complete
        total_step = 1
        while self.g_ep.value < MAX_EP: # episode count
            s = self.env.reset()
            buffer_s = []
            buffer_a = []
            buffer_r = []
            ep_r = 0. # episode rewards
            for t in range(MAX_EP_STEP):
                if self.name == "w0":
                    # only render the first worker
                    self.env.render()
                a = self.lnet.choose_action(v_wrap(s[None,:]))
                s_,r,done,_ = self.env.step(a.clip(-2,2)) # clip operation to limit the range
                if t == MAX_EP_STEP - 1:
                    done = True
                ep_r += r
                buffer_a.append(a)
                buffer_s.append(s)
                buffer_r.append((r+8.1)/8.1) # normalize

                if total_step % UPDATE_GLOBAL_ITER == 0 or done:
                    # the end of a episode
                    # push and pull operation
                    # sync 同步
                    push_and_pull(self.opt,self.lnet,self.gnet,done,s_,buffer_s,buffer_a,buffer_r,GAMMA)
                    buffer_s = []
                    buffer_a = []
                    buffer_r = []
                    if done:
                        record(self.g_ep, self.g_ep_r, ep_r, self.res_queue, self.name)
                        break

                s = s_
                total_step += 1

        self.res_queue.put(None)

def main():
    # global net
    gnet = Net(N_S,N_A)

    # share the global parameters in multiprocessing
    gnet.share_memory()

    # global optimizer
    opt = SharedAdam(gnet.parameters(),lr=1e-4,betas=(0.95,0.999))

    # 通过value将数据存储在一个共享的内存表中
    global_ep = mp.Value('i',0) #int 型, initial = 0
    global_ep_r = mp.Value('d',0) # double
    res_queue = mp.Queue() # result queue

    # parallel training
    workers = [Worker(gnet,opt,global_ep,global_ep_r,res_queue,i) for i in range(4)] # 4 process
    [w.start() for w in workers]
    res = [] #record episode reward to plot
    while True:
        r = res_queue.get()
        if r is not None:
            res.append(r)
        else:
            break

    [w.join() for w in workers]

    import matplotlib.pyplot as plt
    plt.plot(res)
    plt.ylabel('Moving Average ep reward')
    plt.xlabel('Step')
    plt.show()

if __name__ == "__main__":
    main()


