#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Phase 3 测试脚本 - 用于快速验证 Phase 3 功能

这个脚本会创建一个简化的测试场景，快速验证 Phase 3 的核心功能。
"""

import os
import json
import tempfile
from pathlib import Path

def create_mock_phase2_output():
    """创建一个模拟的 Phase 2 输出用于测试"""
    mock_output = {
        "phase": 2,
        "selected_hypothesis": {
            "title": "简单MNIST分类器测试",
            "description": "使用简单的神经网络对MNIST数据集进行分类"
        },
        "research_proposal": {
            "title": "MNIST手写数字识别实验",
            "abstract": "本研究旨在实现一个简单的神经网络，对MNIST手写数字进行分类。这是一个基础的深度学习实验。",
            "methodology": {
                "approach": "使用简单的全连接神经网络",
                "dataset": "MNIST（手写数字数据集）",
                "evaluation": "准确率（Accuracy）"
            },
            "timeline": {
                "total_duration": "1小时",
                "phases": [
                    {"phase": "数据准备", "duration": "10分钟"},
                    {"phase": "模型训练", "duration": "30分钟"},
                    {"phase": "结果评估", "duration": "20分钟"}
                ]
            },
            "expected_contributions": [
                "实现准确率 > 90%",
                "训练时间 < 5分钟",
                "生成loss曲线可视化"
            ],
            "risk_assessment": [
                {"risk": "过拟合", "mitigation": "使用Dropout"}
            ]
        },
        "timestamp": "2024-01-15T10:00:00"
    }
    
    return mock_output


def test_phase3():
    """测试 Phase 3 的核心功能"""
    
    print("\n" + "="*80)
    print("🧪 Phase 3 功能测试")
    print("="*80 + "\n")
    
    # 检查环境
    print("⏳ 步骤 1/5: 检查环境...")
    
    if not os.getenv('ARK_API_KEY'):
        print("❌ 错误：未设置 ARK_API_KEY 环境变量")
        print("请运行: export ARK_API_KEY='你的API密钥'")
        return False
    
    print("✅ API密钥已设置\n")
    
    # 创建临时测试文件
    print("⏳ 步骤 2/5: 创建测试数据...")
    
    temp_dir = Path(tempfile.mkdtemp(prefix="phase3_test_"))
    test_input = temp_dir / "test_phase2_output.json"
    
    mock_data = create_mock_phase2_output()
    with open(test_input, 'w', encoding='utf-8') as f:
        json.dump(mock_data, f, ensure_ascii=False, indent=2)
    
    print(f"✅ 测试数据已创建: {test_input}\n")
    
    # 导入 Phase 3
    print("⏳ 步骤 3/5: 加载 Phase 3 模块...")
    
    try:
        from phase3 import ExecutionSystem
        print("✅ Phase 3 模块加载成功\n")
    except ImportError as e:
        print(f"❌ Phase 3 模块加载失败: {e}")
        return False
    
    # 测试任务分解
    print("⏳ 步骤 4/5: 测试任务分解器...")
    
    try:
        system = ExecutionSystem(
            str(test_input),
            workspace_dir=str(temp_dir / "workspace")
        )
        
        print(f"✅ ExecutionSystem 初始化成功")
        print(f"   实验目录: {system.experiment_dir}\n")
        
        # 测试任务分解
        print("⏳ 测试 TaskDecomposer...")
        task_dag = system.task_decomposer.decompose()
        
        print(f"✅ 任务分解成功")
        print(f"   任务数量: {len(task_dag.get('tasks', []))}")
        print(f"   DAG节点: {len(task_dag.get('dag', {}).get('nodes', []))}\n")
        
    except Exception as e:
        print(f"❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # 清理
    print("⏳ 步骤 5/5: 清理测试文件...")
    
    try:
        import shutil
        shutil.rmtree(temp_dir)
        print("✅ 测试文件已清理\n")
    except Exception as e:
        print(f"⚠️  清理失败: {e}\n")
    
    # 总结
    print("="*80)
    print("✅ Phase 3 基础功能测试通过！")
    print("="*80)
    print("\n💡 下一步:")
    print("1. 运行完整的 Phase 1 和 Phase 2")
    print("2. 使用真实数据运行 Phase 3:")
    print("   python phase3.py\n")
    
    return True


def main():
    """主函数"""
    try:
        success = test_phase3()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    """
    Phase 3 快速测试脚本
    
    使用方式:
        python test_phase3.py
    
    这个脚本会:
    1. 检查环境配置
    2. 创建模拟的 Phase 2 输出
    3. 测试 Phase 3 的基础功能
    4. 清理测试文件
    
    如果测试通过，说明 Phase 3 已经正确安装和配置。
    """
    main()
