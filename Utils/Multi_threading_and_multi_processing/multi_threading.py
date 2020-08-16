#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

# Python 多线程
# 1.设置GIL
# 2.切换到一个线程去执行
# 3.运行
# 4.把线程设置为睡眠状态
# 5.解锁GIL
# 6.repeat ...

import threading
import time

def long_time_task(i):
    print('当前子线程: {} 任务{}'.format(threading.current_thread().name, i))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


if __name__ == "__main__":
    start =time.time()
    print('这是主线程：{}'.format(threading.current_thread().name))
    thread_list = []
    for i in range(1,3):
        t = threading.Thread(target=long_time_task,args=(i,))
        thread_list.append(t)

    for t in thread_list:
        t.start()
    for t in thread_list:
        t.join()

    end = time.time()
    print("总共用时{}秒".format((end - start)))
