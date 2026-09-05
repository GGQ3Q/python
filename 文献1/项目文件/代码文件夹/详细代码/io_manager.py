import json
import numpy as np
import os

def get_config():
    print("="*40)
    print("🚗 欢迎使用 CAV 编队控制仿真系统 🚗")
    print("="*40)
    mode = input("请选择输入模式 (1: 加载 json 文件,  2: 手动逐个输入): ")
    
    if mode == '1':
        file_path = input("请输入json文件路径 (直接回车默认读取 config.json): ") or 'config.json'
        if not os.path.exists(file_path):
            print(f"❌ 找不到文件 {file_path}，请检查！")
            exit()
        with open(file_path, 'r') as f:
            return json.load(f)
            
    elif mode == '2':
        n = int(input("\n请输入跟随车的总数量 (例如 3): "))
        
        # 初始化基础配置参数
        config = {
            "simulation": {"dt": 0.01, "max_time": 20.0, "beta": 1.0, "gamma": 1.0},
            "adaptive_stop": {"pos_error_threshold": 0.05, "vel_error_threshold": 0.05, "hold_time": 1.0},
            "leader": {"pos": [20.0, 50.0], "vel": [6.0, 0.0], "u": [0.0, 0.0]},
            "followers": []
        }
        
        # 循环询问每一辆车的参数
        for i in range(n):
            print(f"\n--- 正在配置第 {i+1} 辆跟随车 ---")
            px = float(input("初始 X 坐标 (例: 10.0): "))
            py = float(input("初始 Y 坐标 (例: 40.0): "))
            vx = float(input("初始 X 速度 (例: 8.0): "))
            vy = float(input("初始 Y 速度 (例: 4.0): "))
            gx = float(input("期望与领航车的纵向(X)间距 (例: -10.0): "))
            gy = float(input("期望与领航车的横向(Y)间距 (例: 0.0): "))
            k = int(input("是否接收领航车信息？(1表示接收，0表示断开): "))
            
            config["followers"].append({
                "id": i+1, "pos": [px, py], "vel": [vx, vy], 
                "desired_gap": [gx, gy], "k": k
            })
            
        # 手动输入模式下，默认生成全连通的网络拓扑 (除了自己到自己是0)
        A = np.ones((n, n))
        np.fill_diagonal(A, 0)
        config["topology_Case1"] = A.tolist()
        
        return config
    else:
        print("❌ 输入错误，程序退出。")
        exit()