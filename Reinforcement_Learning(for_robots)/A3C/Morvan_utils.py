#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

"""
utils list :
1. numpy 2 tensor
2. initialize the neural networks' params
3. push and pull between the local nets and global nets
4. shared adam optimizer between different local nets
"""

from torch import nn
import torch
import numpy as np

def v_wrap(np_array,dtype=np.float32):
    """array 2 tensor"""
    if np_array.dtype != dtype:
        np_array = np_array.astype(dtype)
    return torch.from_numpy(np_array)

def set_init(layers):
    """initialize to nn layers"""
    for layer in layers:
        # the 1st initialize method
        nn.init.normal_(layer.weight,mean=0.,std=0.1) # normalize
        nn.init.constant_(layer.bias,0.)

        # ToDo: Other initialize method could lead to a better performance?

def push_and_pull(opt,lnet,gnet,done,s_,bs,ba,br,gamma):
    """
    The operation between the local net and the global net
    :param opt:  optimizer
    :param lnet:  local net
    :param gnet:  global net
    :param done:  whether done or not?
    :param s_:  next state
    :param bs: batch_states
    :param ba: batch_actions
    :param br: batch_rewards
    :param gamma: discounted
    """
    if done:
        v_s_ = 0 # terminal
    else:
        v_s_ = lnet.forward(v_wrap(s_[None,:]))[-1].data.numpy()[0,0]

    buffer_v_target = []
    for r in br[::-1]: # reverse buffer r to calculate the target v
        v_s_ = r + gamma*v_s_
        buffer_v_target.append(v_s_)
    buffer_v_target.reverse()

    loss = lnet.loss_func(
        v_wrap(np.vstack(bs)),
        v_wrap(np.array(ba),dtype=np.int64) if ba[0].dtype == np.int64 else v_wrap(np.vstack(ba)),
        v_wrap(np.array(buffer_v_target)[:,None])
    )

    # calculate the local gradients and push local params to global
    opt.zero_grad()
    loss.backward()
    for lp,gp in zip(lnet.parameters(),gnet.parameters()):
        gp._grad = lp.grad
    opt.step()

    # pull global parameters
    # because every worker has push their local gradient
    # so, the center server's params is changing every time
    lnet.load_state_dict(gnet.state_dict())

def record(global_ep, global_ep_r, ep_r, res_queue, name):
    """
    :param global_ep:  global
    :param global_ep_r:
    :param ep_r:
    :param res_queue:
    :param name:
    :return:
    """
    with global_ep.get_lock():
        global_ep.value += 1
    with global_ep_r.get_lock():
        if global_ep_r.value == 0.:
            global_ep_r.value = ep_r
        else:
            # moving average
            global_ep_r.value = global_ep_r.value * 0.99 + ep_r * 0.01
    res_queue.put(global_ep_r.value) # create a rewards queue to record
    print(
        name,
        "Ep:", global_ep.value,
        "| Ep_r: %.0f" % global_ep_r.value,
    )

"""
Shared optimizer, the parameters in the optimizer will shared in the multiprocessors.
"""
class SharedAdam(torch.optim.Adam):
    def __init__(self, params, lr=1e-3, betas=(0.9, 0.99), eps=1e-8,
                 weight_decay=0):
        super(SharedAdam, self).__init__(params, lr=lr, betas=betas, eps=eps, weight_decay=weight_decay)
        # State initialization
        for group in self.param_groups:
            for p in group['params']:
                state = self.state[p]
                state['step'] = 0
                state['exp_avg'] = torch.zeros_like(p.data)
                state['exp_avg_sq'] = torch.zeros_like(p.data)

                # share in memory
                state['exp_avg'].share_memory_()
                state['exp_avg_sq'].share_memory_()