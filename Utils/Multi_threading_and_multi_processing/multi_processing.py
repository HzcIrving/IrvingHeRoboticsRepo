#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

# 多进程
# 多cpu计算指数

import time
import os

from multiprocessing import Process # 添加进程

def long_time_task():
    print("当前进程pid:{}".format(os.getpid())) # 获得pid号
    time.sleep(2) # sleep 2s
    print("结果:{}".format(8**20))

def long_time_task2(i):
    print("子进程:{}---任务{}".format(os.getpid(),i)) # 获得pid号
    time.sleep(2) # sleep 2s
    print("结果:{}".format(8**20))

if __name__ == "__main__":

    # 单进程
    print("---------单进程-------------------")
    print("当前母进程:{}".format(os.getpid()))
    start = time.time()
    for i in range(2): # 循环2次，即需要打印两次
        long_time_task()

    end = time.time()
    print("用时{}s",format((end-start)))

    print("---------多进程，两个进程进行两次循环----------")
    print("当前母进程:{}".format(os.getpid()))
    start2= time.time()
    p1 = Process(target=long_time_task2,args=(1,)) # process 1
    p2 = Process(target=long_time_task2,args=(2,)) # process 2
    print("等待所有子进程完成")
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    end2 = time.time()
    print("总共用时{}秒".format((end2-start2)))

