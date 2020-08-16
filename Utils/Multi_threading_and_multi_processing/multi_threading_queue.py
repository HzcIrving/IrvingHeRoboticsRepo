#! /usr/bin/enc python
# -*- coding: utf-8 -*-
# author: Irving He 
# email: 1910646@tongji.edu.cn

from queue import Queue
import random,threading,time

# 生产者Producer
class Producer(threading.Thread):
    def __init__(self,name,queue):
        threading.Thread.__init__(self,name=name)
        self.queue = queue

    def run(self):
        for i in range(1,5):
            print("{}生产{}到Queue了！".format(self.getName(),i))
            self.queue.put(i)
            time.sleep(random.randrange(10)/5)
        print("%s 结束!" % self.getName())

# 消费者Consumer
class Consumer(threading.Thread):
    def __init__(self,name,queue):
        threading.Thread.__init__(self,name=name)
        self.queue = queue

    def run(self):
        for i in range(1,5):
            val = self.queue.get()
            print("{}正在消费Queue中的{}".format(self.getName(),val))
            time.sleep(random.randrange(10))
        print("%s 结束!" % self.getName())

def main():
    queue = Queue()
    producer = Producer('Producer',queue)
    consumer = Consumer('Consumer',queue)

    producer.start()
    consumer.start()

    producer.join()
    consumer.join()

    print('所有线程结束!')

if __name__ == '__main__':
    main()
