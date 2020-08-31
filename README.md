IrvingHeRoboticsRepo

# 机器人相关仓库... CH Ver. 


### 2020-08-09 
### 1 Localization 有关机器人定位算法的总结库
#### 1.1. [ICP](https://www.zhihu.com/search?type=content&q=Iterative%20Closest%20Point) --- Iterative Closet Point用于匹配点云


### 2. Signal Processing 有关信号处理算法的总结库
#### 2.1 [小波变换Wavelets](https://github.com/HzcIrving/IrvingHeRoboticsRepo/tree/master/Signal_Propressing/Wavelets%E5%B0%8F%E6%B3%A2%E5%8F%98%E6%8D%A2) 

### 3. 强化学习RL 
#### 3.1 [A3C(Asychronous Advantage Actor Critic)](https://github.com/HzcIrving/IrvingHeRoboticsRepo/tree/master/Reinforcement_Learning(for_robots)/A3C)









### 备注 ### 
1. np.repeat(a,repeats,axis=None)/object.repeat(repeats,axis=None) 用于将numpy数组重复
  - axis = 0 沿y轴 实际是增加了行数
  - axis = 1 沿x轴 实际是增加了列数 
  - repeats 可以为一个数，也可以为一个矩阵
  - 具体用法: https://blog.csdn.net/u013555719/article/details/83855965
  

### 关于Utils ### 
Utils里面包含了很多可以用到的小工具，比如多线程，多进程，信号处理...
 
  - Multi_threading_and_multi_processing: 主要是多进程与多线程的实现, 内含有独立的multi-processing与multi-threading的[攻略](https://github.com/HzcIrving/IrvingHeRoboticsRepo/tree/master/Utils/Multi_threading_and_multi_processing)
