import numpy as np

class AdaptiveStopper:
    def __init__(self, pos_th, vel_th, hold_time, dt):
        self.pos_th = pos_th # 位置误差阈值（小于多少才行）
        self.vel_th = vel_th # 速度误差阈值
        self.required_steps = int(hold_time / dt) # 所需时间步数
        self.current_steps = 0 # 当前时间步数计数

    def check_stop(self, pos_errors, vel_errors):
        # 计算所有车辆的最大位置和速度误差范数
        max_pos_err = np.max([np.linalg.norm(e) for e in pos_errors])
        max_vel_err = np.max([np.linalg.norm(e) for e in vel_errors])

        if max_pos_err < self.pos_th and max_vel_err < self.vel_th:
            self.current_steps += 1
        else:
            self.current_steps = 0 # 状态打断，重新计数

        return self.current_steps >= self.required_steps