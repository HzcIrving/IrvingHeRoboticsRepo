#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

# MyThread --- 继承+重写
# 实例化两个子线程

import threading
import time

def long_time_task(i):
    time.sleep(2)
    return 8**20

class MyThread(threading.Thread):
    def __init__(self,func,args,name='',):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name

    def run(self):
        print('开始子进程{}'.format(self.name))
        self.result = self.func(self.args[0],)
        print("结果:{}".format(self.result))
        print('结束子进程{}'.format(self.name))

if __name__ == "__main__":
    start = time.time()
    threads = []
    for i in range(1,3):
        t = MyThread(long_time_task,(i,),str(i))
        threads.append(t)

    for  t in threads:
        t.start()
    for t in threads:
        t.join()

    end = time.time()
    print("Total time consump {}s".format((end - start)))

