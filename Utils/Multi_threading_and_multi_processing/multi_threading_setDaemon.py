#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

import threading
import time


def long_time_task():
    print('当子线程: {}'.format(threading.current_thread().name))
    time.sleep(2)
    print("结果: {}".format(8 ** 20))


if __name__=='__main__':
    start = time.time()
    print('这是主线程：{}'.format(threading.current_thread().name))
    for i in range(5):
        t = threading.Thread(target=long_time_task, args=())
        t.setDaemon(True) ### 希望一个主线程结束时不再执行子线程
        t.start()

    end = time.time()
    print("总共用时{}秒".format((end - start)))