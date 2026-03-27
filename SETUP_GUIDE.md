# AutoPaper 完整安装与使用指南

## 🎯 快速开始（5分钟上手）

### 1. 安装依赖

```bash
cd /Users/leave/Desktop/fc/AutoPaper

# 安装Python依赖
pip install -r requirements.txt
```

### 2. 配置API密钥

```bash
# 方式1：导出环境变量（推荐）
export ARK_API_KEY="你的豆包API密钥"

# 方式2：创建.env文件
cp .env.example .env
# 然后编辑.env文件，填入真实的API密钥
```

**获取API密钥**: https://console.volcengine.com/ark/region:ark+cn-beijing/apikey

### 3. 运行完整流程

```bash
# Step 1: 生成知识图谱
python phase1.py "我是MIT计算机系博士生，研究深度学习和NLP"

# 查看可视化
open phase1_kg_visualization.html

# Step 2: 多智能体辩论
python phase2.py

# Step 3: 沙盒执行与评估
python phase3.py

# 查看实验结果
cat phase3_output.json
```

---

## 📦 项目结构

```
AutoPaper/
├── 📘 核心程序
│   ├── phase1.py                    # Phase 1: 知识图谱生成
│   ├── phase2.py                    # Phase 2: 多智能体辩论
│   ├── phase3.py                    # Phase 3: 沙盒执行与评估
│   ├── visualize_kg.py              # 可视化工具
│   └── doubao_use.py                # API使用示例
│
├── 📚 文档
│   ├── PROJECT_README.md            # 项目总览
│   ├── README_PHASE1.md             # Phase 1文档
│   ├── README_PHASE2.md             # Phase 2文档
│   ├── README_PHASE3.md             # Phase 3文档
│   ├── WORKFLOW.md                  # 详细工作流程
│   └── SETUP_GUIDE.md               # 本文件
│
├── ⚙️ 配置
│   ├── requirements.txt             # Python依赖
│   ├── .env.example                 # 环境变量模板
│   └── .gitignore                   # Git忽略规则
│
└── 📁 输出文件（运行后生成）
    ├── phase1_output.json
    ├── phase1_kg_visualization.html
    ├── phase1_kg_visualization.png
    ├── phase1_kg_tree.json
    ├── phase2_output.json
    ├── phase3_output.json
    └── experiments/                 # 实验代码与结果目录
```

---

## 🔧 详细安装步骤

### 环境要求

- Python 3.8+
- 网络连接（调用豆包API）
- 浏览器（查看可视化）

### 依赖包说明

```
openai>=1.0.0              # 豆包API客户端
python-dotenv>=1.0.0       # 环境变量管理
networkx>=3.0              # 图论库（可视化）
pyvis>=0.3.0               # 交互式网络图
matplotlib>=3.5.0          # 静态图表
```

### 完整安装命令

```bash
# 1. 克隆或下载项目
cd /Users/leave/Desktop/fc/AutoPaper

# 2. 安装依赖
pip install openai python-dotenv networkx pyvis matplotlib

# 或使用requirements.txt
pip install -r requirements.txt

# 3. 验证安装
python -c "import openai, networkx, pyvis, matplotlib; print('✅ 所有依赖安装成功')"
```

---

## 🎓 使用教程

### Phase 1: 知识图谱生成

#### 基础用法

```bash
# 一句话生成知识图谱
python phase1.py "你的学术背景描述"
```

#### 示例

```bash
# 示例1：博士生
python phase1.py "我是清华大学计算机系博士生，师从张三教授研究深度学习，特别关注NLP中的长文本问题和注意力机制优化"

# 示例2：研究员
python phase1.py "MIT AI Lab研究员，Yann LeCun的学生，研究计算机视觉和生成模型，有1TB ImageNet数据集"

# 示例3：工业界
python phase1.py "字节跳动AI Lab工程师，负责推荐系统，研究多模态融合和知识图谱，有8卡A100集群"
```

#### 输出查看

```bash
# 1. 查看JSON数据
cat phase1_output.json | jq '.knowledge_graph.core_concepts'

# 2. 在浏览器中查看交互式图谱
open phase1_kg_visualization.html

# 3. 查看静态图片
open phase1_kg_visualization.png

# 4. 或使用可视化工具
python visualize_kg.py
```

---

### Phase 2: 多智能体辩论

#### 基础用法

```bash
# 使用Phase 1的默认输出
python phase2.py

# 或指定Phase 1输出文件
python phase2.py /path/to/phase1_output.json
```

#### 交互流程

```
1. 程序自动运行辩论（激进派→保守派→刺客）
2. 显示通过辩论的假设列表
3. 你选择一个假设（输入数字）
4. 或选择重新辩论（输入0）
5. 程序生成Research Proposal
6. 保存到phase2_output.json
```

#### 输出查看

```bash
# 查看Research Proposal
cat phase2_output.json | jq '.research_proposal'

# 查看辩论历史
cat phase2_output.json | jq '.debate_history'

# 查看选中的假设
cat phase2_output.json | jq '.selected_hypothesis'
```

---

### Phase 3: 沙盒执行与评估

#### 基础用法

```bash
# 使用Phase 2的默认输出
python phase3.py

# 或指定Phase 2输出文件
python phase3.py /path/to/phase2_output.json
```

#### 执行流程

```
1. 任务分解：将Research Proposal分解为DAG任务图
2. 代码生成：自动生成实验代码（main.py, model.py等）
3. 沙盒执行：在隔离环境中运行实验
4. 哨兵监控：检测NaN/Inf等异常
5. 评估器：评估结果质量（评分0-10）
6. 迭代优化：如果失败，自动修正并重试（最多5轮）
```

#### 输出查看

```bash
# 查看完整执行记录
cat phase3_output.json | jq '.summary'

# 查看实验代码
ls experiments/*/

# 查看Git提交历史（FARS机制）
cd experiments/your_experiment/
git log --oneline

# 查看某轮评估结果
cat experiments/your_experiment/evaluation_iter1.json
```

---

## 🔍 故障排除

### 常见问题

#### 1. API密钥错误

```
❌ 错误：未设置 ARK_API_KEY 环境变量
```

**解决**：
```bash
export ARK_API_KEY="你的密钥"
```

#### 2. 依赖包缺失

```
ModuleNotFoundError: No module named 'openai'
```

**解决**：
```bash
pip install openai
```

#### 3. JSON解析失败

```
⚠️ JSON解析失败
```

**解决**：重新运行，AI模型偶尔会返回不规范格式

#### 4. 可视化生成失败

```
❌ 需要安装 networkx 和 matplotlib
```

**解决**：
```bash
pip install networkx matplotlib pyvis
```

#### 5. Phase 2找不到Phase 1输出

```
❌ 错误：找不到Phase 1输出文件
```

**解决**:
```bash
# 先运行Phase 1
python phase1.py "你的背景"

# 再运行Phase 2
python phase2.py
```

#### 6. Phase 3执行超时

```
⏱️ 执行超时
```

**解决**:
- 检查生成的代码中是否有无限循环
- 减少训练轮次或数据集大小
- 修改timeout参数（默认5分钟）

#### 7. Phase 3代码执行失败

```
❌ 执行失败 (返回码: 1)
```

**解决**:
- 查看 `execution_log_iter1.json` 中的错误信息
- 系统会自动重试并修正（最多5轮）
- 如果仍失败，可手动修改 `experiments/*/main.py`

---

## 💡 最佳实践

### Phase 1 输入建议

✅ **好的输入**：
```
"我是浙江大学计算机系博士生，师从李明教授（研究方向：深度学习理论），
我的研究兴趣是长文本处理和注意力机制优化，特别关注如何降低Transformer的
计算复杂度。我有4张RTX 3090 GPU和500GB的预训练语料。"
```

❌ **不好的输入**：
```
"博士生，研究AI"  # 太简略
```

### 描述要点

包含以下信息会获得更好的结果：

1. **教育背景**：学校、专业、学位
2. **导师信息**：导师姓名和研究方向
3. **研究兴趣**：具体的研究问题
4. **硬件资源**：GPU型号、算力
5. **数据资源**：可用的数据集
6. **特殊优势**：独特的资源或背景

---

### Phase 2 选择建议

选择假设时考虑：

1. **可行性评分** ≥ 7分
2. **攻击强度** 不是critical
3. **个人兴趣** - 你真正感兴趣的方向
4. **资源匹配** - 硬件和数据是否满足
5. **时间周期** - 能否在1年内完成

---

## 📊 输出文件说明

### phase1_output.json

```json
{
  "user_profile": {           // 用户档案
    "education": [...],
    "specialties": [...],
    "advisors": [...],
    "research_interests": [...],
    "keywords": [...]
  },
  "literature": [...],        // 推荐文献列表
  "knowledge_graph": {        // 知识图谱
    "nodes": [...],           // 节点（人物、概念等）
    "edges": [...],           // 边（关系）
    "core_concepts": [...],   // 核心概念
    "research_landscape": "..." // 研究全景
  }
}
```

### phase2_output.json

```json
{
  "debate_history": [...],    // 辩论记录
  "selected_hypothesis": {...}, // 选中的假设
  "research_proposal": {      // 研究计划书
    "title": "...",
    "abstract": "...",
    "methodology": {...},
    "timeline": {...},
    "risk_assessment": [...]
  }
}
```

### phase3_output.json

```json
{
  "proposal": {...},          // Research Proposal
  "task_dag": {...},          // 任务分解结果
  "execution_history": [      // 执行历史
    {
      "iteration": 1,
      "execution_result": {...},
      "sentinel_report": {...},
      "evaluation": {...}
    }
  ],
  "summary": {
    "total_iterations": 1,
    "final_status": "pass/fail",
    "experiment_dir": "experiments/..."
  }
}
```

---

## 🚀 性能优化

### 加速技巧

1. **Phase 1优化**：
   ```python
   # 减少文献数量（8-12篇 → 5-8篇）
   search_query = "请推荐5-8篇..."
   ```

2. **Phase 2优化**：
   ```python
   # 减少假设数量（5个 → 3个）
   hypotheses = self.hypothesis_agent.propose_hypotheses(num_hypotheses=3)
   ```

3. **降低温度**（牺牲创新性换取稳定性）：
   ```python
   temperature=0.5  # 默认0.7
   ```

---

## 📈 进阶使用

### Python脚本集成

```python
from phase1 import quick_mode
from phase2 import DebateSystem

# 运行Phase 1
phase1_result = quick_mode("我是MIT博士生...")

# 运行Phase 2
debate = DebateSystem("phase1_output.json")
round_result = debate.run_debate_round(1)
surviving = round_result['surviving_hypotheses']

# 自动选择最佳假设
best = max(surviving, key=lambda h: h.get('sanity_score', 0))
proposal = debate.generate_research_proposal(best)
```

### 批量处理

```python
descriptions = [
    "清华大学...",
    "MIT...",
    "Stanford..."
]

for desc in descriptions:
    quick_mode(desc, visualize=False)
```

---

## 🎯 下一步计划

- [x] Phase 1: 知识图谱生成系统 ✅
- [x] Phase 2: 多智能体辩论系统 ✅
- [x] Phase 3: 沙盒执行与评估系统 ✅
- [ ] Phase 4: 论文自动编撰
- [ ] 支持更多AI模型（GPT-4, Claude等）
- [ ] Web界面
- [ ] 数据库持久化

---

## 📞 获取帮助

遇到问题？

1. 查看 `README_PHASE1.md`、`README_PHASE2.md` 和 `README_PHASE3.md`
2. 查看 `WORKFLOW.md` 了解详细流程
3. 查看 `doubao_use.py` 了解API用法
4. 查看 `PROJECT_README.md` 了解项目整体架构

---

**祝你使用愉快！** 🎉
