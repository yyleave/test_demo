#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
知识图谱可视化工具 - 支持多种展示方式
"""

import json
import os
from typing import Dict, List, Any, Optional

# 尝试导入可视化库
try:
    import networkx as nx
    NETWORKX_AVAILABLE = True
except ImportError:
    NETWORKX_AVAILABLE = False

try:
    import pyvis.network as net
    PYVIS_AVAILABLE = True
except ImportError:
    PYVIS_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False


class KnowledgeGraphVisualizer:
    """知识图谱可视化器"""
    
    def __init__(self, phase1_output_path: str):
        """
        初始化可视化器
        
        Args:
            phase1_output_path: Phase 1输出JSON文件路径
        """
        with open(phase1_output_path, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
        
        self.kg = self.data.get('knowledge_graph', {})
        self.user_profile = self.data.get('user_profile', {})
        self.literature = self.data.get('literature', [])
    
    def print_text_summary(self):
        """打印文本格式的知识图谱总结"""
        print("\n" + "="*80)
        print("📊 知识图谱 - 文本视图")
        print("="*80 + "\n")
        
        # 节点信息
        nodes = self.kg.get('nodes', [])
        print(f"【节点总数】{len(nodes)}\n")
        
        # 按类型分类
        nodes_by_type = {}
        for node in nodes:
            node_type = node.get('type', 'Unknown')
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node)
        
        for node_type, type_nodes in nodes_by_type.items():
            print(f"【{node_type}】({len(type_nodes)}个)")
            for node in type_nodes:
                print(f"  • {node.get('label', node.get('id'))}")
                desc = node.get('description', '')
                if desc:
                    # 截断过长的描述
                    desc = desc[:60] + "..." if len(desc) > 60 else desc
                    print(f"    {desc}")
            print()
        
        # 边信息
        edges = self.kg.get('edges', [])
        print(f"\n【关系总数】{len(edges)}\n")
        
        # 按关系类型分类
        edges_by_relation = {}
        for edge in edges:
            relation = edge.get('relation', 'unknown')
            if relation not in edges_by_relation:
                edges_by_relation[relation] = []
            edges_by_relation[relation].append(edge)
        
        for relation, type_edges in edges_by_relation.items():
            print(f"【{relation}】({len(type_edges)}条)")
            for edge in type_edges[:5]:  # 只显示前5条
                source_label = next((n.get('label') for n in nodes if n.get('id') == edge.get('source')), edge.get('source'))
                target_label = next((n.get('label') for n in nodes if n.get('id') == edge.get('target')), edge.get('target'))
                weight = edge.get('weight', 1.0)
                print(f"  {source_label} --[{relation}]--> {target_label} (权重: {weight})")
            if len(type_edges) > 5:
                print(f"  ... 还有 {len(type_edges) - 5} 条关系")
            print()
        
        # 核心概念
        core_concepts = self.kg.get('core_concepts', [])
        if core_concepts:
            print(f"【核心概念】({len(core_concepts)}个)\n")
            for concept_obj in core_concepts:
                concept = concept_obj.get('concept', '')
                importance = concept_obj.get('importance', '中')
                related = "✓" if concept_obj.get('related_to_user') else "✗"
                print(f"  {'高' if importance == '高' else '中' if importance == '中' else '低'}  {concept}  {'[与用户相关]' if related == '✓' else ''}")
        
        # 研究全景
        print(f"\n【研究全景】\n{self.kg.get('research_landscape', 'N/A')}\n")
    
    def generate_html_visualization(self, output_file: Optional[str] = None):
        """
        生成可交互的HTML可视化
        
        Args:
            output_file: 输出HTML文件路径，默认为phase1_kg_visualization.html
        """
        if not NETWORKX_AVAILABLE:
            print("❌ 需要安装 networkx")
            print("   运行: pip install networkx")
            return None
        
        if output_file is None:
            output_file = "/Users/leave/Desktop/fc/AutoPaper/phase1_kg_visualization.html"
        
        print(f"\n生成可交互HTML可视化... {output_file}")
        
        # 创建NetworkX图
        G = nx.DiGraph()
        
        nodes = self.kg.get('nodes', [])
        edges = self.kg.get('edges', [])
        
        # 添加节点和边
        for node in nodes:
            G.add_node(node.get('id'), 
                      label=node.get('label', node.get('id')))
        
        for edge in edges:
            G.add_edge(edge.get('source'), edge.get('target'))
        
        # 使用Pyvis生成HTML
        try:
            if PYVIS_AVAILABLE:
                net_vis = net.Network(directed=True, height='750px', width='100%')
                net_vis.from_nx(G)
                net_vis.write_html(output_file)
            else:
                # 如果pyvis不可用，生成简单的D3.js可视化HTML
                self._generate_simple_html(nodes, edges, output_file)
            
            print(f"✅ HTML可视化已生成: {output_file}")
            return output_file
        except Exception as e:
            print(f"   ⚠️  Pyvis生成失败: {e}")
            # 降级到简单HTML
            self._generate_simple_html(nodes, edges, output_file)
            return output_file
    
    def _generate_simple_html(self, nodes: List[Dict], edges: List[Dict], output_file: str):
        """生成简单的HTML可视化（不依赖Pyvis）"""
        
        node_type_colors = {
            'Person': '#FF6B6B',
            'Concept': '#4ECDC4',
            'Method': '#45B7D1',
            'Dataset': '#FFA07A',
            'ResearchArea': '#98D8C8',
        }
        
        # 构建节点JSON数据
        nodes_json = []
        for node in nodes:
            nodes_json.append({
                'id': node.get('id'),
                'label': node.get('label', node.get('id')),
                'color': node_type_colors.get(node.get('type', 'Unknown'), '#95E1D3'),
                'title': node.get('description', ''),
                'type': node.get('type', 'Unknown')
            })
        
        # 构建边JSON数据
        edges_json = []
        for edge in edges:
            edges_json.append({
                'from': edge.get('source'),
                'to': edge.get('target'),
                'label': edge.get('relation', ''),
                'title': edge.get('relation', '')
            })
        
        # 生成HTML
        html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Knowledge Graph Visualization</title>
    <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/vis/4.21.0/vis.min.css" rel="stylesheet" type="text/css" />
    <style type="text/css">
        html, body {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
        }}
        #network {{
            width: 100%;
            height: 100%;
            background-color: #f5f5f5;
            border: 1px solid #ddd;
        }}
        .info {{
            position: absolute;
            top: 10px;
            left: 10px;
            background: white;
            padding: 15px;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            z-index: 100;
            max-width: 300px;
        }}
        .info h3 {{
            margin: 0 0 10px 0;
            color: #333;
        }}
        .info p {{
            margin: 5px 0;
            color: #666;
            font-size: 12px;
        }}
    </style>
</head>
<body>
    <div class="info">
        <h3>🎨 知识图谱</h3>
        <p>节点总数: {len(nodes)}</p>
        <p>关系总数: {len(edges)}</p>
        <p>💡 提示: 拖动节点，滚轮缩放</p>
    </div>
    <div id="network"></div>
    <script type="text/javascript">
        var nodes = new vis.DataSet({json.dumps(nodes_json)});
        var edges = new vis.DataSet({json.dumps(edges_json)});
        
        var container = document.getElementById("network");
        var data = {{
            nodes: nodes,
            edges: edges
        }};
        var options = {{
            physics: {{
                enabled: true,
                barnesHut: {{
                    gravitationalConstant: -26000,
                    centralGravity: 0.3,
                    springLength: 200,
                    springConstant: 0.04
                }}
            }},
            interaction: {{
                navigationButtons: true,
                keyboard: true
            }}
        }};
        
        var network = new vis.Network(container, data, options);
    </script>
</body>
</html>"""
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✅ 简单HTML可视化已生成: {output_file}")
    
    def generate_static_image(self, output_file: Optional[str] = None):
        """
        生成静态图片
        
        Args:
            output_file: 输出PNG文件路径，默认为phase1_kg_visualization.png
        """
        if not NETWORKX_AVAILABLE or not MATPLOTLIB_AVAILABLE:
            print("❌ 需要安装 networkx 和 matplotlib")
            print("   运行: pip install networkx matplotlib")
            return None
        
        if output_file is None:
            output_file = "/Users/leave/Desktop/fc/AutoPaper/phase1_kg_visualization.png"
        
        print(f"\n生成静态图片... {output_file}")
        
        # 创建NetworkX图
        G = nx.DiGraph()
        
        nodes = self.kg.get('nodes', [])
        edges = self.kg.get('edges', [])
        
        # 添加节点
        for node in nodes:
            G.add_node(node.get('id'), label=node.get('label', node.get('id')))
        
        # 添加边
        for edge in edges:
            G.add_edge(edge.get('source'), edge.get('target'))
        
        # 绘制
        plt.figure(figsize=(20, 16))
        pos = nx.spring_layout(G, k=2, iterations=50, seed=42)
        
        # 节点颜色
        node_type_colors_map = {
            'Person': '#FF6B6B',
            'Concept': '#4ECDC4',
            'Method': '#45B7D1',
            'Dataset': '#FFA07A',
            'ResearchArea': '#98D8C8',
        }
        
        node_colors = []
        for node_id in G.nodes():
            node_obj = next((n for n in nodes if n.get('id') == node_id), None)
            node_type = node_obj.get('type', 'Unknown') if node_obj else 'Unknown'
            node_colors.append(node_type_colors_map.get(node_type, '#95E1D3'))
        
        # 绘制节点
        nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1000, alpha=0.9)
        
        # 绘制边
        nx.draw_networkx_edges(G, pos, edge_color='gray', arrows=True, 
                              arrowsize=20, arrowstyle='->', 
                              connectionstyle='arc3,rad=0.1', alpha=0.6, width=1.5)
        
        # 绘制标签
        labels = {node.get('id'): node.get('label', node.get('id')) for node in nodes}
        nx.draw_networkx_labels(G, pos, labels, font_size=8, font_weight='bold')
        
        plt.title("Knowledge Graph Visualization", fontsize=20, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"✅ 静态图片已生成: {output_file}")
        
        return output_file
    
    def generate_json_tree(self, output_file: Optional[str] = None):
        """
        生成JSON树形结构，用于其他工具可视化
        
        Args:
            output_file: 输出JSON文件路径，默认为phase1_kg_tree.json
        """
        if output_file is None:
            output_file = "/Users/leave/Desktop/fc/AutoPaper/phase1_kg_tree.json"
        
        print(f"\n生成JSON树形结构... {output_file}")
        
        # 构建树形结构
        tree = {
            "name": "Research Knowledge Graph",
            "children": []
        }
        
        # 按类型组织节点
        nodes = self.kg.get('nodes', [])
        nodes_by_type = {}
        
        for node in nodes:
            node_type = node.get('type', 'Unknown')
            if node_type not in nodes_by_type:
                nodes_by_type[node_type] = []
            nodes_by_type[node_type].append(node)
        
        for node_type, type_nodes in nodes_by_type.items():
            type_group = {
                "name": node_type,
                "children": [
                    {
                        "name": node.get('label', node.get('id')),
                        "description": node.get('description', ''),
                        "id": node.get('id')
                    }
                    for node in type_nodes
                ]
            }
            tree["children"].append(type_group)
        
        # 保存
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(tree, f, ensure_ascii=False, indent=2)
        
        print(f"✅ JSON树形结构已生成: {output_file}")
        return output_file
    
    def generate_statistics(self):
        """生成统计信息"""
        print("\n" + "="*80)
        print("📈 知识图谱统计")
        print("="*80 + "\n")
        
        nodes = self.kg.get('nodes', [])
        edges = self.kg.get('edges', [])
        
        print(f"节点总数: {len(nodes)}")
        print(f"边总数: {len(edges)}")
        
        # 度数统计
        if NETWORKX_AVAILABLE:
            G = nx.DiGraph()
            for edge in edges:
                G.add_edge(edge.get('source'), edge.get('target'))
            
            in_degrees = dict(G.in_degree())
            out_degrees = dict(G.out_degree())
            
            # 最重要的节点（入度最高）
            top_nodes = sorted(in_degrees.items(), key=lambda x: x[1], reverse=True)[:5]
            print(f"\n🎯 最重要的节点（被引用最多）:")
            for node_id, degree in top_nodes:
                node_label = next((n.get('label') for n in nodes if n.get('id') == node_id), node_id)
                print(f"  {node_label}: {degree}次")


def main():
    """主函数"""
    
    phase1_output_path = "/Users/leave/Desktop/fc/AutoPaper/phase1_output.json"
    
    # 检查文件是否存在
    if not os.path.exists(phase1_output_path):
        print(f"❌ 文件不存在: {phase1_output_path}")
        return
    
    # 初始化可视化器
    visualizer = KnowledgeGraphVisualizer(phase1_output_path)
    
    print("\n🎨 知识图谱可视化工具")
    print("="*80)
    
    # 1. 文本总结
    visualizer.print_text_summary()
    
    # 2. 统计信息
    visualizer.generate_statistics()
    
    # 3. 生成可视化文件
    print("\n📁 生成可视化文件...\n")
    
    # HTML可视化（推荐）
    try:
        html_file = visualizer.generate_html_visualization()
        if html_file:
            print(f"   💡 提示: 用浏览器打开: open {html_file}")
    except Exception as e:
        print(f"   ⚠️  HTML生成失败: {e}")
    
    # 静态图片
    try:
        visualizer.generate_static_image()
    except Exception as e:
        print(f"   ⚠️  静态图片生成失败: {e}")
    
    # JSON树
    try:
        visualizer.generate_json_tree()
    except Exception as e:
        print(f"   ⚠️  JSON树生成失败: {e}")
    
    print("\n✅ 可视化完成！")


if __name__ == "__main__":
    main()
