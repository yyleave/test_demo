# 🚀 AutoPaper Phase 1 - 快速开始指南

## ⚡ 最简单的用法（只需一句话！）

### 步骤1：设置API密钥
```bash
export ARK_API_KEY="你的豆包API密钥"
```

### 步骤2：输入一句话生成知识图谱
```bash
cd /Users/leave/Desktop/fc/AutoPaper

# 输入你的背景描述
python phase1.py "我是一名AI研究者，专注于大语言模型的长上下文处理，在字节跳动工作，有丰富的中文预训练语料"
```

**就这么简单！** 🎉

---

## 📊 生成的输出文件

运行完成后，你会得到：

1. **`phase1_output.json`** - 完整的结构化数据
   - 用户档案（教育、专业方向、研究兴趣等）
   - 检索到的学术论文列表
   - 构建的知识图谱

2. **知识图谱可视化**（运行 `visualize_kg.py` 后生成）
   - `phase1_kg_visualization.html` - 💻 交互式网页版（推荐！）
   - `phase1_kg_visualization.png` - 📸 静态图片
   - `phase1_kg_tree.json` - 📄 JSON树形结构

---

## 👀 查看知识图谱

### 方式1：交互式网页版（推荐）
```bash
# 先生成可视化文件
python visualize_kg.py

# 用浏览器打开
open /Users/leave/Desktop/fc/AutoPaper/phase1_kg_visualization.html
```

**功能：**
- 🖱️ 拖动节点调整布局
- 🔍 滚轮放大/缩小
- ✨ 悬停显示节点详情

### 方式2：命令行文本版
```bash
python visualize_kg.py | head -100
```

---

## 🎯 输入示例

### 简短示例（推荐新手）
```bash
python phase1.py "我是博士生，研究NLP，导师是某教授，关心长文本理解和知识图谱应用"
```

### 详细示例（获得更好结果）
```bash
python phase1.py "
我是北京大学计算机科学与技术系的博士生，
师从某院士，主要研究方向是自然语言处理和大语言模型。
具体关注两个问题：
1. 大模型的长上下文中间信息遗忘
2. 专业领域的幻觉问题

我们实验室有GPU集群资源和医疗/法律标注数据集。
"
```

---

## ⚙️ 环境要求

### Python包
```bash
pip install openai networkx pyvis matplotlib
```

### API密钥获取
1. 访问：https://console.volcengine.com/ark/region:ark+cn-beijing/apikey
2. 创建新密钥或复制现有密钥
3. 运行：`export ARK_API_KEY="你的密钥"`

---

## 📈 工作流程

```
┌─ 输入一句话 ─┐
│              ↓
│  档案提取 ← AI智能分析
│              ↓
│  文献检索 ← 学术数据库
│              ↓
│  知识图谱 ← 关系抽取
│              ↓
│ 生成可视化 ← JSON/HTML/PNG
└──────────────┘
```

---

## 💡 使用技巧

### 1. 获得更多相关文献
→ 在描述中包含具体的研究问题和方向

### 2. 优化知识图谱质量
→ 提供更详细的背景和研究兴趣

### 3. 重新生成
→ 直接用新描述再运行一次

### 4. 调试问题
→ 查看 `phase1_output.json` 中的原始数据

---

## ❓ 常见问题

**Q: 可以离线运行吗？**
A: 不行，需要调用豆包API

**Q: 生成多少篇论文？**
A: 通常 8-12 篇，取决于关键词相关度

**Q: 知识图谱有多大？**
A: 通常 30-50 个节点，取决于输入复杂度

**Q: 结果不满意怎么办？**
A: 提供更详细的描述重新运行

---

## 🔗 下一步

Phase 1 完成后，可以进行：

- **Phase 2** 多智能体辩论与方向收敛
- **Phase 3** 沙盒执行与评估闭环
- **Phase 4** 防幻觉论文编撰

查看详细工作流程：`WORKFLOW.md`

---

**现在就开始吧！** 🚀

```bash
export ARK_API_KEY="your_key_here"
python phase1.py "你的背景描述"
```
