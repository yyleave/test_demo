# AutoPaper Phase 2 - 多智能体辩论与方向收敛 🎯

## 概述

Phase 2 通过**对抗性辩论机制**，从 Phase 1 的知识图谱中筛选出具备发表价值的研究选题，最终生成完整的 Research Proposal。

---

## 三大Agent角色 🤖

### 1. 激进派 (Hypothesis Agent) - 创新者

**职责**：提出3-5个新颖冒进的研究假设

**特点**：
- 追求创新性和突破性
- 不拘泥于现有方法
- 大胆提出跨领域组合创新
- 重视学术影响力

**输出示例**：
```json
{
  "id": "hyp_001",
  "title": "基于量子注意力的长序列建模",
  "description": "结合量子计算原理改进Transformer...",
  "novelty": 9,
  "potential_impact": "可能突破当前长度限制",
  "key_innovation": "量子态叠加的注意力机制"
}
```

---

### 2. 保守派 (Sanity Agent) - 审查者

**职责**：审查假设的可行性和自洽性

**审查维度**：
- ✅ 物理/数学自洽性
- ✅ 工程实现可行性
- ✅ 硬件算力是否足够
- ✅ 数据可获得性
- ✅ 时间周期合理性（1年内）

**评分标准**：0-10分，6分及以上视为通过

**输出示例**：
```json
{
  "score": 7,
  "feasibility": "可行",
  "concerns": ["需要专用量子硬件", "理论推导复杂"],
  "suggestions": ["可先在经典计算机上模拟", "分阶段实现"],
  "hardware_ok": false,
  "data_ok": true,
  "timeline_ok": true
}
```

---

### 3. 刺客 (Killer Agent) - 批判者

**职责**：用最严苛的审稿人视角攻击薄弱点

**寻找问题**：
- 🔍 致命缺陷（会导致拒稿）
- 🔍 创新性不足（incremental work）
- 🔍 实验设计漏洞
- 🔍 对比实验不充分
- 🔍 理论支撑薄弱
- 🔍 审稿人可能的质疑

**攻击等级**：
- `critical` - 致命缺陷，建议reject
- `major` - 重大问题，需major revision
- `minor` - 小问题，minor revision
- `accept` - 可接受

**输出示例**：
```json
{
  "severity": "major",
  "fatal_flaws": ["缺乏理论证明"],
  "weak_points": ["实验设计过于简单"],
  "reviewer_questions": ["为什么量子方法一定优于经典方法？"],
  "recommendation": "major_revision"
}
```

---

## 工作流程 📊

```
Phase 1 知识图谱
    ↓
┌─────────────────────────────────────┐
│  第1轮辩论                           │
│  ├─ 激进派: 提出5个假设              │
│  ├─ 保守派: 评分审查                 │
│  ├─ 刺客: 攻击薄弱点                 │
│  └─ 筛选: 保留存活假设               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  用户决策                             │
│  ├─ 选项1: 选择一个假设继续          │
│  ├─ 选项2: 重新辩论（最多3轮）       │
│  └─ 选项3: 退出                      │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  生成 Research Proposal              │
│  ├─ 研究标题与摘要                   │
│  ├─ 研究问题与假设                   │
│  ├─ 动机与文献空白                   │
│  ├─ 研究方法                         │
│  ├─ 预期贡献                         │
│  ├─ 时间规划                         │
│  └─ 风险评估                         │
└─────────────────────────────────────┘
    ↓
phase2_output.json
```

---

## 快速开始 🚀

### 1. 确保已完成 Phase 1

```bash
# 检查Phase 1输出是否存在
ls phase1_output.json
```

### 2. 运行 Phase 2

```bash
# 使用默认的phase1_output.json
python phase2.py

# 或指定Phase 1输出文件
python phase2.py /path/to/phase1_output.json
```

### 3. 交互式选择

程序会显示所有通过辩论的假设，你需要：

```
【假设 1】
标题: 基于量子注意力的长序列建模
描述: ...
创新性: 9/10
可行性评分: 7/10
攻击强度: major

【假设 2】
标题: 跨模态知识蒸馏框架
描述: ...
创新性: 8/10
可行性评分: 8/10
攻击强度: minor

请选择一个假设继续，或选择重新辩论：
输入 1-2 选择对应假设
输入 0 重新辩论
输入 q 退出

你的选择: 2
```

---

## 输出文件 📁

### phase2_output.json

完整的辩论记录和研究计划书：

```json
{
  "debate_history": [
    {
      "round": 1,
      "hypotheses": [...],
      "sanity_review": {...},
      "killer_attacks": {...},
      "surviving_hypotheses": [...]
    }
  ],
  "selected_hypothesis": {
    "id": "hyp_002",
    "title": "...",
    ...
  },
  "research_proposal": {
    "title": "研究标题",
    "abstract": "研究摘要",
    "research_question": "核心研究问题",
    "hypothesis": "研究假设",
    "motivation": {
      "why_important": "重要性",
      "gap_in_literature": "文献空白",
      "potential_impact": "潜在影响"
    },
    "methodology": {
      "approach": "研究方法",
      "datasets": ["数据集1", "数据集2"],
      "evaluation_metrics": ["指标1", "指标2"],
      "baseline_methods": ["基线1", "基线2"]
    },
    "expected_contributions": ["贡献1", "贡献2"],
    "timeline": {
      "month_1_3": "文献调研与数据准备",
      "month_4_6": "模型设计与实现",
      "month_7_9": "实验与优化",
      "month_10_12": "论文撰写"
    },
    "required_resources": {
      "computational": "4×A100 GPU",
      "data": "1TB训练数据",
      "human": "1名博士生"
    },
    "risk_assessment": [
      {
        "risk": "模型收敛困难",
        "likelihood": "中",
        "mitigation": "采用预训练模型初始化"
      }
    ],
    "target_venues": ["NeurIPS", "ICML", "ICLR"]
  },
  "timestamp": "2024-03-26T10:30:00",
  "phase": 2
}
```

---

## 高级用法 🔧

### 1. 调整辩论轮次

修改 `phase2.py` 中的 `max_rounds`：

```python
max_rounds = 5  # 默认3轮
```

### 2. 调整假设数量

```python
hypotheses = debate_system.hypothesis_agent.propose_hypotheses(num_hypotheses=10)
```

### 3. 自定义筛选标准

修改 `_filter_surviving` 方法：

```python
# 更严格的筛选：sanity >= 8 且 attack为minor
if sanity_score >= 8 and attack_severity == 'minor':
    surviving.append(hyp)
```

### 4. 批量模式（非交互）

```python
# 自动选择得分最高的假设
best_hyp = max(surviving, key=lambda h: h.get('sanity_score', 0))
proposal = debate_system.generate_research_proposal(best_hyp)
```

---

## 辩论策略 💡

### 如何提高假设通过率？

1. **Phase 1阶段**：提供更详细的背景信息
2. **激进派**：平衡创新性与可行性（novelty 7-8较合适）
3. **保守派**：确保硬件和数据约束准确
4. **多轮辩论**：第一轮被拒的方向在后续轮次可优化

### 选择假设的建议

- ✅ 优先选择 `sanity_score >= 7` 的假设
- ✅ 避免 `severity: critical` 的假设
- ✅ 考虑自己的实际资源和时间
- ✅ 选择你真正感兴趣的方向

---

## 示例输出 📝

### 成功案例

**输入**（Phase 1）：
```
"清华大学计算机系博士，研究NLP长文本处理"
```

**Phase 2 辩论过程**：

```
第1轮辩论：
- 激进派提出5个假设
- 保守派筛选后剩余3个
- 刺客攻击后存活2个

用户选择：假设2 - "基于滑动窗口的高效长文本建模"

生成Proposal：
标题: Efficient Long-Text Modeling via Sliding Window Attention
创新点: 降低计算复杂度到O(n)，支持无限长度
目标会议: ACL 2025
```

---

## 故障排除 🔧

### 问题1：所有假设都被拒绝

**原因**：假设过于激进或硬件约束太严格

**解决**：
1. 降低创新性要求（temperature降低）
2. 在Phase 1提供更准确的资源信息
3. 增加辩论轮次

### 问题2：JSON解析失败

**原因**：AI模型输出格式不规范

**解决**：重新运行该轮辩论

### 问题3：生成的Proposal质量不高

**原因**：选中的假设本身质量一般

**解决**：
1. 重新辩论，选择更好的假设
2. 手动编辑 `phase2_output.json` 中的proposal部分

---

## 后续步骤 🎯

完成 Phase 2 后：

1. **审阅 Research Proposal** - 确保所有细节合理
2. **准备进入 Phase 3** - 沙盒执行与实验
3. **迭代优化** - 根据Proposal调整研究计划

---

## 设计理念 💭

### 为什么需要三个Agent？

- **激进派**：确保创新性，避免incremental work
- **保守派**：确保可行性，避免空中楼阁
- **刺客**：模拟真实审稿过程，提前发现问题

### 为什么需要多轮辩论？

- 第一轮可能过于激进，通过率低
- 多轮迭代可以逐步收敛到最优方案
- 模拟真实科研中的"试错-优化"过程

---

## 下一步：Phase 3

Research Proposal 生成后，将进入 Phase 3：

- 任务分解（DAG）
- 代码自动生成
- 沙盒环境执行
- 结果监控与评估

**敬请期待！** 🚀

---

**祝你选出优秀的研究方向！** 🎉
