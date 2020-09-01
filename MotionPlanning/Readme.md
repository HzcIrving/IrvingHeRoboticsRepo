## Motion Planning Approaches 路径规划方法 

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

Continuous Representation → Discretization(离散化成网格)→ Graph Searching(blind, best-first, A*)

1. Roadmap Methods 
  - Visibility Graph --- 可视化，障碍物用polygon 
  
