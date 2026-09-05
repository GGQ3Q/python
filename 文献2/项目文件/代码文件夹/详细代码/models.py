# models.py
import numpy as np

class Vehicle:
    
    def __init__(self, v_id, p, q, w, theta):
        self.id = v_id
        self.p = p
        self.q = q
        self.w = w
        self.theta = theta
        # 记录历史轨迹
        self.history = {'p': [], 'q': [], 'w': [], 'theta': []}
        
    def save_state(self):
        self.history['p'].append(self.p)
        self.history['q'].append(self.q)
        self.history['w'].append(self.w)
        self.history['theta'].append(self.theta)

def generate_desired_gaps(leader_idx, follower_idx, gap_unit):
    """
    自适应编队设计：根据车辆在拓扑中的索引自动计算期望相对距离 
    """
    return (follower_idx - leader_idx) * gap_unit

def dl_ff_model(vehicle, leader_H, leader_R, prev_vehicle, r_H_p, r_H_q, r_R_p, r_prev_p, phi, zeta, dt):
    """
    公式 (4) 和 (5): Double Leader-Front Follower (DL-FF) Model [cite: 281, 283]
    """
    # Longitudinal
    w_dot = 0
    if prev_vehicle:
        w_dot -= (phi[0] * (vehicle.p - prev_vehicle.p - r_prev_p) + zeta[0] * (vehicle.w - prev_vehicle.w))
    w_dot -= (phi[1] * (vehicle.p - leader_H.p - r_H_p) + zeta[1] * (vehicle.w - leader_H.w))
    w_dot -= (phi[2] * (vehicle.p - leader_R.p - r_R_p) + zeta[2] * (vehicle.w - leader_R.w))
    
    # Lateral
    theta_dot = -(phi[3] * (vehicle.q - leader_H.q - r_H_q) + zeta[3] * (vehicle.theta - leader_H.theta))
    
    # Update states
    vehicle.p += vehicle.w * dt
    vehicle.q += vehicle.theta * dt
    vehicle.w += w_dot * dt
    vehicle.theta += theta_dot * dt

def hl_af_model(leader, ref_leader, r_LL_p, r_LL_q, psi, xi, dt):
    """
    公式 (6) 和 (7): Head Leader-Avoidance Follower (HL-AF) Model [cite: 292, 362]
    这里简化为 leader 跟踪前一个 MVC 的 leader
    """
    # Longitudinal
    w_dot = -(psi[0] * (leader.p - ref_leader.p - r_LL_p) + xi[0] * (leader.w - ref_leader.w))
    
    # Lateral
    theta_dot = -(psi[2] * (leader.q - ref_leader.q - r_LL_q) + xi[2] * (leader.theta - ref_leader.theta))
    
    leader.p += leader.w * dt
    leader.q += leader.theta * dt
    leader.w += w_dot * dt
    leader.theta += theta_dot * dt