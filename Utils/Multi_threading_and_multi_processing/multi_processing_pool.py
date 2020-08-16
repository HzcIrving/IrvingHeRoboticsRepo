# #! /usr/bin/enc python
# # -*- coding: utf-8 -*-
# # author: Irving He
# # email: 1910646@tongji.edu.cn
#
# # multiprocessing.Pool
# # cpu: 8核
# # 8进程计算9次
# # 8次并行计算+1次重新安排进程进行计算
#
from multiprocessing import Pool
from multiprocessing import cpu_count
import os
import time

def long_time_task(i):
    print("子进程:{} --- 任务{}".format(os.getpid(),i))
    time.sleep(2)
    print("结果:{}".format(8**20))


if __name__ == "__main__":
    print("当前cpu核数:", cpu_count())
    print("当前母进程:{}".format(os.getpid()))
    start = time.time()
    p = Pool(int(cpu_count()))
    for i in range(int(cpu_count())+2):
        p.apply_async(long_time_task,args=(i,))
    print('等待所有子进程完成...')
    p.close()
    p.join()
    end = time.time()
    print("总共用时{}秒".format((end-start)))

