import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class Visualizer:
    def __init__(self, history):
        self.history = history
        self.times = history['time']
        # 转置数据便于画图 [time, vehicle, coordinate]
        self.x_hist = np.array(history['x'])
        self.v_hist = np.array(history['v'])
        self.xL_hist = np.array(history['xL'])
        self.vL_hist = np.array(history['vL'])
        self.r = history['r']

    def plot_fig4_position_trajectory(self):
        plt.figure(figsize=(10, 6))
        # 绘制跟随车
        labels = ['Vehicle i', 'Vehicle i+1', 'Vehicle i+2']
        colors = ['blue', 'black', 'brown']
        for i in range(3):
            plt.plot(self.x_hist[:, i, 0], self.x_hist[:, i, 1], label=labels[i], color=colors[i])
        # 绘制领航车
        plt.plot(self.xL_hist[:, 0], self.xL_hist[:, 1], label='Leader', color='magenta')
        
        plt.xlabel('X Position (m)')
        plt.ylabel('Y Position (m)')
        plt.title('Fig. 4 The position trajectories')
        plt.legend()
        plt.grid(True)
        plt.show()

    def plot_fig5_gaps(self):
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        labels = ['Vehicle i', 'Vehicle i+1', 'Vehicle i+2']
        colors = ['blue', 'black', 'brown']
        
        for i in range(3):
            # 实际位置减去领航车位置，反映纵向/横向间距动态
            lon_gap = self.x_hist[:, i, 0] - self.xL_hist[:, 0]
            lat_gap = self.x_hist[:, i, 1] - self.xL_hist[:, 1]
            ax1.plot(self.times, lon_gap, label=labels[i], color=colors[i])
            ax2.plot(self.times, lat_gap, label=labels[i], color=colors[i])
            
        ax1.axhline(0, color='magenta', label='Leader')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('Longitudinal Gap (m)')
        ax1.set_title('Fig. 5(a) The longitudinal gap')
        ax1.legend()

        ax2.axhline(0, color='magenta', label='Leader')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Lateral Gap (m)')
        ax2.set_title('Fig. 5(b) The lateral gap')
        ax2.legend()
        plt.tight_layout()
        plt.show()
    
    def plot_fig6_velocities(self):
        # 创建上下两个子图，分别对应 Fig. 6(a) 和 (b)
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 10))
        labels = ['Vehicle i', 'Vehicle i+1', 'Vehicle i+2']
        colors = ['blue', 'black', 'brown']
        
        for i in range(3): # 假设有3辆跟随车
            # 绘制跟随车的 X 方向速度
            ax1.plot(self.times, self.v_hist[:, i, 0], label=labels[i], color=colors[i])
            # 绘制跟随车的 Y 方向速度
            ax2.plot(self.times, self.v_hist[:, i, 1], label=labels[i], color=colors[i])
            
        # 绘制领航车的速度作为基准线 (对应图中的粉色直线)
        ax1.plot(self.times, self.vL_hist[:, 0], color='magenta', label='Leader')
        ax1.set_xlabel('Time (s)')
        ax1.set_ylabel('X-Velocity (m/s)')
        ax1.set_title('Fig. 6(a) x-velocity')
        ax1.legend()

        ax2.plot(self.times, self.vL_hist[:, 1], color='magenta', label='Leader')
        ax2.set_xlabel('Time (s)')
        ax2.set_ylabel('Y-Velocity (m/s)')
        ax2.set_title('Fig. 6(b) y-velocity')
        ax2.legend()
        
        plt.tight_layout()
        plt.show()

    def generate_gif(self, filename="platoon_simulation.gif"):
        print("正在拼命渲染 GIF 动图，请稍候...") # 增加提示，防止误以为卡死
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        # 【修改1：动态计算 X 和 Y 的最大/最小值，加上留白边界，防止车辆跑出画面】
        x_min = min(np.min(self.x_hist[:, :, 0]), np.min(self.xL_hist[:, 0])) - 10
        x_max = max(np.max(self.x_hist[:, :, 0]), np.max(self.xL_hist[:, 0])) + 10
        y_min = min(np.min(self.x_hist[:, :, 1]), np.min(self.xL_hist[:, 1])) - 10
        y_max = max(np.max(self.x_hist[:, :, 1]), np.max(self.xL_hist[:, 1])) + 10
        
        ax.set_xlim(x_min, x_max)
        ax.set_ylim(y_min, y_max)
        
        scats = []
        colors = ['blue', 'black', 'brown']
        for i in range(3):
            scat, = ax.plot([], [], 'o', color=colors[i], markersize=8)
            scats.append(scat)
        leader_scat, = ax.plot([], [], '*', color='magenta', markersize=12)

        def init():
            for scat in scats:
                scat.set_data([], [])
            leader_scat.set_data([], [])
            return scats + [leader_scat]

        def update(frame):
            for i in range(3):
                # Matplotlib 的 set_data 需要传入序列 (如列表)
                scats[i].set_data([self.x_hist[frame, i, 0]], [self.x_hist[frame, i, 1]])
            leader_scat.set_data([self.xL_hist[frame, 0]], [self.xL_hist[frame, 1]])
            ax.set_title(f'Time: {self.times[frame]:.2f}s')
            return scats + [leader_scat]

        # 降采样生成GIF加快速度
        step = max(1, len(self.times) // 200)
        frames = range(0, len(self.times), step)
        
        ani = FuncAnimation(fig, update, frames=frames, init_func=init, blit=False)
        
        # 保存动图
        ani.save(filename, writer='pillow', fps=20)
        
        # 【修改2：显式关闭图像，释放内存，确保文件正确写入并闭合】
        plt.close(fig) 
        
        print(f"✅ GIF 已成功保存至 {filename}")