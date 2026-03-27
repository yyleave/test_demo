# AutoPaper - AI驱动的学术论文自动生成系统

## 项目概述

AutoPaper 是一个基于多智能体协作的学术论文自动生成系统，通过4个阶段实现从个人背景到发表级论文的全流程自动化。

---

## 🎯 系统架构

```
Phase 1: 数据底座与图谱初始化
    ↓
Phase 2: 多智能体辩论与方向收敛
    ↓
Phase 3: 沙盒执行与评估闭环
    ↓
Phase 4: 防幻觉论文编撰
```

---

## 📁 项目结构

```
AutoPaper/
├── 📄 PROJECT_README.md          # 项目总览（本文件）
├── 📄 WORKFLOW.md                 # 详细工作流程说明
│
├── 🔵 Phase 1: 数据底座与图谱初始化
│   ├── phase1.py                  # 主程序：一句话生成知识图谱
│   ├── visualize_kg.py            # 知识图谱可视化工具
│   ├── README_PHASE1.md           # Phase 1 使用文档
│   └── 输出文件/
│       ├── phase1_output.json     # 完整数据（档案、文献、图谱）
│       ├── phase1_kg_visualization.html  # 交互式可视化
│       ├── phase1_kg_visualization.png   # 静态图片
│       └── phase1_kg_tree.json    # 树形数据
│
├── 🔵 Phase 2: 多智能体辩论
│   ├── phase2.py                  # 主程序：辩论与方向收敛
│   ├── README_PHASE2.md           # Phase 2 使用文档
│   └── 输出文件/
│       └── phase2_output.json     # 研究计划书与辩论记录
│
├── 🔵 Phase 3: 沙盒执行与评估闭环
│   ├── phase3.py                  # 主程序：实验执行与评估
│   ├── README_PHASE3.md           # Phase 3 使用文档
│   └── 输出文件/
│       ├── phase3_output.json     # 完整执行记录
│       └── experiments/           # 实验代码与结果目录
│
├── 🔵 Phase 4: 防幻觉论文编撰
│   ├── phase4.py                  # 主程序：论文生成与格式化
│   ├── README_PHASE4.md           # Phase 4 使用文档
│   └── 输出文件/
│       ├── phase4_output.json     # 完整论文内容
│       └── paper_output/          # LaTeX和PDF文件
│
├── 🛠️ 工具与配置
│   ├── doubao_use.py              # 豆包API使用示例
│   ├── .env.example               # 环境变量模板
│   └── requirements.txt           # Python依赖
│
└── 📚 文档
    ├── examples.sh                # 使用示例
    └── lib/                       # 前端可视化库
```

---

## ✅ Phase 1 状态：已完成

### 功能清单

- ✅ 智能档案提取
- ✅ 学术关系挖掘
- ✅ 文献智能检索
- ✅ 知识图谱构建
- ✅ 多格式可视化
- ✅ 一键运行

### 快速开始

```bash
# 1. 设置API密钥
export ARK_API_KEY="你的豆包API密钥"

# 2. 运行Phase 1
python phase1.py "你的学术背景描述"

# 3. 查看结果
open phase1_kg_visualization.html
```

### 输出文件

- `phase1_output.json` - 完整数据
- `phase1_kg_visualization.html` - 交互式图谱
- `phase1_kg_visualization.png` - 静态图片

**详细文档**: 见 `README_PHASE1.md`

---

## ✅ Phase 2 状态：已完成

### 功能清单

- ✅ 三大对抗性Agent（激进派、保守派、刺客）
- ✅ 多轮辩论机制
- ✅ 用户交互决策
- ✅ Research Proposal生成
- ✅ 约束条件检验

### 快速开始

```bash
# 1. 运行Phase 2（自动加载phase1_output.json）
python phase2.py

# 2. 或指定输入文件
python phase2.py /path/to/phase1_output.json
```

### 输出文件

- `phase2_output.json` - 完整辩论记录与研究计划书

**详细文档**: 见 `README_PHASE2.md`

---

## ✅ Phase 3 状态：已完成

### 功能清单

- ✅ 任务分解器（DAG）
- ✅ 代码生成器
- ✅ 沙盒执行环境
- ✅ 哨兵监控（NaN/Inf检测）
- ✅ 评估器（客观评估）
- ✅ FARS机制（Git版本控制）
- ✅ 迭代优化机制

### 快速开始

```bash
# 1. 运行Phase 3（自动加载phase2_output.json）
python phase3.py

# 2. 或指定输入文件
python phase3.py /path/to/phase2_output.json
```

### 输出文件

- `phase3_output.json` - 完整执行记录
- `experiments/{exp_name}/` - 实验代码与结果

**详细文档**: 见 `README_PHASE3.md`

---

## ✅ Phase 4 状态：已完成

### 功能清单

- ✅ Academic Writer（学术编撰者）
- ✅ QA & Formatter（质检与格式化）
- ✅ 防幻觉验证机制
- ✅ LaTeX格式转换
- ✅ BibTeX引用生成
- ✅ PDF自动编译（需LaTeX环境）

### 快速开始

```bash
# 1. 运行Phase 4（自动加载phase3_output.json）
python phase4.py

# 2. 或指定输入文件和模板
python phase4.py /path/to/phase3_output.json neurips
```

### 输出文件

- `phase4_output.json` - 完整论文内容和元数据
- `paper_output/paper.tex` - LaTeX源码
- `paper_output/references.bib` - BibTeX引用
- `paper_output/paper.pdf` - PDF论文（需LaTeX）

**详细文档**: 见 `README_PHASE4.md`

---

## 🔧 环境配置

### 安装依赖

```bash
pip install openai python-dotenv networkx pyvis matplotlib
```

### 环境变量

创建 `.env` 文件：

```
ARK_API_KEY=你的豆包API密钥
```

或直接导出：

```bash
export ARK_API_KEY="你的豆包API密钥"
```

---

## 📊 当前进度

| 阶段 | 状态 | 完成度 | 说明 |
|------|------|--------|------|
| Phase 1 | ✅ 完成 | 100% | 知识图谱生成系统 |
| Phase 2 | ✅ 完成 | 100% | 多智能体辩论系统 |
| Phase 3 | ✅ 完成 | 100% | 沙盒执行与评估系统 |
| Phase 4 | ✅ 完成 | 100% | 防幻觉论文编撰系统 |

---

## 🎯 下一步

### 🎉 所有核心功能已完成！

AutoPaper 的四个核心阶段已全部实现：
- ✅ Phase 1: 知识图谱生成
- ✅ Phase 2: 多智能体辩论
- ✅ Phase 3: 沙盒执行与评估
- ✅ Phase 4: 防幻觉论文编撰

### 可选的增强功能

1. **支持更多AI模型**（GPT-4, Claude, 通义千问）
2. **Web界面** - 可视化的用户交互
3. **数据库持久化** - 存储历史记录
4. **分布式执行** - 支持多机并行
5. **实验对比** - 多个实验的横向对比
6. **论文模板库** - 更多期刊和会议模板

---

## 💡 使用示例

### 完整流程示例（Phase 1 → 2 → 3 → 4）

```bash
# 设置API密钥
export ARK_API_KEY="你的豆包API密钥"

# Step 1: 生成知识图谱
python phase1.py "我是清华大学计算机系博士生，研究深度学习和注意力机制"

# Step 2: 多智能体辩论
python phase2.py

# Step 3: 沙盒执行与评估
python phase3.py

# Step 4: 生成论文
python phase4.py

# Step 5: 查看最终结果
cat phase4_output.json
open paper_output/paper.pdf  # 如果安装了LaTeX
```

---

## 📚 文档索引

- **新手指南**: `README_PHASE1.md`
- **工作流程**: `WORKFLOW.md`
- **API文档**: `doubao_use.py`
- **示例集合**: `examples.sh`

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出改进建议！

---

## 📄 许可证

MIT License

---

**✅ AutoPaper 完整系统已开发完成！** 🎉
