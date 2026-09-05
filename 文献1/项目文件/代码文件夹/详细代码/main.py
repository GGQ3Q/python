
from io_manager import get_config
from dynamics import PlatoonDynamics
from adaptive_stop import AdaptiveStopper
from visualizer import Visualizer

def main():
    # 1. 调用交互界面，获取配置项（无论手动输入还是读文件，都在这里搞定）
    config = get_config()
        
    dt = config['simulation']['dt']
    max_time = config['simulation']['max_time'] 
    
    # 2. 初始化动力学（dynamic文件）与自适应（adaptive文件）模块
    system = PlatoonDynamics(config)# 按照所需要求建立了一个车队
    stopper = AdaptiveStopper( # 检测我们的车队是否符合稳定指标，以下为我们的稳定指标数值
        config['adaptive_stop']['pos_error_threshold'],
        config['adaptive_stop']['vel_error_threshold'],
        config['adaptive_stop']['hold_time'],
        dt
    )
    
    # 数据记录器
    history = {'time': [], 'x': [], 'v': [], 'xL': [], 'vL': [], 'r': system.r}
    
   
    print("开始仿真...")
    time = 0.0
    
    #设置一个绝对安全上限（比如100秒），防止参数设置错误导致死循环卡死电脑
    absolute_max_time = 100.0 
    
    # 将原来的 while time <= max_time: 改为无限循环，由内部逻辑控制跳出
    while True:
        # 1. 记录数据
        history['time'].append(time)
        history['x'].append(system.x.copy())
        history['v'].append(system.v.copy())
        history['xL'].append(system.x_L.copy())
        history['vL'].append(system.v_L.copy())
        
        # 2. 判断是否提前结束（你之前看懂的那部分）
        pos_err, vel_err = system.get_errors()
        if stopper.check_stop(pos_err, vel_err):
            print(f"✅ 编队已在 {time:.2f} 秒时自适应完成并稳定，结束仿真！")
            break
            
        # 3. 判断是否需要自动延时（核心新增逻辑！）
        if time >= max_time:
            print(f"⚠️ 达到预设最大时间 {max_time}s，但编队仍未完成，自动延长 10 秒...")
            max_time += 10.0  # 每次不够就自动加 10 秒
            
            # 安全兜底逻辑：如果一直延时到了绝对上限，说明可能永远排不好了
            if max_time > absolute_max_time:
                print(f"❌ 已达到绝对安全上限 {absolute_max_time}s 仍未收敛，强制结束！")
                print("   👉 建议检查：是否有些车辆的 k=0 且没和其他车连通？或者增益 beta/gamma 太小？")
                break
                
        # 4. 迭代步进
        system.step()
        time += dt
        
    

    # 5. 数据可视化
    viz = Visualizer(history)
    viz.plot_fig4_position_trajectory() # 画轨迹图
    viz.plot_fig5_gaps()                # 画间距误差图
    viz.plot_fig6_velocities()          # 画速度共识图
    viz.generate_gif()                  # 生成动图

if __name__ == "__main__":
    main()