# plot_utils.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def plot_results(vehicles, leader_id, title_prefix, save_name):
    """
    复现论文中的 (c) ~ (i) 7个子图 (包含完整正确的 e 和 h 的线型与双Leader参照)
    """
    time = np.linspace(0, 15, len(vehicles[leader_id].history['p']))
    
    fig, axs = plt.subplots(3, 3, figsize=(15, 10))
    fig.suptitle(f'{title_prefix} Results', fontsize=16)
    
    # (c) Position Trajectories (X vs Y)
    ax_traj = axs[0, 2]
    for v_id, v in vehicles.items():
        ax_traj.plot(v.history['p'], v.history['q'], label=v_id)
        ax_traj.scatter(v.history['p'][0], v.history['q'][0], marker='o') # Start
    ax_traj.set_title('(c) Position trajectories')
    ax_traj.set_xlabel('X Position (m)')
    ax_traj.set_ylabel('Y Position (m)')
    ax_traj.legend()
    
    # (d) X Position
    ax_x = axs[1, 0]
    for v_id, v in vehicles.items():
        ax_x.plot(time, v.history['p'], label=v_id)
    ax_x.set_title('(d) X position')
    ax_x.set_xlabel('Time (s)')
    
    # (e) Longitudinal Gap
    ax_long_gap = axs[1, 1]
    ref_p_L1 = np.array(vehicles['L1'].history['p'])
    if 'L2' in vehicles:
        ref_p_L2 = np.array(vehicles['L2'].history['p'])
    
    f_list = ['F1', 'F2', 'F3', 'F4']
    colors = ['tab:blue', 'tab:orange', 'tab:green', 'tab:red']
    # 绘制 L1 相对间距 (实线)
    for i, f_id in enumerate(f_list):
        if f_id in vehicles:
            v_p = np.array(vehicles[f_id].history['p'])
            ax_long_gap.plot(time, ref_p_L1 - v_p, label=f'L1-{f_id}', color=colors[i], linestyle='-')
            
    # 绘制 L2 相对间距 (点划线)
    colors_l2 = ['tab:blue', 'tab:orange', 'tab:green', 'tab:purple']
    for i, f_id in enumerate(f_list):
        if 'L2' in vehicles and f_id in vehicles:
            v_p = np.array(vehicles[f_id].history['p'])
            ax_long_gap.plot(time, ref_p_L2 - v_p, label=f'L2-{f_id}', color=colors_l2[i], linestyle='-.')
            
    ax_long_gap.set_title('(e) Longitudinal gap')
    ax_long_gap.set_xlabel('Time (s)')
    ax_long_gap.legend(fontsize='x-small', loc='center right')
    
    # (f) X Velocity 
    ax_vx = axs[1, 2]
    for v_id, v in vehicles.items():
        ax_vx.plot(time, v.history['w'], label=v_id)
    ax_vx.set_title('(f) X velocity')
    ax_vx.set_xlabel('Time (s)')
    
    # (g) Y Position 
    ax_y = axs[2, 0]
    for v_id, v in vehicles.items():
        ax_y.plot(time, v.history['q'], label=v_id)
    ax_y.set_title('(g) Y position')
    ax_y.set_xlabel('Time (s)')
    
    # (h) Lateral Gap
    ax_lat_gap = axs[2, 1]
    ref_q_L1 = np.array(vehicles['L1'].history['q'])
    if 'L2' in vehicles:
        ref_q_L2 = np.array(vehicles['L2'].history['q'])
        
    for i, f_id in enumerate(f_list):
        if f_id in vehicles:
            v_q = np.array(vehicles[f_id].history['q'])
            ax_lat_gap.plot(time, ref_q_L1 - v_q, label=f'L1-{f_id}', color=colors[i], linestyle='-')
            
    for i, f_id in enumerate(f_list):
        if 'L2' in vehicles and f_id in vehicles:
            v_q = np.array(vehicles[f_id].history['q'])
            ax_lat_gap.plot(time, ref_q_L2 - v_q, label=f'L2-{f_id}', color=colors_l2[i], linestyle='-.')
            
    ax_lat_gap.set_title('(h) Lateral gap')
    ax_lat_gap.set_xlabel('Time (s)')
    ax_lat_gap.legend(fontsize='x-small', loc='center right')
    
    # (i) Y Velocity
    ax_vy = axs[2, 2]
    for v_id, v in vehicles.items():
        ax_vy.plot(time, v.history['theta'], label=v_id)
    ax_vy.set_title('(i) Y velocity')
    ax_vy.set_xlabel('Time (s)')

    # 隐藏无用的左上角子图
    axs[0, 0].axis('off')
    axs[0, 1].axis('off')
    
    plt.tight_layout()
    plt.savefig(f'{save_name}.png')
    plt.close()

def create_gif(vehicles, save_name):
    """
    绘制动态车队变化并保存为 GIF
    """
    fig, ax = plt.subplots(figsize=(10, 3))
    
    colors = plt.cm.get_cmap('tab10', len(vehicles))
    scatters = []
    for i, v_id in enumerate(vehicles.keys()):
        scat = ax.scatter([], [], color=colors(i), s=100, label=v_id, marker='s')
        scatters.append(scat)
        
    ax.set_xlim(0, 300)
    ax.set_ylim(-1, 4)
    ax.legend(loc='upper right')
    ax.set_title("Platoon Convergence Animation")
    ax.set_xlabel("Longitudinal Position (m)")
    ax.set_ylabel("Lateral Position (m)")
    
    def update(frame):
        # 动态更新 x 轴范围以跟随车队
        current_x_max = 0
        for i, (v_id, v) in enumerate(vehicles.items()):
            x = v.history['p'][frame]
            y = v.history['q'][frame]
            scatters[i].set_offsets(np.c_[x, y])
            if x > current_x_max: current_x_max = x
            
        ax.set_xlim(current_x_max - 80, current_x_max + 20)
        return scatters

    num_frames = len(vehicles[list(vehicles.keys())[0]].history['p'])
    # 抽帧加快 GIF 生成速度
    anim = animation.FuncAnimation(fig, update, frames=range(0, num_frames, 5), interval=50, blit=True)
    anim.save(f'{save_name}.gif', writer='pillow', fps=20)
    plt.close()