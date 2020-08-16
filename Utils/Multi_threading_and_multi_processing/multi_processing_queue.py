#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

# 2个独立进程
# 1个负责写
# 1个负责读
# 实现共享队列queue

from multiprocessing import Process,Queue
import os
import time
import random

# 写数据进程执行的代码
def write(q):
    print('Process to write:{}'.format(os.getpid()))
    for value in ['A','B','C']:
        print('Put %s to queue...' % value )
        q.put(value)
        time.sleep(random.random())

# 读数据进程
def read(q):
    print('Process to read:{}'.format(os.getpid()))
    while True:
        value = q.get(True)
        print('Get %s from queue...' % value)

if __name__ == "__main__":
    # 父进程创建Queue, 并传给各个子进程
    q = Queue()
    pw = Process(target=write,args=(q,))
    pr = Process(target=read,args=(q,))
    # 启动子进程pw, 写入
    pw.start()
    # 启动子进程pr, 读取
    pr.start()
    # 等待pw结束
    pw.join()
    # 终止pr(死循环)
    pr.terminate()