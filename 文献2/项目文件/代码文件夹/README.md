# 车辆缩减场景下的多智能体自适应编队仿真系统

本项目是基于 IEEE 论文 **《Sustainable Distributed Adaptive Platoon in Multi-Agent Mobile-Edge Computing Networks for Lane Reduction Scenario》** 开发的 Python 仿真实现 。系统通过复现论文提出的 **SD-M3ASP** 架构，展示了 Connected Automated Vehicles (CAVs) 在车道缩减（2-to-1 Lane Reduction）场景下的自适应编队与协作控制逻辑 。

## 1. 项目背景

在车道缩减场景下，传统的驾驶行为容易导致自发性交通拥堵 。本项目利用软件定义网络 (SDN)、多智能体系统 (MAS) 和移动边缘计算 (MEC) 技术，通过以下核心模型实现稳定的车道协同 ：

- **DL-FF 模型**：双领航员-前向跟随模型，用于内编队（Intra-platoon）稳定性控制 。


- **HL-AF 模型**：头领航员-避障跟随模型，用于多编队间（Inter-platoon）的距离协调 。

 

## 2. 环境要求

运行本项目需要安装以下 Python 库：

- **Python 3.x**
- **NumPy**: 用于矩阵运算与运动学计算。
- **Matplotlib**: 用于生成仿真图表及 GIF 动画。

安装命令：

```Bash
pip install numpy matplotlib
```

## 3. 文件结构

项目采用模块化设计，各文件职责如下：

- **config.py**: 全局参数中心。包含论文 Table III 和 IV 中的初始状态、控制器增益参数（$\phi, \zeta, \psi, \xi$）以及仿真步长设置 。

- **models.py**: 核心运动学实现。封装了论文中的公式 (3) 至 (7)，包含 `Vehicle` 类及自适应间距生成算法 。

- **plot_utils.py**: 数据可视化工具。负责复现论文中的 14 张子图（Fig 5 和 Fig 6 的 c~i 图），并生成动态轨迹 GIF 。

- **main.py**: 系统入口。模拟 SDN 控制器逻辑，执行 `Intra-platoon` 和 `Inter-platoon` 仿真循环，并提供交互式终端输入。

## 4. 核心功能与特性

- **自适应编队设计**：用户无需手动输入所有车的坐标。系统根据用户输入的“期望车头间距”（$F+Z$），利用拓扑索引自动推算期望位置矩阵 $r_{ij} = (j-i) * (F+Z)$ 。

- **交互式运行**：运行程序时，用户可通过终端输入自定义间距，系统将实时动态更新仿真轨迹与结果。


## 5. 运行指南

1. 在终端或 PowerShell 中导航至项目目录。
2. 运行主脚本：
3. 
   ```Bash
   python main.py
   ```
   
3. 按提示输入编队间距（例如输入论文默认的 `10`）。
4. 程序结束后，查看生成的图像文件：

   - `fig5_reproduction.png`: 内编队收敛结果。
   - `fig6_reproduction.png`: 多编队间协作结果。
   - `intra_platoon.gif` / `inter_platoon.gif`: 动态轨迹演示。

## 6. 参考文献

[1] Guangqiang Xie, Biwei Zhong, Haoran Xu, et al. Sustainable Distributed Adaptive Platoon in Multi-Agent Mobile-Edge Computing Networks for Lane Reduction Scenario [J]. Journal of LaTex Class Files, Vol. 14, No. 8, August 2015. 