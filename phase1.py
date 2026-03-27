#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AutoPaper Phase 1: 数据底座与图谱初始化
支持两种模式：
1. 快速模式：输入一句话，自动生成知识图谱
2. 详细模式：多轮对话深度调查
"""

import os
import json
import sys
from openai import OpenAI
from typing import Dict, List, Any, Optional
from datetime import datetime

# 初始化豆包客户端（兼容火山方舟）
api_key = os.getenv('ARK_API_KEY')
if not api_key:
    # 如果未设置环境变量，尝试从 .env 文件读取
    try:
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv('ARK_API_KEY')
    except ImportError:
        pass

client = None  # 延迟初始化


def get_client():
    """获取或初始化OpenAI客户端"""
    global client
    if client is None:
        api_key = os.getenv('ARK_API_KEY')
        if not api_key:
            raise ValueError("ARK_API_KEY 环境变量未设置")
        client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
            api_key=api_key
        )
    return client


class SmartProfileExtractor:
    """智能档案提取器 - 从一句话生成完整用户档案"""
    
    def __init__(self, user_input: str):
        self.user_input = user_input
        self.client = get_client()
        self.user_profile = {
            "education": [],
            "specialties": [],
            "advisors": [],
            "research_interests": [],
            "hardware_constraints": {},
            "datasets": [],
            "inspirations": [],
            "academic_relationships": [],  # 新增：学术关系
            "raw_input": user_input
        }
    
    def extract_from_description(self) -> Dict[str, Any]:
        """
        从用户的一句话描述中智能提取档案信息
        """
        print("\n" + "="*80)
        print("🔍 第1步：正在分析用户描述...")
        print("="*80 + "\n")
        
        extract_prompt = f"""分析以下人物背景描述，提取结构化信息：

用户描述：{self.user_input}

请提取以下信息并返回JSON格式：
{{
    "education": ["最高学历", "专业方向"],
    "specialties": ["专业方向1", "专业方向2"],
    "advisor_info": [
        {{
            "name": "导师/机构名称",
            "research_direction": "研究方向",
            "academic_school": "学术流派"
        }}
    ],
    "research_interests": ["研究兴趣1", "研究兴趣2"],
    "hardware_info": {{
        "available": "硬件描述或'未提及'",
        "constraints": ["约束条件1", "约束条件2"]
    }},
    "special_datasets": ["数据集1", "数据集2"],
    "inspirations": ["灵感1", "灵感2"],
    "keywords": ["关键词1", "关键词2", "关键词3"]
}}

注意：如果某些信息未在描述中提及，保持对应字段为空数组或空对象。
只返回JSON，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": extract_prompt}],
            temperature=0.5,
        )
        
        extracted_text = response.choices[0].message.content
        
        try:
            extracted_data = json.loads(extracted_text)
            
            # 填充用户档案
            self.user_profile.update({
                "education": extracted_data.get("education", []),
                "specialties": extracted_data.get("specialties", []),
                "advisors": extracted_data.get("advisor_info", []),
                "research_interests": extracted_data.get("research_interests", []),
                "hardware_constraints": extracted_data.get("hardware_info", {}),
                "datasets": extracted_data.get("special_datasets", []),
                "inspirations": extracted_data.get("inspirations", []),
                "keywords": extracted_data.get("keywords", [])
            })
            
            print("✅ 档案信息提取成功！")
            print(f"   教育背景: {', '.join(self.user_profile['education']) or '未提及'}")
            print(f"   专业方向: {', '.join(self.user_profile['specialties'][:2]) or '未提及'}")
            print(f"   研究兴趣: {', '.join(self.user_profile['research_interests'][:2]) or '未提及'}")
            
        except json.JSONDecodeError:
            print(f"⚠️  JSON解析失败，保存原始文本")
            self.user_profile["extraction_raw"] = extracted_text
        
        return self.user_profile
    
    def extract_academic_relationships(self) -> List[Dict[str, Any]]:
        """
        从描述中提取学术关系网络
        返回：[(person1, person2, relation_type), ...]
        """
        print("\n" + "="*80)
        print("🔗 第2步：正在提取学术关系网络...")
        print("="*80 + "\n")
        
        relationship_prompt = f"""基于这个人物背景，提取所有可能的学术关系网络：

用户描述：{self.user_input}

已提取的信息：
- 教育背景：{', '.join(self.user_profile.get('education', [])) or '未提及'}
- 导师/机构：{', '.join([a.get('name', '') for a in self.user_profile.get('advisors', [])]) or '未提及'}
- 专业方向：{', '.join(self.user_profile.get('specialties', [])) or '未提及'}

请返回JSON格式，包含所有可推断的学术关系：
{{
    "relationships": [
        {{
            "person1": "人物1",
            "person2": "人物2",
            "relation_type": "导师关系/同事/合作者/学生/引用影响",
            "confidence": "高/中/低",
            "description": "关系描述"
        }}
    ],
    "institutions": ["机构1", "机构2"],
    "collaborators": [
        {{
            "name": "合作者名字",
            "type": "直接合作者/潜在合作者",
            "research_overlap": "研究重叠领域"
        }}
    ]
}}

只返回JSON，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": relationship_prompt}],
            temperature=0.5,
        )
        
        relationship_text = response.choices[0].message.content
        
        try:
            relationship_data = json.loads(relationship_text)
            self.user_profile["academic_relationships"] = relationship_data.get("relationships", [])
            
            print(f"✅ 提取学术关系成功！")
            print(f"   发现关系数: {len(relationship_data.get('relationships', []))}")
            print(f"   相关机构: {', '.join(relationship_data.get('institutions', [])[:3]) or '未提及'}")
            
            # 显示前几个关系
            for rel in relationship_data.get("relationships", [])[:3]:
                print(f"   • {rel.get('person1', '')} -[{rel.get('relation_type', '')}]-> {rel.get('person2', '')}")
            
        except json.JSONDecodeError:
            print(f"⚠️  关系提取失败")
            self.user_profile["relationships_raw"] = relationship_text
        
        return self.user_profile.get("academic_relationships", [])


class SmartLiteratureCrawler:
    """智能文献爬虫 - 基于关键词自动检索相关文献"""
    
    def __init__(self, user_profile: Dict[str, Any]):
        self.user_profile = user_profile
        self.client = get_client()
        self.literature_database = []
    
    def search_literature(self) -> List[Dict[str, Any]]:
        """根据提取的关键词和研究兴趣检索学术文献"""
        
        print("\n" + "="*80)
        print("📚 正在检索相关学术文献...")
        print("="*80 + "\n")
        
        # 构造搜索关键词
        keywords = self.user_profile.get("keywords", [])
        research_interests = self.user_profile.get("research_interests", [])
        specialties = self.user_profile.get("specialties", [])
        
        search_keywords = list(set(keywords + research_interests[:2] + specialties[:2]))
        search_keywords_str = ", ".join(search_keywords[:5]) if search_keywords else "学术研究"
        
        search_query = f"""基于以下研究背景，我需要推荐相关的学术论文：

研究关键词: {search_keywords_str}
用户背景: {self.user_profile.get('raw_input', '')}

请推荐8-12篇最相关的学术论文（真实存在的论文），包括：
1. 论文标题
2. 作者
3. 发表年份（2020年以后优先）
4. 简要摘要（2-3句话）
5. 与研究的关联度（高/中/低）
6. GitHub代码仓库链接（如有）
7. 核心概念关键词

请以JSON数组格式返回，只返回JSON数组，不要其他文本。格式如下：
[
    {{
        "title": "论文标题",
        "authors": ["作者1", "作者2"],
        "year": 2024,
        "abstract": "摘要内容",
        "relevance": "高",
        "github_link": "GitHub链接或null",
        "key_concepts": ["概念1", "概念2"]
    }}
]"""
        
        response = client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": search_query}],
            temperature=0.6,
        )
        
        search_result = response.choices[0].message.content
        
        try:
            self.literature_database = json.loads(search_result)
            print(f"✅ 检索到 {len(self.literature_database)} 篇相关文献")
            for lit in self.literature_database[:3]:
                print(f"   • {lit.get('title', '未知')[:60]}...")
        except json.JSONDecodeError:
            print(f"⚠️  文献检索失败，保存原始结果")
            self.literature_database = [{"raw_content": search_result}]
        
        return self.literature_database


class SmartKGBuilder:
    """智能知识图谱构建器 - 自动构建学术关系网络"""
    
    def __init__(self, user_profile: Dict[str, Any], literature: List[Dict[str, Any]]):
        self.user_profile = user_profile
        self.literature = literature
        self.client = get_client()
        self.knowledge_graph = {
            "nodes": [],
            "edges": [],
            "metadata": {},
            "core_concepts": [],
            "research_landscape": ""
        }
    
    def build_graph(self) -> Dict[str, Any]:
        """智能构建知识图谱"""
        
        print("\n" + "="*80)
        print("🧠 正在构建知识图谱...")
        print("="*80 + "\n")
        
        profile_text = json.dumps(self.user_profile, ensure_ascii=False, indent=2)
        literature_text = json.dumps(self.literature, ensure_ascii=False, indent=2)
        
        kg_prompt = f"""基于以下用户背景和相关文献，构建一个学术知识图谱。

用户背景：
{profile_text}

相关文献：
{literature_text}

请创建一个知识图谱，包含：

1. **节点(Nodes)** - 提取以下实体：
   - 用户相关实体：用户本身、导师、机构、专业领域
   - 论文相关实体：论文、作者、研究方法、核心概念、技术方案
   - 实体类型应包括：Person, Concept, Method, Dataset, ResearchArea, Institution

2. **边(Edges)** - 表示实体间的关系：
   - works_with(协作)
   - studies(研究)
   - cites(引用)
   - related_to(相关)
   - implements(实现)
   - authored_by(作者)
   - works_at(工作)

3. **核心概念汇总** - 研究领域的关键概念及重要性

4. **研究全景** - 用3-5句话总结研究方向

请返回JSON格式（只返回JSON，不要其他文本）：
{{
    "nodes": [
        {{"id": "unique_id", "label": "显示标签", "type": "Person/Concept/Method/Dataset/ResearchArea/Institution", "description": "简短描述"}}
    ],
    "edges": [
        {{"source": "node_id1", "target": "node_id2", "relation": "关系类型", "weight": 0.5}}
    ],
    "core_concepts": [
        {{"concept": "概念名称", "importance": "高/中/低", "related_to_user": true/false}}
    ],
    "research_landscape": "研究全景描述"
}}"""
        
        response = client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": kg_prompt}],
            temperature=0.6,
        )
        
        kg_result = response.choices[0].message.content
        
        try:
            self.knowledge_graph = json.loads(kg_result)
            print(f"✅ 知识图谱构建成功！")
            print(f"   节点数: {len(self.knowledge_graph.get('nodes', []))}")
            print(f"   关系数: {len(self.knowledge_graph.get('edges', []))}")
            print(f"   核心概念: {len(self.knowledge_graph.get('core_concepts', []))}")
        except json.JSONDecodeError:
            print(f"⚠️  知识图谱JSON解析失败")
            self.knowledge_graph = {
                "raw_content": kg_result,
                "status": "raw_text_only"
            }
        
        return self.knowledge_graph


def quick_mode(description: str, visualize: bool = True):
    """快速模式：一句话输入，自动生成知识图谱"""
    
    print("\n" + "="*80)
    print("🚀 AutoPaper Phase 1 - 快速知识图谱生成")
    print("="*80)
    print(f"\n📝 用户输入: {description}\n")
    
    try:
        # 步骤1：提取用户档案
        print("⏳ 正在执行第1步...")
        extractor = SmartProfileExtractor(description)
        user_profile = extractor.extract_from_description()
        
        # 步骤2：提取学术关系（新增）
        print("\n⏳ 正在执行第2步...")
        relationships = extractor.extract_academic_relationships()
        
        # 步骤3：检索文献
        print("\n⏳ 正在执行第3步...")
        crawler = SmartLiteratureCrawler(user_profile)
        literature = crawler.search_literature()
        
        # 步骤4：构建知识图谱
        print("\n⏳ 正在执行第4步...")
        kg_builder = SmartKGBuilder(user_profile, literature)
        knowledge_graph = kg_builder.build_graph()
        
        # 保存输出
        phase1_output = {
            "user_profile": user_profile,
            "literature": literature,
            "knowledge_graph": knowledge_graph,
            "timestamp": datetime.now().isoformat(),
            "phase": 1,
            "mode": "quick"
        }
        
        output_file = "/Users/leave/Desktop/fc/AutoPaper/phase1_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(phase1_output, f, ensure_ascii=False, indent=2)
        
        # 生成统计报告
        print("\n" + "="*80)
        print("✅ Phase 1 完成！")
        print("="*80)
        print(f"\n📊 输出文件: {output_file}")
        print(f"\n📈 知识图谱概况:")
        print(f"   • 节点总数: {len(knowledge_graph.get('nodes', []))}")
        print(f"   • 关系总数: {len(knowledge_graph.get('edges', []))}")
        print(f"   • 核心概念: {len(knowledge_graph.get('core_concepts', []))}")
        print(f"   • 学术关系: {len(relationships)}")
        
        # 显示核心概念
        core_concepts = knowledge_graph.get('core_concepts', [])
        if core_concepts:
            print(f"\n🎯 核心概念（前5个）:")
            for concept in core_concepts[:5]:
                importance = concept.get('importance', '中')
                related = "✓" if concept.get('related_to_user') else "✗"
                print(f"   • {concept.get('concept', '')} [{importance}] {related}")
        
        # 显示研究全景
        landscape = knowledge_graph.get('research_landscape', '')
        if landscape:
            print(f"\n🌍 研究全景:")
            # 截断长文本，但保留完整句子
            landscape_preview = landscape[:300]
            if len(landscape) > 300:
                landscape_preview += "..."
            print(f"   {landscape_preview}")
        
        # 显示学术关系摘要
        if relationships:
            print(f"\n🔗 学术关系发现（前3个）:")
            for rel in relationships[:3]:
                rel_type = rel.get('relation_type', '未知')
                confidence = rel.get('confidence', '中')
                print(f"   • {rel.get('person1', '')} -[{rel_type}({confidence})]-> {rel.get('person2', '')}")
        
        # 一键可视化
        if visualize:
            print(f"\n📊 正在生成可视化...")
            try:
                # 动态导入可视化工具
                import sys
                sys.path.insert(0, '/Users/leave/Desktop/fc/AutoPaper')
                from visualize_kg import KnowledgeGraphVisualizer
                
                visualizer = KnowledgeGraphVisualizer(output_file)
                html_file = visualizer.generate_html_visualization()
                print(f"✅ 可视化已生成")
                print(f"   💡 在浏览器中打开: open {html_file}")
            except Exception as e:
                print(f"⚠️  可视化生成失败: {e}")
                print(f"   💡 手动运行: python visualize_kg.py")
        
        print("\n" + "="*80)
        print("🎉 任务完成！")
        print("="*80 + "\n")
        
        return phase1_output
        
    except ValueError as e:
        print(f"\n❌ 错误: {e}")
        return None
    except Exception as e:
        print(f"\n❌ 意外错误: {e}")
        import traceback
        traceback.print_exc()
        return None


def interactive_mode():
    """交互模式：多轮对话深度调查"""
    
    print("\n" + "="*80)
    print("🎯 AutoPaper Phase 1 - 交互深度调查模式")
    print("="*80)
    print("\n请输入你的学术背景描述（可以很长）:")
    print("包括：教育经历、专业方向、导师信息、研究兴趣、硬件条件、特殊数据集等\n")
    
    # 收集用户输入
    description_lines = []
    print("(按两次回车完成输入)")
    empty_count = 0
    
    while empty_count < 2:
        line = input()
        if line.strip() == "":
            empty_count += 1
        else:
            empty_count = 0
            description_lines.append(line)
    
    user_description = "\n".join(description_lines)
    
    if not user_description.strip():
        print("❌ 输入不能为空")
        return None
    
    return quick_mode(user_description)


def main():
    """主函数"""
    
    # 检查API密钥
    if not os.getenv('ARK_API_KEY'):
        print("❌ 错误：未设置 ARK_API_KEY 环境变量")
        print("请运行: export ARK_API_KEY='你的API密钥'")
        return
    
    # 判断运行模式
    if len(sys.argv) > 1:
        # 命令行模式：python phase1.py "用户描述"
        user_input = " ".join(sys.argv[1:])
        quick_mode(user_input)
    else:
        # 交互模式
        interactive_mode()


if __name__ == "__main__":
    """
    AutoPaper Phase 1 - 一句话生成知识图谱
    
    使用方式：
    
    1️⃣  命令行快速模式（推荐）：
        export ARK_API_KEY="你的API密钥"
        python phase1.py "你的学术背景描述"
        
        示例：
        python phase1.py "我是浙江大学计算机系的博士生，师从张三教授研究深度学习，特别关注NLP中的长文本问题"
    
    2️⃣  交互模式：
        export ARK_API_KEY="你的API密钥"
        python phase1.py
        （然后输入详细背景）
    
    3️⃣  禁用自动可视化：
        python phase1.py "描述" 2>/dev/null
    
    输出文件：
        - phase1_output.json: 完整的输出数据（用户档案、文献、知识图谱）
        - phase1_kg_visualization.html: 可交互的知识图谱可视化
        - phase1_kg_visualization.png: 静态知识图谱图片
        - phase1_kg_tree.json: 树形结构化数据
    
    功能：
        ✅ 智能档案提取：自动解析学术背景、教育经历、专业方向
        ✅ 学术关系挖掘：发现导师关系、合作者、学术流派
        ✅ 文献检索：推荐相关学术论文及GitHub代码
        ✅ 知识图谱构建：自动生成学术关系网络图谱
        ✅ 可视化展示：生成多种格式的可视化结果
    """
    main()
