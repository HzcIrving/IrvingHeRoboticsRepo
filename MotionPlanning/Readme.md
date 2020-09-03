## Motion Planning Approaches 路径规划方法 

Refs: 
[知乎Motion Planning](https://www.zhihu.com/search?type=content&q=motion%20planning%20)

### 1. From Robotics to autonomous driving 

### 2. Modeling the environment and techniques/环境建模 

- RRT(RRT*...) 
- Lattice  


### 3. Modern Approaches in autonomous driving 

- Darpa Challenge Approaches 
- Lattice in Frenet Frame(自然坐标系) 
- Spiral、Polynomial and Splines 
- Function Optimization (优化一个state) 


## Types of Path Constraints 
### 存在哪些约束呢 ? 
- **Local Constraints**: eg. avoid collision with obstacles(判断两个bounding box有没有相交，进行碰撞检测) 
- **Differential Constraints**: eg.bounded curvature(曲率)--- 你方向盘转多大，车本身存在运动限制, curvature与运动之间的关系 
- **Global Constraints**: 全局约束，在地图中---minimal length 

- 一条path是否平滑？满足无人车的运动要求？ --- 曲率是否连续？(Dubin Path的曲率是不连续的) 
  - It is a combination of smoothness and length 考虑平滑性与长度
  
## Motion Planning Framework 

### SUB Problems: 
- Missiong Plannar : High-Level地图级别规划(Graph Based图搜索实现路径的规划) 

- Behaviour Plannar : 关注交通规则(Traffic Rules)、其他道路交通参与者，决定在在当前场景下应该采取何种操作(如停车让行、加速通过、避让行人等等)； 
  - Behavior Planner的实现方式比较常见的有几种：**有限状态机(Finite State Machines)**、**规则匹配系统(Rule Based System)**、**强化学习系统(Reinforcement Learning)**。

- Local Plannar ： 局部路径规划
  - (1) Path Plannar 路径规划
     - a. Sampling Based Plannar 基于采样 （RRT、RRT*、infor-RRT*...) 
     - b. Variation Plannar 根据Cost Function进行优化，避开障碍物，生成安全轨迹  
     - c. Lattice Plannar 将空间搜索限置在对车辆可行的Action Space (Lattice Plannar、Conformal Lattice Plannar...)  

![image](https://picb.zhimg.com/v2-37976c44ad3dd15fd999baa7c9b20a52_b.jpg) 

  - (2) Velocity Profile Generation 速度曲线生成  --- 需要考虑限速以及速度的平滑性 
![image](https://pic1.zhimg.com/v2-7b37bb4b52583d43426cfeab06c94958_b.jpg)  

- Vehicle Control 车辆控制 


