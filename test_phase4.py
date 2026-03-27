#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Phase 4 测试脚本 - 用于快速验证 Phase 4 功能
"""

import os
import json
import tempfile
from pathlib import Path


def create_mock_phase3_output():
    """创建模拟的 Phase 3 输出用于测试"""
    mock_output = {
        "phase": 3,
        "proposal": {
            "title": "MNIST手写数字识别实验",
            "abstract": "本研究实现了一个简单的神经网络对MNIST手写数字进行分类",
            "methodology": {
                "approach": "全连接神经网络",
                "dataset": "MNIST",
                "evaluation": "准确率"
            },
            "expected_contributions": [
                "实现准确率 > 90%",
                "训练时间 < 5分钟"
            ]
        },
        "execution_history": [
            {
                "iteration": 1,
                "execution_result": {
                    "status": "success",
                    "metrics": {
                        "accuracy": 0.92,
                        "loss": 0.234,
                        "training_time": 240
                    },
                    "artifacts": ["results.png", "metrics.csv"]
                },
                "evaluation": {
                    "status": "pass",
                    "score": 8.5,
                    "strengths": ["高准确率", "快速训练"]
                }
            }
        ],
        "summary": {
            "total_iterations": 1,
            "final_status": "pass",
            "experiment_dir": "/tmp/mock_experiment"
        }
    }
    
    return mock_output


def create_mock_phase1_output():
    """创建模拟的 Phase 1 输出（文献库）"""
    mock_output = {
        "phase": 1,
        "literature": [
            {
                "title": "Deep Learning",
                "authors": "Goodfellow, I., Bengio, Y., Courville, A.",
                "year": "2016",
                "venue": "MIT Press",
                "url": "https://www.deeplearningbook.org/"
            },
            {
                "title": "Attention Is All You Need",
                "authors": "Vaswani, A. et al.",
                "year": "2017",
                "venue": "NeurIPS",
                "url": "https://arxiv.org/abs/1706.03762"
            }
        ]
    }
    
    return mock_output


def test_phase4():
    """测试 Phase 4 的核心功能"""
    
    print("\n" + "="*80)
    print("🧪 Phase 4 功能测试")
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
    
    temp_dir = Path(tempfile.mkdtemp(prefix="phase4_test_"))
    test_phase3 = temp_dir / "test_phase3_output.json"
    test_phase1 = temp_dir / "test_phase1_output.json"
    
    with open(test_phase3, 'w', encoding='utf-8') as f:
        json.dump(create_mock_phase3_output(), f, ensure_ascii=False, indent=2)
    
    with open(test_phase1, 'w', encoding='utf-8') as f:
        json.dump(create_mock_phase1_output(), f, ensure_ascii=False, indent=2)
    
    print(f"✅ 测试数据已创建")
    print(f"   Phase 3: {test_phase3}")
    print(f"   Phase 1: {test_phase1}\n")
    
    # 导入 Phase 4
    print("⏳ 步骤 3/5: 加载 Phase 4 模块...")
    
    try:
        from phase4 import PaperGenerationSystem
        print("✅ Phase 4 模块加载成功\n")
    except ImportError as e:
        print(f"❌ Phase 4 模块加载失败: {e}")
        return False
    
    # 测试系统初始化
    print("⏳ 步骤 4/5: 测试论文生成系统...")
    
    try:
        system = PaperGenerationSystem(
            str(test_phase3),
            str(test_phase1)
        )
        
        print(f"✅ PaperGenerationSystem 初始化成功")
        print(f"   论文标题: {system.proposal.get('title', 'N/A')}")
        print(f"   文献数量: {len(system.literature)}")
        print(f"   实验结果: {len(system.experiment_results)} 轮\n")
        
        # 测试单个章节生成
        print("⏳ 测试 AcademicWriter（生成摘要）...")
        abstract = system.academic_writer.write_section('abstract')
        
        print(f"✅ 摘要生成成功")
        print(f"   长度: {len(abstract)} 字符")
        print(f"   预览: {abstract[:100]}...\n")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
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
    print("✅ Phase 4 基础功能测试通过！")
    print("="*80)
    print("\n💡 下一步:")
    print("1. 运行完整的 Phase 1、2 和 3")
    print("2. 使用真实数据运行 Phase 4:")
    print("   python phase4.py")
    print("\n📚 注意:")
    print("- Phase 4 需要 Phase 3 的实验结果")
    print("- 生成PDF需要安装LaTeX环境（可选）")
    print("- 即使没有LaTeX，也会生成LaTeX源码\n")
    
    return True


def main():
    """主函数"""
    try:
        success = test_phase4()
        exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 测试过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        exit(1)


if __name__ == "__main__":
    """
    Phase 4 快速测试脚本
    
    使用方式:
        python test_phase4.py
    
    这个脚本会:
    1. 检查环境配置
    2. 创建模拟的 Phase 3 和 Phase 1 输出
    3. 测试 Phase 4 的基础功能
    4. 清理测试文件
    
    如果测试通过，说明 Phase 4 已经正确安装和配置。
    """
    main()
