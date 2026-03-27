#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AutoPaper Phase 2: 多智能体辩论与方向收敛

通过对抗性辩论机制，从知识图谱中产出具备发表价值的研究选题。

三大Agent:
1. 激进派 (Hypothesis Agent) - 提出新颖冒进的研究假设
2. 保守派 (Sanity Agent) - 审查假设的可行性和自洽性
3. 刺客 (Killer Agent) - 用最严苛的审稿人视角攻击薄弱点
"""

import os
import json
import sys
from typing import Dict, List, Any, Optional
from datetime import datetime
from openai import OpenAI

# 尝试导入dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class DebateSystem:
    """多智能体辩论系统管理器"""
    
    def __init__(self, phase1_output_path: str):
        """
        初始化辩论系统
        
        Args:
            phase1_output_path: Phase 1输出文件路径
        """
        # 加载Phase 1输出
        with open(phase1_output_path, 'r', encoding='utf-8') as f:
            self.phase1_data = json.load(f)
        
        # 初始化API客户端
        api_key = os.getenv('ARK_API_KEY')
        if not api_key:
            raise ValueError("ARK_API_KEY 环境变量未设置")
        
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
            api_key=api_key
        )
        
        # 提取关键信息
        self.knowledge_graph = self.phase1_data.get('knowledge_graph', {})
        self.user_profile = self.phase1_data.get('user_profile', {})
        self.literature = self.phase1_data.get('literature', [])
        
        # 初始化三个Agent
        self.hypothesis_agent = HypothesisAgent(self.client, self.phase1_data)
        self.sanity_agent = SanityAgent(self.client, self.phase1_data)
        self.killer_agent = KillerAgent(self.client, self.phase1_data)
        
        # 辩论历史
        self.debate_history = []
        self.proposals = []
    
    def run_debate_round(self, round_num: int = 1) -> Dict[str, Any]:
        """
        执行一轮完整的辩论
        
        Args:
            round_num: 辩论轮次
            
        Returns:
            本轮辩论结果
        """
        print(f"\n{'='*80}")
        print(f"🎯 第 {round_num} 轮辩论开始")
        print(f"{'='*80}\n")
        
        # 步骤1: 激进派提出假设
        print("⏳ 激进派正在提出研究假设...")
        hypotheses = self.hypothesis_agent.propose_hypotheses()
        print(f"✅ 激进派提出了 {len(hypotheses)} 个研究假设\n")
        
        # 步骤2: 保守派审查
        print("⏳ 保守派正在审查可行性...")
        sanity_results = self.sanity_agent.review_hypotheses(hypotheses)
        print(f"✅ 保守派完成审查\n")
        
        # 步骤3: 刺客攻击
        print("⏳ 刺客正在寻找薄弱点...")
        attack_results = self.killer_agent.attack_hypotheses(hypotheses, sanity_results)
        print(f"✅ 刺客完成攻击\n")
        
        # 汇总结果
        round_result = {
            "round": round_num,
            "timestamp": datetime.now().isoformat(),
            "hypotheses": hypotheses,
            "sanity_review": sanity_results,
            "killer_attacks": attack_results,
            "surviving_hypotheses": self._filter_surviving(hypotheses, sanity_results, attack_results)
        }
        
        self.debate_history.append(round_result)
        
        return round_result
    
    def _filter_surviving(self, hypotheses: List[Dict], sanity: Dict, attacks: Dict) -> List[Dict]:
        """
        筛选出存活的假设（通过保守派审查且抵御住刺客攻击）
        
        Returns:
            存活的假设列表
        """
        surviving = []
        
        for hyp in hypotheses:
            hyp_id = hyp.get('id')
            
            # 检查保守派评分
            sanity_score = sanity.get('reviews', {}).get(hyp_id, {}).get('score', 0)
            
            # 检查刺客攻击强度
            attack_severity = attacks.get('attacks', {}).get(hyp_id, {}).get('severity', 'critical')
            
            # 存活条件: sanity >= 6 且 attack不是critical
            if sanity_score >= 6 and attack_severity != 'critical':
                surviving.append({
                    **hyp,
                    'sanity_score': sanity_score,
                    'attack_severity': attack_severity,
                    'status': 'surviving'
                })
        
        return surviving
    
    def generate_research_proposal(self, selected_hypothesis: Dict) -> Dict[str, Any]:
        """
        基于选定的假设生成完整的研究计划书
        
        Args:
            selected_hypothesis: 用户选定的研究假设
            
        Returns:
            Research Proposal
        """
        print(f"\n{'='*80}")
        print("📝 正在生成研究计划书...")
        print(f"{'='*80}\n")
        
        proposal_prompt = f"""基于以下选定的研究假设，生成一份完整的研究计划书(Research Proposal)。

选定假设：
{json.dumps(selected_hypothesis, ensure_ascii=False, indent=2)}

用户背景：
{json.dumps(self.user_profile, ensure_ascii=False, indent=2)}

知识图谱核心概念：
{json.dumps(self.knowledge_graph.get('core_concepts', []), ensure_ascii=False, indent=2)}

请生成包含以下内容的研究计划书（JSON格式）：

{{
    "title": "研究标题",
    "abstract": "研究摘要（200字以内）",
    "research_question": "核心研究问题",
    "hypothesis": "研究假设",
    "motivation": {{
        "why_important": "为什么重要",
        "gap_in_literature": "现有文献的空白",
        "potential_impact": "潜在影响"
    }},
    "methodology": {{
        "approach": "研究方法",
        "datasets": ["数据集1", "数据集2"],
        "evaluation_metrics": ["指标1", "指标2"],
        "baseline_methods": ["基线方法1", "基线方法2"]
    }},
    "expected_contributions": [
        "预期贡献1",
        "预期贡献2",
        "预期贡献3"
    ],
    "timeline": {{
        "month_1_3": "阶段1任务",
        "month_4_6": "阶段2任务",
        "month_7_9": "阶段3任务",
        "month_10_12": "阶段4任务"
    }},
    "required_resources": {{
        "computational": "算力需求",
        "data": "数据需求",
        "human": "人力需求"
    }},
    "risk_assessment": [
        {{
            "risk": "风险描述",
            "likelihood": "高/中/低",
            "mitigation": "缓解策略"
        }}
    ],
    "target_venues": [
        "目标会议/期刊1",
        "目标会议/期刊2"
    ]
}}

只返回JSON，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": proposal_prompt}],
            temperature=0.6,
        )
        
        proposal_text = response.choices[0].message.content
        
        try:
            proposal = json.loads(proposal_text)
            proposal['metadata'] = {
                'generated_at': datetime.now().isoformat(),
                'based_on_hypothesis': selected_hypothesis.get('id'),
                'debate_rounds': len(self.debate_history)
            }
            
            print("✅ 研究计划书生成完成！\n")
            return proposal
            
        except json.JSONDecodeError:
            print("⚠️  JSON解析失败")
            return {
                "raw_content": proposal_text,
                "status": "parse_failed"
            }
    
    def interactive_selection(self, surviving_hypotheses: List[Dict]) -> Optional[Dict]:
        """
        交互式选择假设
        
        Args:
            surviving_hypotheses: 存活的假设列表
            
        Returns:
            用户选择的假设，或None（重新辩论）
        """
        if not surviving_hypotheses:
            print("❌ 没有假设通过审查，需要重新辩论。")
            return None
        
        print(f"\n{'='*80}")
        print(f"📊 当前有 {len(surviving_hypotheses)} 个假设通过了辩论")
        print(f"{'='*80}\n")
        
        # 显示每个假设
        for i, hyp in enumerate(surviving_hypotheses, 1):
            print(f"\n【假设 {i}】")
            print(f"标题: {hyp.get('title', 'N/A')}")
            print(f"描述: {hyp.get('description', 'N/A')[:200]}...")
            print(f"创新性: {hyp.get('novelty', 'N/A')}/10")
            print(f"可行性评分: {hyp.get('sanity_score', 0)}/10")
            print(f"攻击强度: {hyp.get('attack_severity', 'N/A')}")
        
        print(f"\n{'='*80}")
        print("请选择一个假设继续，或选择重新辩论：")
        print("输入 1-{} 选择对应假设".format(len(surviving_hypotheses)))
        print("输入 0 重新辩论")
        print("输入 q 退出")
        print(f"{'='*80}\n")
        
        while True:
            choice = input("你的选择: ").strip()
            
            if choice == 'q':
                return 'quit'
            elif choice == '0':
                return None
            elif choice.isdigit():
                idx = int(choice) - 1
                if 0 <= idx < len(surviving_hypotheses):
                    return surviving_hypotheses[idx]
                else:
                    print(f"❌ 无效选择，请输入 0-{len(surviving_hypotheses)}")
            else:
                print("❌ 无效输入，请重新输入")


class HypothesisAgent:
    """激进派 - 提出新颖冒进的研究假设"""
    
    def __init__(self, client: OpenAI, phase1_data: Dict):
        self.client = client
        self.phase1_data = phase1_data
    
    def propose_hypotheses(self, num_hypotheses: int = 5) -> List[Dict[str, Any]]:
        """
        提出研究假设
        
        Args:
            num_hypotheses: 假设数量
            
        Returns:
            假设列表
        """
        kg = self.phase1_data.get('knowledge_graph', {})
        profile = self.phase1_data.get('user_profile', {})
        
        prompt = f"""你是一位激进的研究者，善于提出新颖、冒进但有价值的研究假设。

基于以下信息，提出{num_hypotheses}个研究假设：

用户背景：
- 专业方向：{', '.join(profile.get('specialties', []))}
- 研究兴趣：{', '.join(profile.get('research_interests', []))}

核心概念：
{json.dumps(kg.get('core_concepts', [])[:10], ensure_ascii=False, indent=2)}

研究全景：
{kg.get('research_landscape', '')}

要求：
1. 每个假设都要有创新性和突破性
2. 不要拘泥于现有方法，大胆提出新想法
3. 可以是跨领域的组合创新
4. 追求影响力和学术价值

返回JSON格式：
[
    {{
        "id": "hyp_001",
        "title": "假设标题（精炼）",
        "description": "详细描述（200-300字）",
        "novelty": 8,
        "potential_impact": "对领域的潜在影响",
        "key_innovation": "核心创新点",
        "related_work": ["相关工作1", "相关工作2"],
        "technical_challenges": ["技术挑战1", "技术挑战2"]
    }}
]

只返回JSON数组，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.8,  # 高温度，鼓励创新
        )
        
        result = response.choices[0].message.content
        
        try:
            hypotheses = json.loads(result)
            return hypotheses
        except json.JSONDecodeError:
            print("⚠️  激进派输出解析失败")
            return []


class SanityAgent:
    """保守派 - 审查假设的可行性和自洽性"""
    
    def __init__(self, client: OpenAI, phase1_data: Dict):
        self.client = client
        self.phase1_data = phase1_data
    
    def review_hypotheses(self, hypotheses: List[Dict]) -> Dict[str, Any]:
        """
        审查假设的可行性
        
        Args:
            hypotheses: 激进派提出的假设列表
            
        Returns:
            审查结果
        """
        profile = self.phase1_data.get('user_profile', {})
        
        prompt = f"""你是一位保守严谨的研究者，负责审查研究假设的可行性。

用户约束条件：
- 硬件限制：{json.dumps(profile.get('hardware_constraints', {}), ensure_ascii=False)}
- 可用数据集：{json.dumps(profile.get('datasets', []), ensure_ascii=False)}

待审查的假设：
{json.dumps(hypotheses, ensure_ascii=False, indent=2)}

请对每个假设进行审查，评估：
1. 物理/数学自洽性（是否违反基本原理）
2. 工程实现可行性（是否超出硬件算力限制）
3. 数据可获得性（所需数据是否可得）
4. 时间周期合理性（1年内能否完成）
5. 技术风险评估

返回JSON格式：
{{
    "reviews": {{
        "hyp_001": {{
            "score": 7,
            "feasibility": "可行",
            "concerns": ["顾虑1", "顾虑2"],
            "suggestions": ["建议1", "建议2"],
            "hardware_ok": true,
            "data_ok": true,
            "timeline_ok": true
        }}
    }},
    "summary": "总体评价"
}}

评分标准：0-10分，6分及以上视为通过。
只返回JSON，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,  # 低温度，追求严谨
        )
        
        result = response.choices[0].message.content
        
        try:
            review = json.loads(result)
            return review
        except json.JSONDecodeError:
            print("⚠️  保守派输出解析失败")
            return {"reviews": {}, "summary": "解析失败"}


class KillerAgent:
    """刺客 - 用最严苛的审稿人视角攻击薄弱点"""
    
    def __init__(self, client: OpenAI, phase1_data: Dict):
        self.client = client
        self.phase1_data = phase1_data
    
    def attack_hypotheses(self, hypotheses: List[Dict], sanity_review: Dict) -> Dict[str, Any]:
        """
        攻击假设的薄弱点
        
        Args:
            hypotheses: 假设列表
            sanity_review: 保守派的审查结果
            
        Returns:
            攻击结果
        """
        prompt = f"""你是一位极其严苛的审稿人，善于发现研究中的致命缺陷。

待攻击的假设：
{json.dumps(hypotheses, ensure_ascii=False, indent=2)}

保守派审查结果：
{json.dumps(sanity_review, ensure_ascii=False, indent=2)}

请对每个假设进行最严厉的批判，寻找：
1. 致命缺陷（会导致拒稿的问题）
2. 创新性不足（是否只是incremental work）
3. 实验设计漏洞
4. 对比实验不充分
5. 理论支撑薄弱
6. 可能被审稿人质疑的点

返回JSON格式：
{{
    "attacks": {{
        "hyp_001": {{
            "severity": "critical/major/minor",
            "fatal_flaws": ["致命缺陷1", "致命缺陷2"],
            "weak_points": ["薄弱点1", "薄弱点2"],
            "reviewer_questions": ["审稿人可能的问题1", "问题2"],
            "recommendation": "reject/major_revision/minor_revision/accept"
        }}
    }},
    "overall": "总体评价"
}}

只返回JSON，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        
        result = response.choices[0].message.content
        
        try:
            attacks = json.loads(result)
            return attacks
        except json.JSONDecodeError:
            print("⚠️  刺客输出解析失败")
            return {"attacks": {}, "overall": "解析失败"}


def main():
    """主函数"""
    
    print("\n" + "="*80)
    print("🎯 AutoPaper Phase 2 - 多智能体辩论与方向收敛")
    print("="*80 + "\n")
    
    # 检查API密钥
    if not os.getenv('ARK_API_KEY'):
        print("❌ 错误：未设置 ARK_API_KEY 环境变量")
        print("请运行: export ARK_API_KEY='你的API密钥'")
        return
    
    # 检查Phase 1输出文件
    phase1_file = "/Users/leave/Desktop/fc/AutoPaper/phase1_output.json"
    
    if len(sys.argv) > 1:
        phase1_file = sys.argv[1]
    
    if not os.path.exists(phase1_file):
        print(f"❌ 错误：找不到Phase 1输出文件: {phase1_file}")
        print("请先运行 Phase 1 生成知识图谱")
        return
    
    print(f"📂 加载Phase 1输出: {phase1_file}\n")
    
    # 初始化辩论系统
    debate_system = DebateSystem(phase1_file)
    
    # 多轮辩论
    max_rounds = 3
    selected_hypothesis = None
    
    for round_num in range(1, max_rounds + 1):
        # 执行辩论
        round_result = debate_system.run_debate_round(round_num)
        
        # 用户选择
        surviving = round_result['surviving_hypotheses']
        selected = debate_system.interactive_selection(surviving)
        
        if selected == 'quit':
            print("\n👋 用户退出")
            return
        elif selected is None:
            print(f"\n🔄 重新进行第 {round_num + 1} 轮辩论...\n")
            continue
        else:
            selected_hypothesis = selected
            break
    
    if not selected_hypothesis:
        print("\n❌ 达到最大辩论轮次，未选出合适的假设")
        return
    
    # 生成研究计划书
    proposal = debate_system.generate_research_proposal(selected_hypothesis)
    
    # 保存结果
    output_data = {
        "debate_history": debate_system.debate_history,
        "selected_hypothesis": selected_hypothesis,
        "research_proposal": proposal,
        "timestamp": datetime.now().isoformat(),
        "phase": 2
    }
    
    output_file = "/Users/leave/Desktop/fc/AutoPaper/phase2_output.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    # 打印结果
    print(f"\n{'='*80}")
    print("✅ Phase 2 完成！")
    print(f"{'='*80}\n")
    print(f"📊 输出文件: {output_file}\n")
    print(f"📋 研究计划书:")
    print(f"   标题: {proposal.get('title', 'N/A')}")
    print(f"   摘要: {proposal.get('abstract', 'N/A')[:100]}...")
    print(f"\n💡 下一步: 运行 Phase 3 进行实验执行")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    """
    AutoPaper Phase 2 - 多智能体辩论系统
    
    使用方式：
    
    1️⃣  使用Phase 1的输出（默认）：
        python phase2.py
    
    2️⃣  指定Phase 1输出文件：
        python phase2.py /path/to/phase1_output.json
    
    工作流程：
        1. 激进派提出3-5个研究假设
        2. 保守派审查可行性
        3. 刺客攻击薄弱点
        4. 用户选择通过的假设
        5. 生成完整的Research Proposal
    
    输出文件：
        - phase2_output.json: 完整辩论记录和研究计划书
    """
    main()
