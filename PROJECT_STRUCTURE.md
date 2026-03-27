# 📂 AutoPaper 项目结构

## 当前文件清单

```
AutoPaper/
│
├── 🔴 核心代码
│   ├── phase1.py ⭐ (14KB)
│   │   └── 新的快速模式：一句话生成知识图谱
│   │       ├── SmartProfileExtractor (档案提取)
│   │       ├── SmartLiteratureCrawler (文献检索)
│   │       ├── SmartKGBuilder (知识图谱构建)
│   │       └── quick_mode() / interactive_mode()
│   │
│   ├── visualize_kg.py ⭐ (16KB)
│   │   └── 知识图谱可视化
│   │       ├── KnowledgeGraphVisualizer (主类)
│   │       ├── print_text_summary() (文本摘要)
│   │       ├── generate_html_visualization() (网页版)
│   │       ├── generate_static_image() (PNG图片)
│   │       └── generate_json_tree() (JSON树)
│   │
│   └── doubao_use.py (1.1KB)
│       └── 豆包API使用示例
│
├── 📖 入门文档 (必读)
│   ├── QUICK_START.md ⭐ (3.6KB)
│   │   └── 新手快速指南（5分钟快速上手）
│   │       ├── 最简单的用法
│   │       ├── 环境要求
│   │       ├── 输入示例
│   │       └── 常见问题
│   │
│   └── SUMMARY.md (6.3KB)
│       └── 完整功能总结（本文件，2分钟了解全貌）
│           ├── 新旧对比
│           ├── 三种使用方式
│           ├── 输出说明
│           └── 下一步指引
│
├── 📚 详细文档
│   ├── README_PHASE1.md (4.1KB)
│   │   └── 详细使用指南（深入学习）
│   │       ├── 功能概述
│   │       ├── 输入格式建议
│   │       ├── 输出说明
│   │       ├── 使用技巧
│   │       ├── 工作流程图
│   │       └── FAQ
│   │
│   ├── UPDATE_NOTES.md (5.4KB)
│   │   └── 更新说明（了解改进）
│   │       ├── 主要改进
│   │       ├── 新增功能
│   │       ├── 代码改进
│   │       ├── 性能对比
│   │       └── 后续计划
│   │
│   └── WORKFLOW.md (4.7KB)
│       └── 完整工作流程（理解整体设计）
│           ├── Phase 1-4 说明
│           ├── Agent 职责
│           ├── 状态机流转
│           └── 校验规则
│
├── 🚀 快速工具
│   └── examples.sh (2.7KB)
│       └── 交互式示例脚本（可选）
│           ├── API检查
│           ├── 示例展示
│           └── 快速测试
│
├── 📊 输出文件 (运行后生成)
│   ├── phase1_output.json ✨
│   │   └── 完整结构化数据（主输出）
│   │       ├── user_profile (用户档案)
│   │       ├── literature (学术文献列表)
│   │       └── knowledge_graph (完整图谱)
│   │           ├── nodes (实体)
│   │           ├── edges (关系)
│   │           ├── core_concepts (核心概念)
│   │           └── research_landscape (研究全景)
│   │
│   ├── phase1_kg_visualization.html 💻 (运行visualize_kg.py生成)
│   │   └── 交互式网页版知识图谱（推荐查看）
│   │       ├── 可拖动节点
│   │       ├── 支持缩放
│   │       ├── 悬停显示详情
│   │       └── 自动物理仿真
│   │
│   ├── phase1_kg_visualization.png 📸 (运行visualize_kg.py生成)
│   │   └── 高清PNG静态图片
│   │
│   └── phase1_kg_tree.json 📄 (运行visualize_kg.py生成)
│       └── JSON树形结构（用于其他工具导入）
│
└── 🔧 配置文件 (可选)
    └── .env (自己创建，用于保存API密钥)
        └── ARK_API_KEY=your_key_here
```

---

## 📋 文件说明表

| 文件 | 类型 | 大小 | 用途 | 优先级 |
|------|------|------|------|--------|
| **phase1.py** | 核心代码 | 14KB | 生成知识图谱 | ⭐⭐⭐⭐⭐ |
| **visualize_kg.py** | 工具代码 | 16KB | 可视化图谱 | ⭐⭐⭐⭐ |
| **QUICK_START.md** | 文档 | 3.6KB | 快速上手 | ⭐⭐⭐⭐⭐ |
| **SUMMARY.md** | 文档 | 6.3KB | 功能总结 | ⭐⭐⭐⭐⭐ |
| **README_PHASE1.md** | 文档 | 4.1KB | 详细指南 | ⭐⭐⭐⭐ |
| **UPDATE_NOTES.md** | 文档 | 5.4KB | 更新说明 | ⭐⭐⭐ |
| **WORKFLOW.md** | 文档 | 4.7KB | 工作流程 | ⭐⭐⭐ |
| **examples.sh** | 脚本 | 2.7KB | 示例工具 | ⭐⭐ |
| **doubao_use.py** | 示例 | 1.1KB | API示例 | ⭐ |

---

## 🎯 快速导航

### 我是新手，现在就要开始
→ **QUICK_START.md** (5分钟)

### 我想快速了解全貌
→ **SUMMARY.md** (2分钟)

### 我想详细学习
→ **README_PHASE1.md** (15分钟)

### 我想知道改了什么
→ **UPDATE_NOTES.md** (5分钟)

### 我想理解整个系统
→ **WORKFLOW.md** (10分钟)

---

## 🚀 使用流程

### 第一次使用

```
1. 查看 QUICK_START.md
   ↓
2. 设置 ARK_API_KEY 环境变量
   ↓
3. 运行 python phase1.py "你的描述"
   ↓
4. 运行 python visualize_kg.py
   ↓
5. 打开 phase1_kg_visualization.html
```

### 后续使用

```
修改描述 → 运行 phase1.py → 查看结果
```

---

## 📊 代码架构

### Phase 1 - 主要类

```python
class SmartProfileExtractor
    ├── extract_from_description()
    └── 输出: user_profile (JSON)

class SmartLiteratureCrawler
    ├── search_literature()
    └── 输出: literature (JSON数组)

class SmartKGBuilder
    ├── build_graph()
    └── 输出: knowledge_graph (JSON)

class KnowledgeGraphVisualizer
    ├── print_text_summary()
    ├── generate_html_visualization()
    ├── generate_static_image()
    └── generate_json_tree()
```

---

## 📈 数据流

```
用户输入
   ↓
SmartProfileExtractor
   ↓ (user_profile)
SmartLiteratureCrawler
   ↓ (literature)
SmartKGBuilder
   ↓ (knowledge_graph)
phase1_output.json
   ↓
KnowledgeGraphVisualizer
   ↓
HTML / PNG / JSON
```

---

## 🔧 环境设置

### Python版本
- 需要：Python 3.8+
- 推荐：Python 3.10+

### 依赖包
```bash
pip install openai networkx pyvis matplotlib
```

### 环境变量
```bash
export ARK_API_KEY="your_key_here"
```

### 可选配置文件 (.env)
```
ARK_API_KEY=your_key_here
```

---

## 📁 输出目录说明

### phase1_output.json 结构

```json
{
  "user_profile": {
    "education": [],
    "specialties": [],
    "advisors": [],
    "research_interests": [],
    "hardware_constraints": {},
    "datasets": [],
    "inspirations": [],
    "keywords": []
  },
  "literature": [
    {
      "title": "...",
      "authors": [],
      "year": 2024,
      "abstract": "...",
      "relevance": "高",
      "github_link": "...",
      "key_concepts": []
    }
  ],
  "knowledge_graph": {
    "nodes": [],
    "edges": [],
    "core_concepts": [],
    "research_landscape": ""
  },
  "timestamp": "...",
  "phase": 1,
  "mode": "quick"
}
```

---

## 💾 存储位置

所有文件都保存在：
```
/Users/leave/Desktop/fc/AutoPaper/
```

### 输出文件位置
```
/Users/leave/Desktop/fc/AutoPaper/phase1_output.json
/Users/leave/Desktop/fc/AutoPaper/phase1_kg_visualization.html
/Users/leave/Desktop/fc/AutoPaper/phase1_kg_visualization.png
/Users/leave/Desktop/fc/AutoPaper/phase1_kg_tree.json
```

---

## ✅ 完整性检查

运行前确保有：
- [ ] phase1.py ✅
- [ ] visualize_kg.py ✅
- [ ] 所有 .md 文档 ✅
- [ ] examples.sh ✅
- [ ] ARK_API_KEY 设置 ✅

---

## 🎯 常见命令速查

```bash
# 查看快速开始
cat QUICK_START.md

# 查看完整总结
cat SUMMARY.md

# 运行phase1（快速模式）
python phase1.py "你的描述"

# 运行phase1（交互模式）
python phase1.py

# 生成可视化
python visualize_kg.py

# 查看HTML可视化
open phase1_kg_visualization.html

# 查看输出JSON
cat phase1_output.json | python -m json.tool

# 查看文本摘要
python visualize_kg.py | head -50

# 运行示例脚本
bash examples.sh

# 查看帮助信息
python phase1.py --help  # (未来功能)
```

---

## 📞 获取帮助

### 查找信息的优先级

1. **QUICK_START.md** - 最常见的问题
2. **SUMMARY.md** - 功能总览
3. **README_PHASE1.md** - 详细说明
4. **UPDATE_NOTES.md** - 技术细节
5. **WORKFLOW.md** - 系统设计

---

**项目版本：** 2.0  
**最后更新：** 2026年3月26日  
**维护状态：** ✅ 积极维护
