# AutoPaper Phase 1 - 一句话生成知识图谱 🚀

## 功能概述

**只需一句话描述你的学术背景，自动生成完整的学术知识图谱！**

### 核心功能 ✨

- **智能档案提取**：自动解析教育背景、专业方向、研究兴趣
- **学术关系挖掘**：发现导师关系、合作者、学术流派
- **文献智能检索**：推荐相关学术论文及GitHub代码
- **知识图谱构建**：自动生成学术关系网络图谱
- **多格式可视化**：HTML交互式、PNG静态图片、JSON树形数据

---

## 快速开始 🎯

### 1. 设置环境

```bash
# 设置豆包API密钥（必需）
export ARK_API_KEY="你的API密钥"

# 或者创建 .env 文件
echo "ARK_API_KEY=你的API密钥" > .env
pip install python-dotenv  # 如果使用.env文件
```

### 2. 运行（三种方式）

#### 方式1：命令行快速模式（推荐）✅

```bash
python phase1.py "你的学术背景描述"
```

**示例：**

```bash
python phase1.py "我是浙江大学计算机系的博士生，师从张三教授研究深度学习，特别关注NLP中的长文本问题"

python phase1.py "MIT的深度学习方向博士，导师Yann LeCun，研究长序列处理和注意力机制优化"

python phase1.py "清华大学数学系硕士，在腾讯AI Lab实习，研究知识图谱和推荐系统，有5TB训练数据集"
```

#### 方式2：交互模式

```bash
python phase1.py
```

然后按照提示输入详细背景，按两次回车提交。

#### 方式3：Python脚本调用

```python
from phase1 import quick_mode

result = quick_mode("我是MIT博士生，研究深度学习...")

# 访问结果
user_profile = result['user_profile']
literature = result['literature']
knowledge_graph = result['knowledge_graph']
```

---

## 输出文件 📁

运行后将生成以下文件：

| 文件名 | 描述 | 用途 |
|--------|------|------|
| `phase1_output.json` | 完整输出数据 | 包含用户档案、文献列表、知识图谱 |
| `phase1_kg_visualization.html` | 交互式可视化 | 🌐 **在浏览器中打开查看** |
| `phase1_kg_visualization.png` | 静态图片 | 📸 用于报告、展示 |
| `phase1_kg_tree.json` | 树形数据 | 🔧 可导入Obsidian等工具 |

### 查看可视化

```bash
# 自动生成后，在浏览器中打开
open phase1_kg_visualization.html

# 或手动运行可视化工具
python visualize_kg.py
```

---

## 输出示例 🎨

### 执行流程

```
🚀 AutoPaper Phase 1 - 快速知识图谱生成
================================================================================

📝 用户输入: 我是MIT计算机系深度学习方向的博士生...

⏳ 正在执行第1步...

================================================================================
🔍 第1步：正在分析用户描述...
================================================================================

✅ 档案信息提取成功！
   教育背景: MIT博士, 计算机系
   专业方向: 深度学习, 自然语言处理
   研究兴趣: 长序列处理, 注意力机制优化

⏳ 正在执行第2步...

================================================================================
🔗 第2步：正在提取学术关系网络...
================================================================================

✅ 提取学术关系成功！
   发现关系数: 5
   相关机构: MIT, Facebook AI Research, NYU
   • 用户 -[导师关系]-> Yann LeCun
   • Yann LeCun -[引用影响]-> Geoffrey Hinton
   • 用户 -[研究]-> Transformer架构

⏳ 正在执行第3步...

================================================================================
📚 正在检索相关学术文献...
================================================================================

✅ 检索到 10 篇相关文献
   • Attention Is All You Need...
   • BERT: Pre-training of Deep Bidirectional Transformers...
   • GPT-3: Language Models are Few-Shot Learners...

⏳ 正在执行第4步...

================================================================================
🧠 正在构建知识图谱...
================================================================================

✅ 知识图谱构建成功！
   节点数: 35
   关系数: 42
   核心概念: 12

================================================================================
✅ Phase 1 完成！
================================================================================

📊 输出文件: /Users/leave/Desktop/fc/AutoPaper/phase1_output.json

📈 知识图谱概况:
   • 节点总数: 35
   • 关系总数: 42
   • 核心概念: 12
   • 学术关系: 5

🎯 核心概念（前5个）:
   • Transformer架构 [高] ✓
   • 注意力机制 [高] ✓
   • 长序列建模 [高] ✓
   • BERT模型 [中] ✗
   • 自监督学习 [中] ✓

🌍 研究全景:
   本知识图谱围绕深度学习在自然语言处理领域的长序列处理展开...

🔗 学术关系发现（前3个）:
   • 用户 -[导师关系(高)]-> Yann LeCun
   • Yann LeCun -[引用影响(高)]-> Geoffrey Hinton
   • 用户 -[研究(高)]-> Transformer架构

📊 正在生成可视化...
✅ 可视化已生成
   💡 在浏览器中打开: open /Users/leave/Desktop/fc/AutoPaper/phase1_kg_visualization.html

================================================================================
🎉 任务完成！
================================================================================
```

---

## 工作原理 🔬

### 技术架构

```
用户输入（一句话）
    ↓
[SmartProfileExtractor]
    ├─ 提取教育背景、专业方向
    ├─ 识别导师/机构信息
    ├─ 解析研究兴趣关键词
    └─ 挖掘学术关系网络
    ↓
[SmartLiteratureCrawler]
    ├─ 基于关键词检索文献
    ├─ 推荐相关论文
    └─ 收集GitHub代码链接
    ↓
[SmartKGBuilder]
    ├─ 融合用户档案和文献
    ├─ 提取实体（人物、概念、方法）
    ├─ 构建关系边（导师、引用、研究）
    └─ 生成知识图谱JSON
    ↓
[Visualization]
    ├─ HTML交互式可视化
    ├─ PNG静态图片
    └─ JSON树形数据
```

### 知识图谱结构

```json
{
  "nodes": [
    {
      "id": "user_001",
      "label": "用户",
      "type": "Person",
      "description": "MIT博士生"
    },
    {
      "id": "concept_transformer",
      "label": "Transformer架构",
      "type": "Concept",
      "description": "注意力机制核心技术"
    }
  ],
  "edges": [
    {
      "source": "user_001",
      "target": "advisor_yann",
      "relation": "works_with",
      "weight": 1.0
    }
  ],
  "core_concepts": [
    {
      "concept": "注意力机制",
      "importance": "高",
      "related_to_user": true
    }
  ],
  "research_landscape": "研究全景描述..."
}
```

---

## 高级用法 🔧

### 1. 定制输出路径

修改 `phase1.py` 中的 `output_file` 变量：

```python
output_file = "/自定义/路径/phase1_output.json"
```

### 2. 禁用自动可视化

```python
quick_mode(description, visualize=False)
```

### 3. 批量处理

```python
descriptions = [
    "清华大学计算机系...",
    "Stanford AI Lab...",
    "MSRA研究员..."
]

for desc in descriptions:
    quick_mode(desc)
```

### 4. 集成到你的工作流

```python
from phase1 import SmartProfileExtractor, SmartLiteratureCrawler, SmartKGBuilder

# 分步执行
extractor = SmartProfileExtractor("我是...")
profile = extractor.extract_from_description()
relationships = extractor.extract_academic_relationships()

crawler = SmartLiteratureCrawler(profile)
literature = crawler.search_literature()

kg_builder = SmartKGBuilder(profile, literature)
kg = kg_builder.build_graph()

# 自定义处理...
```

---

## FAQ ❓

### Q1: 如何获取API密钥？

A: 访问 [火山方舟控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/apikey) 获取 `ARK_API_KEY`。

### Q2: 生成的知识图谱不准确怎么办？

A: 提供更详细的描述信息，包括：
- 具体的学校/机构名称
- 导师姓名和研究方向
- 研究领域的关键词
- 特殊的数据集或资源

### Q3: 可以处理中文输入吗？

A: 完全支持！中文和英文混合输入也没问题。

```bash
python phase1.py "我是清华大学计算机系博士生，师从李明教授研究强化学习"
```

### Q4: 生成时间需要多久？

A: 通常 30-60 秒，取决于网络速度和API响应时间。

### Q5: 能否导出为其他格式？

A: 是的！你可以基于 `phase1_output.json` 转换为：
- Gephi (.gexf)
- Neo4j (Cypher)
- Markdown
- PDF报告

---

## 故障排除 🔧

### 错误：`ARK_API_KEY 环境变量未设置`

```bash
export ARK_API_KEY="你的密钥"
```

### 错误：`JSON解析失败`

原因：AI模型返回格式不规范。

解决：重新运行，或提供更清晰的输入描述。

### 可视化生成失败

```bash
# 安装依赖
pip install networkx pyvis matplotlib

# 手动生成可视化
python visualize_kg.py
```

---

## 后续步骤 🎯

完成 Phase 1 后，你可以：

1. **查看知识图谱可视化** - 了解你的学术关系网络
2. **进入 Phase 2** - 多智能体辩论与方向收敛（开发中）
3. **导出数据** - 用于其他工具分析
4. **迭代优化** - 基于新的背景信息重新生成

---

## 贡献与反馈 💬

遇到问题或有改进建议？欢迎反馈！

---

## 许可证 📄

MIT License

---

**享受你的学术知识图谱之旅！🎉**
