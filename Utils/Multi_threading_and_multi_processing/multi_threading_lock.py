#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

import threading

class Account:
    def __init__(self):
        self.balance = 0  # 共享变量，不能被随意改乱

    def add(self,lock):
        # 获得锁
        lock.acquire()
        for i in range(0,100000):
            self.balance += 5
        # 释放锁
        lock.release()

    def delete(self,lock):
        # 获得锁
        lock.acquire()
        for i in range(0,100000):
            self.balance -= 1
        # 释放锁
        lock.release()

if __name__ == "__main__":
    account = Account()
    lock = threading.Lock()
    # 创建线程
    thread_add = threading.Thread(target=account.add,args=(lock,),name='Add')
    thread_del = threading.Thread(target=account.delete,args=(lock,),name='Delete')

    # 启动
    thread_add.start()
    thread_del.start()

    # 等待结束
    thread_add.join()
    thread_del.join()

    print("最终余额：",account.balance)
