# main.py
import config
from models import Vehicle, dl_ff_model, hl_af_model, generate_desired_gaps
from plot_utils import plot_results, create_gif

def run_intra_platoon():
    print(f"Running Intra-platoon simulation (Fig 5) with desired gap: {config.DESIRED_GAP}m...")
    vs = {vid: Vehicle(vid, **data) for vid, data in config.INTRA_INIT_STATES.items()}
    
    for step in range(config.STEPS):
        for v in vs.values():
            v.save_state()
            
        vs['L1'].p += vs['L1'].w * config.DT
        vs['L2'].p += vs['L2'].w * config.DT
        
        f_list = ['F1', 'F2', 'F3', 'F4']
        for i, f_id in enumerate(f_list):
            v = vs[f_id]
            prev = vs[f_list[i-1]] if i > 0 else vs['L1']
            
            # 【核心逻辑】自适应计算：只根据拓扑索引差和用户输入的 DESIRED_GAP 计算相对距离
            r_H_p = generate_desired_gaps(0, i+1, -config.DESIRED_GAP) 
            r_R_p = generate_desired_gaps(5, i+1, -config.DESIRED_GAP)
            r_prev_p = generate_desired_gaps(i, i+1, -config.DESIRED_GAP)
            
            dl_ff_model(v, vs['L1'], vs['L2'], prev, 
                        r_H_p, 0, r_R_p, r_prev_p, 
                        config.PHI, config.ZETA, config.DT)

    plot_results(vs, 'L1', 'Intra-platoon', 'fig5_reproduction')
    create_gif(vs, 'intra_platoon')

def run_inter_platoon():
    print(f"Running Inter-platoon simulation (Fig 6) with desired gap: {config.DESIRED_GAP}m...")
    vs = {vid: Vehicle(vid, **data) for vid, data in config.INTER_INIT_STATES.items()}
    
    for step in range(config.STEPS):
        for v in vs.values():
            v.save_state()
            
        vs['L1'].p += vs['L1'].w * config.DT
        
        f1_list = ['F1', 'F2']
        for i, f_id in enumerate(f1_list):
            v = vs[f_id]
            prev = vs[f1_list[i-1]] if i > 0 else vs['L1']
            r_H_p = generate_desired_gaps(0, i+1, -config.DESIRED_GAP)
            dl_ff_model(v, vs['L1'], vs['L1'], prev, r_H_p, 0, r_H_p, -config.DESIRED_GAP, config.PHI, config.ZETA, config.DT)

        r_LL_p = generate_desired_gaps(0, 3, -config.DESIRED_GAP)
        hl_af_model(vs['L2'], vs['L1'], r_LL_p, 0, config.PSI, config.XI, config.DT)
        
        f2_list = ['F3', 'F4']
        for i, f_id in enumerate(f2_list):
            v = vs[f_id]
            prev = vs[f2_list[i-1]] if i > 0 else vs['L2']
            r_H_p = generate_desired_gaps(0, i+1, -config.DESIRED_GAP)
            dl_ff_model(v, vs['L2'], vs['L2'], prev, r_H_p, 0, r_H_p, -config.DESIRED_GAP, config.PHI, config.ZETA, config.DT)

    plot_results(vs, 'L1', 'Inter-platoon', 'fig6_reproduction')
    create_gif(vs, 'inter_platoon')

if __name__ == "__main__":
    print("="*50)
    print("欢迎使用多智能体边缘计算网络车辆编队仿真系统")
    print("="*50)
    
    # 在这里实现终端交互式输入
    while True:
        try:
            user_input = input("请输入最后编队时每两辆车头之间的期望距离 (单位: 米，推荐 5.4): ")
            # 动态修改 config 里的配置
            config.DESIRED_GAP = float(user_input) 
            break
        except ValueError:
            print("输入格式错误，请输入一个有效的数字！\n")
    
    print(f"\n已收到，将使用 {config.DESIRED_GAP} 米作为编队间距。开始生成，请稍候...\n")
    
    # 执行仿真
    run_intra_platoon()
    run_inter_platoon()
    
    print("\n" + "="*50)
    print("Simulation complete! 仿真完成！相关的 14张子图(.png) 和 动画(.gif) 已成功保存在当前目录下。")
    print("="*50)