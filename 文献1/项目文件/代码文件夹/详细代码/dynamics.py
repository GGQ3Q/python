import numpy as np

class PlatoonDynamics:
    def __init__(self, config):
        self.dt = config['simulation']['dt'] # 时间步长
        self.beta = config['simulation']['beta'] # 跟随车之间的速度反馈系数
        self.gamma = config['simulation']['gamma'] # 领航车与跟随车之间的速度反馈系数
        self.A = np.array(config['topology_Case1']) # 邻接矩阵 a_ij
        
        # 领航车状态
        self.x_L = np.array(config['leader']['pos']) # 位置
        self.v_L = np.array(config['leader']['vel']) # 速度
        self.u_L = np.array(config['leader']['u'])# 加速度
        
        # 跟随车状态
        self.n = len(config['followers'])# 跟随车数量
        self.x = np.array([f['pos'] for f in config['followers']]) 
        self.v = np.array([f['vel'] for f in config['followers']])
        self.r = np.array([f['desired_gap'] for f in config['followers']])
        self.K = np.array([f['k'] for f in config['followers']]) # leader连接权重

    def step(self):
        # 存储当前导数用于欧拉更新
        dx = np.zeros_like(self.x)
        dv = np.zeros_like(self.v)

        # 遍历每辆跟随车计算公式(3)
        for i in range(self.n):
            dx[i] = self.v[i]
            
            # 第一部分：与其他跟随车的交互
            sum_ij = np.zeros(2)#创建一个二维0向量，用来存储所有其他车的总影响
            for j in range(self.n):
                if self.A[i, j] > 0: # 如果有直接连接，才计算交互
                    r_ij = self.r[i] - self.r[j] 
                    pos_diff = self.x[i] - self.x[j] - r_ij
                    vel_diff = self.beta * (self.v[i] - self.v[j])
                    sum_ij += self.A[i, j] * (pos_diff + vel_diff)
            
            # 第二部分：与领航车的交互
            leader_term = np.zeros(2)
            if self.K[i] > 0:
                pos_diff_L = self.x[i] - self.x_L - self.r[i]
                vel_diff_L = self.gamma * (self.v[i] - self.v_L)
                leader_term = self.K[i] * (pos_diff_L + vel_diff_L)
            
            # 速度导数公式(3)
            dv[i] = self.u_L - sum_ij - leader_term

        # 领航车状态更新 (匀速运动或按u_L运动)
        self.x_L = self.x_L + self.v_L * self.dt
        self.v_L = self.v_L + self.u_L * self.dt

        # 跟随车状态更新
        self.x = self.x + dx * self.dt
        self.v = self.v + dv * self.dt

    def get_errors(self):
        # 计算误差，用于自适应停止判断
        pos_errors = []
        vel_errors = []
        for i in range(self.n):
            pos_errors.append(self.x[i] - self.x_L - self.r[i])
            vel_errors.append(self.v[i] - self.v_L)
        return pos_errors, vel_errors