#!/bin/bash
# AutoPaper Phase 1 使用示例

echo "🚀 AutoPaper Phase 1 使用示例"
echo "=============================="
echo ""

# 检查API密钥
if [ -z "$ARK_API_KEY" ]; then
    echo "❌ 错误：未设置 ARK_API_KEY 环境变量"
    echo ""
    echo "请先运行："
    echo '  export ARK_API_KEY="你的豆包API密钥"'
    echo ""
    echo "获取API密钥："
    echo "  https://console.volcengine.com/ark/region:ark+cn-beijing/apikey"
    exit 1
fi

echo "✅ API密钥已设置"
echo ""

# 示例1：简短描述
echo "📝 示例1：简短描述"
echo "命令："
echo 'python phase1.py "我是自然语言处理研究者，关注大模型安全对齐"'
echo ""

# 示例2：详细描述
echo "📝 示例2：详细描述"
echo "命令："
echo 'python phase1.py "我是北京大学计算机系博士生，师从某教授，研究大语言模型的长上下文处理问题，拥有GPU集群资源和医疗领域标注数据"'
echo ""

# 示例3：交互模式
echo "📝 示例3：交互模式（无命令行参数）"
echo "命令："
echo "python phase1.py"
echo "然后按提示输入你的背景描述"
echo ""

# 示例4：查看可视化
echo "📝 示例4：查看可视化知识图谱"
echo "第1步：生成可视化"
echo "  python visualize_kg.py"
echo ""
echo "第2步：打开网页版（推荐）"
echo "  open phase1_kg_visualization.html"
echo ""
echo "第3步：或查看PNG图片"
echo "  open phase1_kg_visualization.png"
echo ""

# 示例5：查看输出数据
echo "📝 示例5：查看生成的JSON输出"
echo "命令："
echo "  cat phase1_output.json | python -m json.tool | head -100"
echo ""

# 快速测试
echo "🚀 现在让我们运行一个快速示例..."
echo ""
echo "✏️  输入示例描述（或按Ctrl+C跳过）："
read -r -t 5 user_input || {
    echo ""
    echo "⏭️  跳过示例，显示帮助信息"
    echo ""
    echo "💡 下一步："
    echo "1. 设置API密钥："
    echo '   export ARK_API_KEY="你的密钥"'
    echo ""
    echo "2. 运行phase1："
    echo '   python phase1.py "你的背景描述"'
    echo ""
    echo "3. 查看结果："
    echo "   python visualize_kg.py"
    echo "   open phase1_kg_visualization.html"
    echo ""
    exit 0
}

if [ -z "$user_input" ]; then
    echo "使用默认示例..."
    user_input="我是AI研究者，专注于大语言模型的长上下文处理，在字节跳动工作，拥有丰富的中文预训练语料库"
fi

echo ""
echo "运行Phase 1..."
python phase1.py "$user_input"

echo ""
echo "✅ Phase 1 完成！"
echo ""
echo "💡 接下来："
echo "1. 生成可视化："
echo "   python visualize_kg.py"
echo ""
echo "2. 打开可视化："
echo "   open phase1_kg_visualization.html"
echo ""
