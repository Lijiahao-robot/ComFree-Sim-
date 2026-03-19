cat > test_humanoid.py << 'EOF'
#!/usr/bin/env python3
"""
人形机器人仿真模板测试 (修复版)
适配 MuJoCo，兼容 ComFree-Sim 接口
"""

import os
import sys
import numpy as np

# 检查mujoco
try:
    import mujoco as mj
    print(f"✅ MuJoCo 版本: {mj.__version__}")
except ImportError:
    print("❌ 未安装 MuJoCo，请运行: pip install mujoco")
    sys.exit(1)

class HumanoidSimulator:
    def __init__(self, model_path: str, use_gpu=False):
        """
        初始化人形机器人仿真器
        """
        # 检查模型文件
        if not os.path.exists(model_path):
            # 尝试使用默认模型
            default_paths = [
                os.path.expanduser("~/mujoco_menagerie/unitree_g1/scene.xml"),
                os.path.expanduser("~/mujoco_menagerie/unitree_h1/scene.xml"),
                "/usr/share/mujoco/model/humanoid.xml",
            ]
            for p in default_paths:
                if os.path.exists(p):
                    model_path = p
                    print(f"🔄 使用默认模型: {p}")
                    break
            else:
                print(f"❌ 找不到模型: {model_path}")
                print("请提供有效的XML模型路径")
                sys.exit(1)
        
        # 加载模型
        try:
            self.model = mj.MjModel.from_xml_path(model_path)
            self.data = mj.MjData(self.model)
            print(f"✅ 模型加载成功: {os.path.basename(model_path)}")
        except Exception as e:
            print(f"❌ 加载模型失败: {e}")
            sys.exit(1)
        
        # 配置
        self.model.opt.timestep = 0.002
        self.use_gpu = use_gpu
        
        # 自动检测关节结构
        self.joint_info = self._detect_joints()
        print(f"📊 检测到 {len(self.joint_info)} 个关节")
        
        # 查找关键关节
        self._find_key_joints()

    def _detect_joints(self):
        """自动检测关节结构"""
        joints = {}
        for i in range(self.model.njnt):
            name = mj.mj_id2name(self.model, mj.mjtObj.mjOBJ_JOINT, i)
            if name:
                qpos_adr = self.model.jnt_qposadr[i]
                dof_adr = self.model.jnt_dofadr[i] if self.model.jnt_dofadr[i] >= 0 else -1
                joints[name] = {
                    'id': i,
                    'qpos_adr': qpos_adr,
                    'dof_adr': dof_adr,
                    'type': self.model.jnt_type[i]
                }
        return joints
    
    def _find_key_joints(self):
        """查找关键关节组"""
        # 腿部关节关键词
        leg_keywords = ['hip', 'knee', 'ankle', 'leg', 'thigh', 'calf', 'shin']
        arm_keywords = ['shoulder', 'elbow', 'wrist', 'arm', 'hand']
        
        self.leg_joints = []
        self.arm_joints = []
        self.other_joints = []
        
        for name, info in self.joint_info.items():
            name_lower = name.lower()
            if any(k in name_lower for k in leg_keywords):
                self.leg_joints.append(name)
            elif any(k in name_lower for k in arm_keywords):
                self.arm_joints.append(name)
            else:
                self.other_joints.append(name)
        
        print(f"  🦵 腿部关节: {len(self.leg_joints)} 个")
        print(f"    {self.leg_joints[:6]}...")
        print(f"  💪 手臂关节: {len(self.arm_joints)} 个")
        print(f"    {self.arm_joints[:4]}...")

    def reset(self, qpos=None, qvel=None):
        """重置仿真状态"""
        mj.mj_resetData(self.model, self.data)
        
        if qpos is not None:
            self.data.qpos[:] = qpos
        else:
            # 使用keyframe 0或默认站立
            if self.model.nkey > 0:
                mj.mj_resetDataKeyframe(self.model, self.data, 0)
                print("🔄 重置到 keyframe 0")
        
        if qvel is not None:
            self.data.qvel[:] = qvel
            
        mj.mj_forward(self.model, self.data)

    def step(self, control_input=None):
        """执行单步仿真"""
        if control_input is not None:
            # 确保维度匹配
            ctrl_dim = min(len(control_input), self.model.nu)
            self.data.ctrl[:ctrl_dim] = control_input[:ctrl_dim]
        
        mj.mj_step(self.model, self.data)

    def get_state(self):
        """获取当前状态"""
        return {
            "qpos": self.data.qpos.copy(),
            "qvel": self.data.qvel.copy(),
            "time": self.data.time,
            "height": self.data.qpos[2] if len(self.data.qpos) > 2 else 0
        }

    def pd_control(self, target_qpos, kp=100.0, kd=10.0):
        """PD控制器计算力矩"""
        ctrl = np.zeros(self.model.nu)
        
        # 对每个执行器应用PD控制
        for i in range(self.model.nu):
            # 获取对应的关节信息
            if i < len(self.data.qpos) - 7:  # 跳过根节点
                q_idx = 7 + i  # 假设根节点7个自由度
                v_idx = 6 + i
                
                if q_idx < len(self.data.qpos) and v_idx < len(self.data.qvel):
                    q = self.data.qpos[q_idx]
                    dq = self.data.qvel[v_idx]
                    target = target_qpos[i] if i < len(target_qpos) else 0
                    ctrl[i] = kp * (target - q) - kd * dq
        
        return ctrl

# ==============================================
# 主程序
# ==============================================
if __name__ == "__main__":
    # 测试模型路径（优先使用G1）
    test_model = os.path.expanduser("~/mujoco_menagerie/unitree_g1/scene.xml")
    
    print("=" * 60)
    print("人形机器人仿真模板测试")
    print("=" * 60)
    
    # 初始化
    sim = HumanoidSimulator(model_path=test_model, use_gpu=False)
    
    # 重置
    sim.reset()
    initial_height = sim.data.qpos[2]
    print(f"\n📏 初始高度: {initial_height:.3f}m")
    
    # 测试1: 无控制（自由落体/平衡测试）
    print("\n🧪 测试1: 无控制仿真（观察稳定性）")
    for step in range(500):
        sim.step()
        if step % 100 == 0:
            state = sim.get_state()
            print(f"  Step {step:3d} | 高度: {state['height']:.3f}m | 时间: {state['time']:.2f}s")
    
    # 重置
    sim.reset()
    
    # 测试2: PD控制站立
    print("\n🧪 测试2: PD控制站立")
    target_pos = np.zeros(sim.model.nu)
    
    for step in range(1000):
        # 计算PD控制力矩
        ctrl = sim.pd_control(target_pos, kp=80.0, kd=8.0)
        sim.step(ctrl)
        
        if step % 200 == 0:
            state = sim.get_state()
            print(f"  Step {step:4d} | 高度: {state['height']:.3f}m")
    
    # 测试3: 简单正弦波行走
    print("\n🧪 测试3: 正弦波行走测试")
    sim.reset()
    
    for step in range(2000):
        t = sim.data.time
        phase = 2 * np.pi * 1.0 * t  # 1Hz
        
        # 生成正弦波控制（交替腿部）
        ctrl = np.zeros(sim.model.nu)
        
        # 假设腿部执行器在前几个
        leg_ctrl_count = min(6, sim.model.nu)
        for i in range(leg_ctrl_count):
            if i % 2 == 0:  # 左腿
                ctrl[i] = 20.0 * np.sin(phase)
            else:  # 右腿
                ctrl[i] = 20.0 * np.sin(phase + np.pi)
        
        sim.step(ctrl)
        
        if step % 400 == 0:
            state = sim.get_state()
            print(f"  Step {step:4d} | 高度: {state['height']:.3f}m | 时间: {state['time']:.2f}s")
    
    print("\n" + "=" * 60)
    print("✅ 所有测试完成")
    print("=" * 60)
EOF

python3 test_humanoid.py
