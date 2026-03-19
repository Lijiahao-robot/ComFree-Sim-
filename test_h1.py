cat > test_h1.py << 'EOF'
#!/usr/bin/env python3
"""
Unitree H1 人形机器人测试
"""

import os
import sys
import numpy as np
import time

try:
    import mujoco as mj
    import mujoco.viewer
except ImportError:
    print("❌ 请安装 MuJoCo: pip install mujoco")
    sys.exit(1)

print("=" * 70)
print("Unitree H1 人形机器人仿真测试")
print("=" * 70)

# H1 模型路径
H1_PATH = os.path.expanduser("~/mujoco_menagerie/unitree_h1/scene.xml")

if not os.path.exists(H1_PATH):
    print(f"❌ 找不到 H1 模型: {H1_PATH}")
    print("请确认 mujoco_menagerie 已安装:")
    print("  git clone https://github.com/google-deepmind/mujoco_menagerie")
    sys.exit(1)

print(f"✅ 找到 H1 模型")

# 加载模型
model = mj.MjModel.from_xml_path(H1_PATH)
data = mj.MjData(model)

print(f"📊 模型信息:")
print(f"   自由度 (nv): {model.nv}")
print(f"   位置维度 (nq): {model.nq}")
print(f"   控制维度 (nu): {model.nu}")
print(f"   关节数 (njnt): {model.njnt}")
print(f"   刚体数 (nbody): {model.nbody}")

# 关节映射
joints = {}
for i in range(model.njnt):
    name = mj.mj_id2name(model, mj.mjtObj.mjOBJ_JOINT, i)
    if name:
        joints[name] = {
            'id': i,
            'qpos_idx': model.jnt_qposadr[i],
            'dof_idx': model.jnt_dofadr[i] if model.jnt_dofadr[i] >= 0 else -1,
            'type': model.jnt_type[i],
            'range': (model.jnt_range[i*2], model.jnt_range[i*2+1])
        }

print(f"\n🔧 检测到 {len(joints)} 个关节:")

# 分类显示
categories = {
    'leg': ['hip', 'knee', 'ankle'],
    'arm': ['shoulder', 'elbow', 'wrist'],
    'torso': ['waist', 'torso'],
    'head': ['head']
}

for cat, keywords in categories.items():
    found = [n for n in joints.keys() if any(k in n.lower() for k in keywords)]
    if found:
        print(f"\n  🦵 {cat.upper()} ({len(found)}个):")
        for n in found[:6]:
            info = joints[n]
            print(f"    {n:20s} qpos[{info['qpos_idx']:2d}] range[{info['range'][0]:+.2f}, {info['range'][1]:+.2f}]")

# 重置到初始姿势
mj.mj_resetDataKeyframe(model, data, 0)
home_qpos = data.qpos.copy()
home_qvel =2d}] range[{info['range'][0]:+.2f}, {info['range'][1]:+.2f}]")

# 重置到初始姿势
mj.mj_resetDataKeyframe(model, data, 0)
home_qpos = data.qpos.copy()
home_qvel = data.qvel.copy()

print(f"\n📏 初始状态:")
print(f"   位置: ({data.qpos[0]:.3f}, {data.qpos[1]:.3f}, {data.qpos[2]:.3f})")
print(f"   高度: {data.qpos[2]:.3f}m")

# 启动查看器
print("\n🖥️  启动查看器...")
viewer = mujoco.viewer.launch_passive(model, data)
viewer.cam.distance = 3.5
viewer.cam.azimuth = 135
viewer.cam.elevation = -20
viewer.cam.lookat[:] = [0, 0, 0.9]

# 稳定阶段
print("⏳ 物理稳定中...")
for i in range(300):
    mj.mj_step(model, data)
    if i % 50 == 0:
        viewer.sync()
    time.sleep(0.005)

print(f"✅ 稳定后高度: {data2d}] range[{info['range'][0]:+.2f}, {info['range'][1]:+.2f}]")

# 重置到初始姿势
mj.mj_resetDataKeyframe(model, data, 0)
home_qpos = data.qpos.copy()
home_qvel = data.qvel.copy()

print(f"\n📏 初始状态:")
print(f"   位置: ({data.qpos[0]:.3f}, {data.qpos[1]:.3f}, {data.qpos[2]:.3f})")
print(f"   高度: {data.qpos[2]:.3f}m")

# 启动查看器
print("\n🖥️  启动查看器...")
viewer = mujoco.viewer.launch_passive(model, data)
viewer.cam.distance = 3.5
viewer.cam.azimuth = 135
viewer.cam.elevation = -20
viewer.cam.lookat[:] = [0, 0, 0.9]

# 稳定阶段
print("⏳ 物理稳定中...")
for i in range(300):
    mj.mj_step(model, data)
    if i % 50 == 0:
        viewer.sync()
    time.sleep(0.005)

print(f"✅ 稳定后高度: {data.qpos[2]:.3f}m")

# ============================================
# 测试 1: 站立平衡 (PD控制)
# ============================================
print("\n🧪 测试 1: PD控制站立平衡")

def pd_control(kp=100, kd=10):
    """计算PD控制力矩"""
    ctrl = np.zeros(model.nu)
    
    for i in range(model.nu):
        # 找到对应的关节
       2d}] range[{info['range'][0]:+.2f}, {info['range'][1]:+.2f}]")

# 重置到初始姿势
mj.mj_resetDataKeyframe(model, data, 0)
home_qpos = data.qpos.copy()
home_qvel = data.qvel.copy()

print(f"\n📏 初始状态:")
print(f"   位置: ({data.qpos[0]:.3f}, {data.qpos[1]:.3f}, {data.qpos[2]:.3f})")
print(f"   高度: {data.qpos[2]:.3f}m")

# 启动查看器
print("\n🖥️  启动查看器...")
viewer = mujoco.viewer.launch_passive(model, data)
viewer.cam.distance = 3.5
viewer.cam.azimuth = 135
viewer.cam.elevation = -20
viewer.cam.lookat[:] = [0, 0, 0.9]

# 稳定阶段
print("⏳ 物理稳定中...")
for i in range(300):
    mj.mj_step(model, data)
    if i % 50 == 0:
        viewer.sync()
    time.sleep(0.005)

print(f"✅ 稳定后高度: {data.qpos[2]:.3f}m")

# ============================================
# 测试 1: 站立平衡 (PD控制)
# ============================================
print("\n🧪 测试 1: PD控制站立平衡")

def pd_control(kp=100, kd=10):
    """计算PD控制力矩"""
    ctrl = np.zeros(model.nu)
    
    for i in range(model.nu):
        # 找到对应的关节
        if i < len(joints):
            joint_name = list(joints.keys())[i] if i < len(joints) else None
            if joint_name:
                q_idx = joints[joint_name]['qpos_idx']
                v_idx = joints[joint_name]['dof_idx']
                
                if q_idx < len(data.qpos) and v_idx >= 0 and v_idx < len(data.qvel):
                    q = data.qpos[q_idx]
                    q0 = home_qpos[q_idx]
                    dq = data.qvel[v_idx]
                    
                    # PD: tau = kp*(q0-q) - kd*dq
                    ctrl[i] = kp * (q0 - q) - kd * dq
    
    return np.clip(ctrl, -80, 80)  # 限幅

# 测试站立
for step in range(1000):
   2d}] range[{info['range'][0]:+.2f}, {info['range'][1]:+.2f}]")

# 重置到初始姿势
mj.mj_resetDataKeyframe(model, data, 0)
home_qpos = data.qpos.copy()
home_qvel = data.qvel.copy()

print(f"\n📏 初始状态:")
print(f"   位置: ({data.qpos[0]:.3f}, {data.qpos[1]:.3f}, {data.qpos[2]:.3f})")
print(f"   高度: {data.qpos[2]:.3f}m")

# 启动查看器
print("\n🖥️  启动查看器...")
viewer = mujoco.viewer.launch_passive(model, data)
viewer.cam.distance = 3.5
viewer.cam.azimuth = 135
viewer.cam.elevation = -20
viewer.cam.lookat[:] = [0, 0, 0.9]

# 稳定阶段
print("⏳ 物理稳定中...")
for i in range(300):
    mj.mj_step(model, data)
    if i % 50 == 0:
        viewer.sync()
    time.sleep(0.005)

print(f"✅ 稳定后高度: {data.qpos[2]:.3f}m")

# ============================================
# 测试 1: 站立平衡 (PD控制)
# ============================================
print("\n🧪 测试 1: PD控制站立平衡")

def pd_control(kp=100, kd=10):
    """计算PD控制力矩"""
    ctrl = np.zeros(model.nu)
    
    for i in range(model.nu):
        # 找到对应的关节
        if i < len(joints):
            joint_name = list(joints.keys())[i] if i < len(joints) else None
            if joint_name:
                q_idx = joints[joint_name]['qpos_idx']
                v_idx = joints[joint_name]['dof_idx']
                
                if q_idx < len(data.qpos) and v_idx >= 0 and v_idx < len(data.qvel):
                    q = data.qpos[q_idx]
                    q0 = home_qpos[q_idx]
                    dq = data.qvel[v_idx]
                    
                    # PD: tau = kp*(q0-q) - kd*dq
                    ctrl[i] = kp * (q0 - q) - kd * dq
    
    return np.clip(ctrl, -80, 80)  # 限幅

# 测试站立
for step in range(1000):
    ctrl = pd_control(kp=80, kd=8)
    data.ctrl[:] = ctrl
    mj.mj_step(model, data)
    viewer.sync()
    
    if step % 200 == 0:
        print(f"   Step {step:4d} | 高度: {data.qpos[2]:.3f}m | 俯仰: {np.arctan2(2*(data.qpos[3]*data.qpos[5] - data.qpos[6]*data.qpos[4]), 1-2*(data.qpos2d}] range[{info['range'][0]:+.2f}, {info['range'][1]:+.2f}]")

# 重置到初始姿势
mj.mj_resetDataKeyframe(model, data, 0)
home_qpos = data.qpos.copy()
home_qvel = data.qvel.copy()

print(f"\n📏 初始状态:")
print(f"   位置: ({data.qpos[0]:.3f}, {data.qpos[1]:.3f}, {data.qpos[2]:.3f})")
print(f"   高度: {data.qpos[2]:.3f}m")

# 启动查看器
print("\n🖥️  启动查看器...")
viewer = mujoco.viewer.launch_passive(model, data)
viewer.cam.distance = 3.5
viewer.cam.azimuth = 135
viewer.cam.elevation = -20
viewer.cam.lookat[:] = [0, 0, 0.9]

# 稳定阶段
print("⏳ 物理稳定中...")
for i in range(300):
    mj.mj_step(model, data)
    if i % 50 == 0:
        viewer.sync()
    time.sleep(0.005)

print(f"✅ 稳定后高度: {data.qpos[2]:.3f}m")

# ============================================
# 测试 1: 站立平衡 (PD控制)
# ============================================
print("\n🧪 测试 1: PD控制站立平衡")

def pd_control(kp=100, kd=10):
    """计算PD控制力矩"""
    ctrl = np.zeros(model.nu)
    
    for i in range(model.nu):
        # 找到对应的关节
        if i < len(joints):
            joint_name = list(joints.keys())[i] if i < len(joints) else None
            if joint_name:
                q_idx = joints[joint_name]['qpos_idx']
                v_idx = joints[joint_name]['dof_idx']
                
                if q_idx < len(data.qpos) and v_idx >= 0 and v_idx < len(data.qvel):
                    q = data.qpos[q_idx]
                    q0 = home_qpos[q_idx]
                    dq = data.qvel[v_idx]
                    
                    # PD: tau = kp*(q0-q) - kd*dq
                    ctrl[i] = kp * (q0 - q) - kd * dq
    
    return np.clip(ctrl, -80, 80)  # 限幅

# 测试站立
for step in range(1000):
    ctrl = pd_control(kp=80, kd=8)
    data.ctrl[:] = ctrl
    mj.mj_step(model, data)
    viewer.sync()
    
    if step % 200 == 0:
        print(f"   Step {step:4d} | 高度: {data.qpos[2]:.3f}m | 俯仰: {np.arctan2(2*(data.qpos[3]*data.qpos[5] - data.qpos[6]*data.qpos[4]), 1-2*(data.qpos[5]**2+data.qpos[6]**2)):.3f}")

# ============================================
# 测试 2: 原地踏步 (正弦波)
# ============================================
print("\n🧪 测试 2: 原地踏步行走")

# 找到腿部关节
left_leg = [n for n in joints.keys() if 'left' in n.lower() and any(k in n.lower() for k in ['hip', 'knee', 'ankle'])]
right_leg = [n for n in joints.keys() if 'right' in n.lower() and any(k in n.lower() for k in ['hip', 'knee', 'ankle'])]

print(f"   左腿关节: {left_leg}")
print(f"   右腿关节: {right_leg}")

# 重置
mj.mj_resetDataKeyframe(model, data, 0)

step_count = 0
start_x = data.qpos[0]

try:
    while viewer.is_running() and step_count < 3000:
        t = data.time
        
        # 步态参数
        freq = 1.5  # 步频
        phase = 2 * np.pi * freq * t
        
        ctrl = np.zeros(model.nu)
        
        # 对腿部施加正弦波
        for i, name in enumerate(joints.keys()):
            if i >= model.nu:
                break
                
            if name in left_leg:
                # 左腿
                if 'hip_pitch' in name:
                    ctrl[i] = 30 * np.sin(phase)  # 髋关节前后
                elif 'knee' in name:
                    ctrl[i] = 20 * max(0, np.sin(phase - 0.5))  # 膝关节弯曲
                elif 'ankle' in name:
                    ctrl[i] = 10 * np.sin(phase - 1.0)  # 踝关节补偿
                    
            elif name in right_leg:
                # 右腿 (相位差180度)
                if '2d}] range[{info['range'][0]:+.2f}, {info['range'][1]:+.2f}]")

# 重置到初始姿势
mj.mj_resetDataKeyframe(model, data, 0)
home_qpos = data.qpos.copy()
home_qvel = data.qvel.copy()

print(f"\n📏 初始状态:")
print(f"   位置: ({data.qpos[0]:.3f}, {data.qpos[1]:.3f}, {data.qpos[2]:.3f})")
print(f"   高度: {data.qpos[2]:.3f}m")

# 启动查看器
print("\n🖥️  启动查看器...")
viewer = mujoco.viewer.launch_passive(model, data)
viewer.cam.distance = 3.5
viewer.cam.azimuth = 135
viewer.cam.elevation = -20
viewer.cam.lookat[:] = [0, 0, 0.9]

# 稳定阶段
print("⏳ 物理稳定中...")
for i in range(300):
    mj.mj_step(model, data)
    if i % 50 == 0:
        viewer.sync()
    time.sleep(0.005)

print(f"✅ 稳定后高度: {data.qpos[2]:.3f}m")

# ============================================
# 测试 1: 站立平衡 (PD控制)
# ============================================
print("\n🧪 测试 1: PD控制站立平衡")

def pd_control(kp=100, kd=10):
    """计算PD控制力矩"""
    ctrl = np.zeros(model.nu)
    
    for i in range(model.nu):
        # 找到对应的关节
        if i < len(joints):
            joint_name = list(joints.keys())[i] if i < len(joints) else None
            if joint_name:
                q_idx = joints[joint_name]['qpos_idx']
                v_idx = joints[joint_name]['dof_idx']
                
                if q_idx < len(data.qpos) and v_idx >= 0 and v_idx < len(data.qvel):
                    q = data.qpos[q_idx]
                    q0 = home_qpos[q_idx]
                    dq = data.qvel[v_idx]
                    
                    # PD: tau = kp*(q0-q) - kd*dq
                    ctrl[i] = kp * (q0 - q) - kd * dq
    
    return np.clip(ctrl, -80, 80)  # 限幅

# 测试站立
for step in range(1000):
    ctrl = pd_control(kp=80, kd=8)
    data.ctrl[:] = ctrl
    mj.mj_step(model, data)
    viewer.sync()
    
    if step % 200 == 0:
        print(f"   Step {step:4d} | 高度: {data.qpos[2]:.3f}m | 俯仰: {np.arctan2(2*(data.qpos[3]*data.qpos[5] - data.qpos[6]*data.qpos[4]), 1-2*(data.qpos[5]**2+data.qpos[6]**2)):.3f}")

# ============================================
# 测试 2: 原地踏步 (正弦波)
# ============================================
print("\n🧪 测试 2: 原地踏步行走")

# 找到腿部关节
left_leg = [n for n in joints.keys() if 'left' in n.lower() and any(k in n.lower() for k in ['hip', 'knee', 'ankle'])]
right_leg = [n for n in joints.keys() if 'right' in n.lower() and any(k in n.lower() for k in ['hip', 'knee', 'ankle'])]

print(f"   左腿关节: {left_leg}")
print(f"   右腿关节: {right_leg}")

# 重置
mj.mj_resetDataKeyframe(model, data, 0)

step_count = 0
start_x = data.qpos[0]

try:
    while viewer.is_running() and step_count < 3000:
        t = data.time
        
        # 步态参数
        freq = 1.5  # 步频
        phase = 2 * np.pi * freq * t
        
        ctrl = np.zeros(model.nu)
        
        # 对腿部施加正弦波
        for i, name in enumerate(joints.keys()):
            if i >= model.nu:
                break
                
            if name in left_leg:
                # 左腿
                if 'hip_pitch' in name:
                    ctrl[i] = 30 * np.sin(phase)  # 髋关节前后
                elif 'knee' in name:
                    ctrl[i] = 20 * max(0, np.sin(phase - 0.5))  # 膝关节弯曲
                elif 'ankle' in name:
                    ctrl[i] = 10 * np.sin(phase - 1.0)  # 踝关节补偿
                    
            elif name in right_leg:
                # 右腿 (相位差180度)
                if 'hip_pitch' in name:
                    ctrl[i] = 30 * np.sin(phase + np.pi)
                elif 'knee' in name:
                    ctrl[i] = 20 * max(0, np.sin(phase + np.pi - 0.5))
                elif 'ankle' in name:
                    ctrl[i] = 10 * np.sin(phase + np.pi - 1.0)
            
            else:
                # 其他关节保持平衡
                q_idx = joints[name]['qpos_idx']
                v_idx = joints[name]['dof_idx']
                if q_idx < len(data.qpos) and v_idx >= 0:
                    q = data.qpos[q_idx]
                    q0 = home_qpos[q_idx]
                    dq = data.qvel[v_idx] if v_idx < len(data.qvel) else 0
                    ctrl[i] = 50 * (q0 - q) - 5 * dq
        
        # 限幅
        ctrl = np.clip(ctrl, -80, 80)
        data.ctrl[:] = ctrl
        
        mj.mj_step(model, data)
        viewer.sync()
        
        step_count += 1
        if step_count % 500 == 0:
            moved = data.qpos[0] - start_x
            print(f"   Step {step_count:4d} | 前移: {moved:+.3f}m | 高度: {data.qpos[2]:.3f}m")
        
        time.sleep(0.002)

except KeyboardInterrupt:
    print("\n   用户停止")

# ============================================
# 恢复
# ============================================
print("\n🔄 恢复站立...")

for i in range(500):
    ctrl = pd_control(kp=100, kd=10)
    data.ctrl[:] = ctrl
    mj.mj_step(model, data)
    if i % 50 == 0:
        viewer.sync()
    time.sleep(0.005)

viewer.close()
print("\n" + "=" * 70)
print("✅ H1 测试完成")
print("=" * 70)
EOF

python3 test_h1.py
