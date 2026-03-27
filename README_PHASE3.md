# Phase 3: 沙盒执行与评估闭环

> 在严格隔离的沙盒环境中执行实验，通过客观评估闭环确保质量。

---

## 🎯 核心功能

Phase 3 将 Phase 2 生成的 Research Proposal 转化为可执行的实验代码，并通过多轮迭代优化，确保实验质量。

### 核心机制

1. **上下文硬重置**：清空前两阶段的冗杂讨论，仅保留 Proposal 作为唯一输入
2. **DAG 任务分解**：将研究目标拆解为有向无环图形式的实验步骤
3. **沙盒执行**：在隔离环境中运行实验，防止系统污染
4. **智能监控**：实时检测数值异常（NaN/Inf）和运行错误
5. **客观评估**：基于真实探针数据评估实验结果
6. **FARS 机制**：所有运行日志强制 Git 提交，过程可回溯、可审计

---

## 🤖 四大 Agent

### 1. Task Decomposer（任务分解器）

**职责**：将 Research Proposal 拆解为 DAG 形式的实验步骤

**输入**：Research Proposal
**输出**：
```json
{
  "tasks": [
    {
      "id": "task_001",
      "name": "数据预处理",
      "type": "data_preparation",
      "dependencies": [],
      "estimated_time": "1 hour",
      "code_template": "..."
    }
  ],
  "dag": {
    "nodes": ["task_001", "task_002"],
    "edges": [["task_001", "task_002"]]
  }
}
```

### 2. Code Generator（代码生成器）

**职责**：根据任务 DAG 生成完整的实验代码

**输入**：Task DAG + 上下文（之前迭代的错误和建议）
**输出**：
- `main.py`：主执行文件
- `model.py`：模型定义
- `data.py`：数据处理
- `utils.py`：工具函数
- `requirements.txt`：依赖包

### 3. Sentinel（哨兵）

**职责**：监控执行过程，检测异常并触发熔断

**监控指标**：
- ✅ 数值异常：NaN、Inf
- ✅ Loss 爆炸：Loss > 1e6
- ✅ 执行错误：Return code ≠ 0
- ✅ 超时：执行时间 > 5分钟
- ✅ 运行时警告：stderr 中的 warning

**输出**：
```json
{
  "status": "normal/error",
  "anomalies": [
    {
      "type": "nan_detected",
      "metric": "loss",
      "severity": "critical"
    }
  ],
  "warnings": []
}
```

### 4. Evaluator（评估器）

**职责**：读取真实探针数据，客观评估实验结果

**评估维度**：
1. **目标达成度**：是否实现 Proposal 中的预期目标
2. **指标合理性**：Loss、Accuracy 等是否在合理范围
3. **输出完整性**：是否生成了必要的可视化和数据文件
4. **代码质量**：是否有异常和警告

**评分标准**：
- 8-10 分：优秀，达到预期目标 ➜ `status: pass`
- 6-8 分：良好，基本达标 ➜ `status: partial`
- 4-6 分：及格，需要改进 ➜ `status: fail`
- 0-4 分：不及格，需要重做 ➜ `status: fail`

---

## 🚀 快速开始

### 前置条件

1. 已完成 Phase 2，生成 `phase2_output.json`
2. 安装 Python 3.7+

### 运行 Phase 3

```bash
# 1. 使用默认的 Phase 2 输出
python phase3.py

# 2. 指定 Phase 2 输出文件
python phase3.py /path/to/phase2_output.json
```

### 完整流程演示

```bash
# 步骤1: 确保环境变量设置正确
export ARK_API_KEY='你的豆包API密钥'

# 步骤2: 运行 Phase 3
python phase3.py

# 输出示例：
# ================================================================================
# 🚀 Phase 3: 沙盒执行与评估闭环
# ================================================================================
# 
# 📂 实验目录: experiments/attention_mechanism_study_20240115_143022
# 📋 研究标题: Attention Mechanism Comparison Study
# 
# ⏳ 步骤1: 任务分解（DAG）...
# ✅ 任务分解完成，共 5 个任务
# 
# ================================================================================
# 🔄 迭代 1/5
# ================================================================================
# 
# ⏳ 步骤2: 代码生成...
# ✅ 代码生成完成，共 4 个文件
# 
# ⏳ 步骤3: 沙盒执行...
#    执行文件: main.py
#    ✅ 执行成功
# 
# ⏳ 步骤4: 哨兵监控...
#    ✅ 未发现异常
# 
# ⏳ 步骤5: 评估器校验...
#    状态: pass
#    评分: 8.5/10
#    优点: 3个
# 
# ✅ 实验通过评估！
# 
# ================================================================================
# ✅ Phase 3 完成！
# ================================================================================
# 
# 📊 最终状态: pass
# 🔁 总迭代次数: 1
# 📂 实验目录: experiments/attention_mechanism_study_20240115_143022
```

---

## 📁 输出文件

### 1. 全局输出

**`phase3_output.json`**：完整的执行记录

```json
{
  "proposal": { /* Phase 2 的 Research Proposal */ },
  "task_dag": { /* 任务分解结果 */ },
  "execution_history": [
    {
      "iteration": 1,
      "execution_result": { /* 执行结果 */ },
      "sentinel_report": { /* 哨兵报告 */ },
      "evaluation": { /* 评估结果 */ },
      "timestamp": "2024-01-15T14:30:45"
    }
  ],
  "summary": {
    "total_iterations": 1,
    "final_status": "pass",
    "experiment_dir": "experiments/..."
  }
}
```

### 2. 实验目录

**`experiments/{exp_name}_{timestamp}/`**

```
experiments/attention_mechanism_study_20240115_143022/
├── .git/                          # Git 仓库（FARS 机制）
├── task_dag.json                   # 任务分解结果
├── main.py                         # 主执行文件
├── model.py                        # 模型定义
├── data.py                         # 数据处理
├── utils.py                        # 工具函数
├── requirements.txt                # 依赖包
├── execution_log_iter1.json        # 第1轮执行日志
├── evaluation_iter1.json           # 第1轮评估结果
├── final_report.json               # 最终报告
├── results.png                     # 可视化结果（由实验生成）
└── metrics.csv                     # 指标数据（由实验生成）
```

---

## 🔄 迭代优化机制

Phase 3 支持最多 5 轮迭代优化：

### 迭代流程

```
第 N 轮:
  1. Code Generator 根据上一轮的错误和建议生成代码
  2. 沙盒执行新代码
  3. Sentinel 检测异常
  4. Evaluator 评估结果
  5. 如果 status = "pass" ➜ 结束
     如果 status = "fail" ➜ 进入第 N+1 轮
```

### 示例：两轮迭代

```
迭代 1:
  执行结果: Loss = NaN
  哨兵报告: 发现 NaN 异常
  评估结果: status = fail, 建议降低学习率

迭代 2:
  代码调整: learning_rate = 0.001 → 0.0001
  执行结果: Loss = 0.342
  哨兵报告: 未发现异常
  评估结果: status = pass, score = 8.5
```

---

## 🛡️ FARS 机制

**FARS (Force All Runs Submission)** 确保所有实验过程可追溯：

### 特性

1. **自动初始化 Git 仓库**：在实验目录下自动 `git init`
2. **强制提交**：每个关键步骤都会自动 `git commit`
3. **完整历史**：可通过 `git log` 查看所有试错过程

### 查看历史

```bash
cd experiments/your_experiment/
git log --oneline

# 输出示例：
# a3f2c1d Phase3: Final report
# 9e8b7c6 Iteration 2: Evaluation
# 5d4c3a2 Iteration 2: Execution logs
# 1b0a9f8 Iteration 2: Code generation
# 7e6d5c4 Iteration 1: Evaluation
# 3c2b1a0 Iteration 1: Execution logs
# f9e8d7c Iteration 1: Code generation
# c6b5a4f Phase3: Task decomposition
```

---

## 🧪 高级用法

### 1. 自定义工作目录

```python
from phase3 import ExecutionSystem

system = ExecutionSystem(
    phase2_output_path="phase2_output.json",
    workspace_dir="/custom/workspace"
)

result = system.run_phase3(max_iterations=3)
```

### 2. 调整最大迭代次数

```bash
# 修改 phase3.py 中的 max_iterations 参数
result = execution_system.run_phase3(max_iterations=10)
```

### 3. 查看中间结果

```python
# 读取某一轮的执行日志
import json

with open("experiments/your_exp/execution_log_iter1.json") as f:
    log = json.load(f)

print(log['stdout'])      # 标准输出
print(log['metrics'])     # 指标
print(log['artifacts'])   # 生成的文件
```

---

## 🐛 故障排除

### 问题 1：代码执行超时

**现象**：
```
⏱️  执行超时
```

**解决方案**：
1. 检查代码中是否有无限循环
2. 减少数据集大小或训练轮次
3. 修改超时时间（默认 5 分钟）

### 问题 2：NaN/Inf 异常

**现象**：
```
⚠️  发现 1 个异常
   - nan_detected: loss
```

**解决方案**：
- 评估器会自动建议降低学习率或调整初始化
- 系统会在下一轮迭代中自动修正

### 问题 3：缺少依赖包

**现象**：
```
ModuleNotFoundError: No module named 'xxx'
```

**解决方案**：
```bash
# 安装生成的 requirements.txt
cd experiments/your_experiment/
pip install -r requirements.txt
```

---

## 📊 监控指标说明

### 自动解析的指标

Phase 3 会自动从输出中解析以下格式的指标：

```python
# 在你的代码中输出（会被自动捕获）：
print("loss: 0.342")
print("accuracy: 0.856")
print("epoch: 10")
```

### 探针数据

Sentinel 和 Evaluator 会监控：

1. **Loss 曲线**：检测收敛性和稳定性
2. **张量分布**：检测 NaN/Inf
3. **资源使用**：检测内存泄漏（未来支持）
4. **收敛状态**：判断是否达到预期

---

## 💡 最佳实践

### 1. 设计可验证的 Proposal

在 Phase 2 中设计明确的评估指标：

```json
{
  "expected_contributions": [
    "实现准确率 > 85%",
    "训练时间 < 10分钟",
    "生成 loss 曲线可视化"
  ]
}
```

### 2. 使用简单数据集

Phase 3 建议使用小规模数据集进行快速验证：
- MNIST（手写数字）
- CIFAR-10（小图像）
- 自定义小数据集

### 3. 充分利用 Git 历史

```bash
# 查看所有提交
git log --graph --oneline --all

# 查看某次提交的变更
git show <commit-hash>

# 回退到某个版本
git checkout <commit-hash>
```

---

## 🔗 相关文档

- [Phase 2: 多智能体辩论](README_PHASE2.md)
- [Phase 4: 论文编撰](README_PHASE4.md)（开发中）
- [项目总览](PROJECT_README.md)

---

## ❓ FAQ

### Q1: Phase 3 需要多长时间？

**A**: 取决于实验复杂度，通常：
- 简单实验（MNIST 分类）：5-10 分钟
- 中等实验（小型 CNN）：15-30 分钟
- 复杂实验（大模型微调）：可能超过 1 小时

### Q2: 迭代次数用完了怎么办？

**A**: 系统会保存最后一轮的结果和建议，你可以：
1. 手动查看 `evaluation_iterN.json` 中的建议
2. 修改代码后手动运行
3. 增加 `max_iterations` 参数重新运行

### Q3: 如何自定义评估标准？

**A**: 修改 `Evaluator` 类的 `evaluate` 方法，添加自定义的评分逻辑。

### Q4: 支持 GPU 执行吗？

**A**: 当前版本在本地环境执行，如果系统有 GPU 且安装了相应的深度学习框架（如 PyTorch + CUDA），生成的代码会自动使用 GPU。

### Q5: 可以暂停和恢复吗？

**A**: 当前版本不支持暂停/恢复，但通过 FARS 机制，你可以：
1. 查看 Git 历史了解进度
2. 手动从某个检查点继续
3. 重新运行 Phase 3（会创建新的实验目录）

---

**🎉 恭喜！你已经掌握了 Phase 3 的核心功能！**

接下来：运行 `python phase3.py` 开始你的第一个自动化实验！
