## A3C与A2C Documentation 

### 1. Refs 
[张斯俊专栏---白话强化学习](https://zhuanlan.zhihu.com/c_1215667894253830144)

[知乎CristianoC](https://zhuanlan.zhihu.com/p/77523580)  

### 2. Intro --- A3C与A2C 

#### 2.1 基础，什么是Actor-Critic?  
Actor-Critic网络，基本上是用了两个网络，两个网络有一个共同点，输入状态S: 
- 一个输出策略，负责选择动作action，我们把这个网络成为**Actor**； 
- 一个负责计算每个动作的分数Value，我们把这个网络成为**Critic**。

Actor通过Critic评价的Value，去学习，若Critic给某个action很高的Value，则Actor会调整这个动作的输出概率，反之，若Critic给的Value低，就减少这个概率；从某些角度来说，AC是TD error的PG； 

**注意** 这里的Value是V值不是Q值，原有以下[几点](https://zhuanlan.zhihu.com/p/110998399): 
- 为了避免**正数陷阱**，我们希望Actor的更新权重有正有负。因此，我们把Q值减去他们的均值V。有：Q(s,a)-V(s);
- 为了避免需要预估V值和Q值，我们希望把Q和V统一；由于`Q(s,a) = gamma * V(s') + r - V(s)`。所以我们得到TD-error公式： `TD-error = gamma * V(s') + r - V(s)`; 
- TD-error就是Actor更新策略时候，带权重更新中的权重值；
- 现在Critic不再需要预估Q，而是预估V。而根据马可洛夫链所学，我们知道TD-error就是Critic网络需要的loss，也就是说，Critic函数需要最小化TD-error; 

![Actor-critic](https://pic3.zhimg.com/80/v2-06c9787f9cd9a71d92ce0bbeb871af60_1440w.jpg)

### 2.2 A2C(Advantage Actor Critic)

优势动作评论算法， A2C使用优势函数代替Critic网络中的原始回报，可以作为衡量选取动作值和所有动作平均值好坏的指标。 

![A2C](https://pic1.zhimg.com/80/v2-0ae6011641a20697fbb604dd59e3034a_1440w.jpg)  

`A_pi(s,a) = Q_pi(s,a)-V_pi(s)` 

优势函数的表面意义——动作值函数相比于当前状态值函数的优势； 

> **如果优势函数大于零，则说明该动作比平均动作好，如果优势函数小于零，则说明当前动作还不如平均动作好**  

P.S. 某种程度上来说,A2C又是同步版本的A3C; 


### 2.3 A3C （Asynchronous Advantage Actor Critc) (A2C+Asychronous) 

![Actor-critic](https://pic4.zhimg.com/v2-ea1a5a76eda97b0dd4d7aeccd1410c82_b.jpg)

- A3C中，有一个主网络，还有许多worker，每一个worker也是一个actor-critic的net:
	- Pull: 把主网络的参数直接赋予worker中的网络；
	- Push: 使用各Worker中的梯度，对主网络的参数进行更新；  

- A3C是Google DeepMind 提出的一种解决Actor-Critic不收敛问题的算法。我们知道DQN中很重要的一点是他具有经验池，可以降低数据之间的相关性，而**A3C则提出降低数据之间的相关性的另一种方法**：**异步**。
- A3C会创建多个并行的环境, 让多个拥有副结构的 agent 同时在这些并行环境上更新主结构中的参数. 并行中的 agent 们互不干扰, 而主结构的参数更新受到副结构提交更新的不连续性干扰, 所以更新的相关性被降低, 收敛性提高. 

![算法架构](https://pic1.zhimg.com/80/v2-5c9b3350998f423d5b102e4a70d5adde_1440w.jpg) 

1. A3C的算法实际上就是将Actor-Critic放在了多个线程中进行同步训练. 可以想象成几个人同时在玩一样的游戏, 而他们玩游戏的经验都会同步上传到一个中央大脑. 然后他们又从中央大脑中获取最新的玩游戏方法。

2. 这样, 对于这几个人, 他们的好处是: 中央大脑汇集了所有人的经验, 是最会玩游戏的一个, 他们能时不时获取到中央大脑的必杀招, 用在自己的场景中.

3. 对于中央大脑的好处是: 中央大脑最怕一个人的连续性更新, 不只基于一个人推送更新这种方式能打消这种连续性. 使中央大脑不必像DQN,DDPG那样的记忆库也能很好的更新。

- 中央大脑：拥有`global net`以及他的参数；
- 每个worker有一个`global net`副本`local net`, 可以定时向`global net`推送更新，然后定时从`global net`那获取综合版的更新； 

![A3C](https://pic4.zhimg.com/80/v2-87ab06563111ea06780c83b25f77642e_1440w.jpg)    

- 异步的，谁搞完谁更新 
- 调用sync中的pull，这个worker就会从`global net`中获取到最新的参数； 
- 调用sync中的push, 这个worker就会将自己个人的update送去`global net`;  



