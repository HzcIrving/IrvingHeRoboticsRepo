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

## 按照前端和后端的架构

### 前端Front-end： Path Finging  

1. Search-Based Path Finding 基于搜索:volcano:
	- Graph Search Basis 图
	- Dijkstra and A* 图搜索
		- Dijkstra algorithm expanded in all directions(高代价)
		- A* expands mainly towards the goal, but does not hedge its bets to ensure optimality(不保证最优); 
	- Jump Point Search 跳点算法(A*的改良版本) SOTA! 
	- 对于任何一个搜索问题，都会有对应的状态空间图；图中节点间的连接可以是有向的也可以是无向的；
	- 图搜索，找一条最短的path； 
	

2. Sampling-Based Path Finding 基于采样的:mountain:
	- PRM: Probabilistic Road Map 概率路线图 
	- RRT: Rapidly-exploring Random Tree(RRT*、Informed RRT*)
		- RRT -> RRT* -> informed RRT*(以起点与终点做椭圆范围---启发式) 
	- Optimal Sampling-based Methods 
	- Advanced Sampling-based Methods 

3. Kinodynamic path finding 考虑车辆/移动机器人自身动力学特性、要求的:ferris_wheel:
	- 会考虑模型动力学模型 from xyo to {sl} frame 
	- State-state Boundary Value Optimal Control Problem 满足亮点边界值约束的优化问题
	- State Lattice Search 状态值搜索---高维Dijkstra and A* 
		- Lattice这种路径是不同"油门“+“方向盘”的不同组合造成的；:frog:
		- SLS 这种算法代价太高， Lattice graph 构建代价太高，搜索过于费时
	- Kinodynamic RRT* 
		- Follow RRT* algorithm 
		- Sample a random state 
		- Solve two state boundary optimal control problem 
			- ***initial state***
			- ***final state*** 
			- :hear_no_evil: 两点的最优路线 
	- Hybrid A* 混合A*(最广泛的一种前端路径搜索算法) 
		- **在每一个栅格里只保留一个状态**; 
		- 把一个机器人简历一个非线性模型；
		- 给定离散化控制量；
		- Follow A* algorithm; 会维护一个栅格网络地图(不同状态) 


### 后端Back-end: Trajectory Generation 轨迹生成

1. Minimum Snap Trajectory Generation 
	- 沿着Path去生成Trajectory; 
		- 若生成轨迹有碰撞，则进行minimum snp 
	- Differential Flatness 微分平坦性
	- Minimum Snap Optimization 
	- Closed-form Solution to Minimum Snap 
	- Time Allocation 时间分配问题 

2. Soft and Hard Constrained Trajectory Optimization 
	- Soft Constrained Trajectory Optimization 软约束轨迹优化
		- ** local replanning ** 
		- APF ... 
	- Hard Constrained Trajectory Optimization 硬约束轨迹优化 
	- 在复杂环境中，生成一条不发生碰撞的轨迹； 

SOTA： MDP、MPC、Reinforcement Learning ... 

### Map Representation 常用的地图表达形式  

1. MAP :frog:
	- Data Structure 
	- Fusion Method  

#### 常用的地图形式 

1. Occupancy Grid Map 
	- 2D、3D、2.5
	- Dense 
	- 直接索引即可，但是费空间

2. Octo-Map 
	- 八叉树地图 
	- 没有障碍物的地方，很大的方块； 
	- 有障碍物的地方，进行递归切分，知道可以表示障碍物；
	- Indirect Index Query 

3. Voxel Hashing 

4. Point Cloud Map 
	- 点云
	- 激光雷达，传感器的原始测量的集合
	- 点是无序的，无法进行Index Query(索引查询)
	- [PCL库(使用方法、示例、tutorial...)](https://pointclouds.org/)

5. TSDF Map (Truncated(截断) Signed Distance Functions) 距离场

6. ESDF Map (Euclidean Signed Distance Functions) 
	- Incremental Update, Global Map 
	- VoxBlox
	- Fiesta
	- TRR's Local Map
	- 势场: 红色---近 绿色---远
	
		



