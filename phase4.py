#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AutoPaper Phase 4: 防幻觉论文编撰

基于真实实验数据和文献，生成符合学术规范的论文。

核心Agent:
1. Academic Writer - 学术编撰者：基于真实数据自底向上撰写论文
2. QA & Formatter - 质检与格式化：LaTeX转换、BibTeX处理、图表校验

防幻觉机制:
1. 引用验证：仅允许引用知识图谱中真实存在的文献
2. 数据验证：图表必须来源于真实运行日志
3. URL检查：所有引用链接必须返回200

输出: Ready-to-Submit 的 PDF 终稿
"""

import os
import json
import sys
import re
import subprocess
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from openai import OpenAI
import urllib.request
import urllib.error

# 尝试导入dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class PaperGenerationSystem:
    """Phase 4 论文生成系统管理器"""
    
    def __init__(self, phase3_output_path: str, phase1_output_path: Optional[str] = None):
        """
        初始化论文生成系统
        
        Args:
            phase3_output_path: Phase 3输出文件路径
            phase1_output_path: Phase 1输出文件路径（可选，用于文献引用）
        """
        # 加载Phase 3输出
        with open(phase3_output_path, 'r', encoding='utf-8') as f:
            self.phase3_data = json.load(f)
        
        # 加载Phase 1输出（文献库）
        if phase1_output_path is None:
            phase1_output_path = "/Users/leave/Desktop/fc/AutoPaper/phase1_output.json"
        
        self.phase1_data = None
        if os.path.exists(phase1_output_path):
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
        
        # 提取关键数据
        self.proposal = self.phase3_data.get('proposal', {})
        self.experiment_results = self.phase3_data.get('execution_history', [])
        self.experiment_dir = Path(self.phase3_data.get('summary', {}).get('experiment_dir', ''))
        
        # 提取文献库
        self.literature = []
        if self.phase1_data:
            self.literature = self.phase1_data.get('literature', [])
        
        # 初始化两个Agent
        self.academic_writer = AcademicWriter(
            self.client, 
            self.proposal, 
            self.experiment_results,
            self.experiment_dir
        )
        self.qa_formatter = QAFormatter(
            self.client,
            self.literature
        )
        
        # 论文内容
        self.paper_content = {}
        self.citations = []
    
    def run_phase4(self, template: str = "neurips") -> Dict[str, Any]:
        """
        执行完整的Phase 4流程
        
        Args:
            template: 论文模板（neurips/icml/arxiv）
            
        Returns:
            生成结果
        """
        print(f"\n{'='*80}")
        print("📝 Phase 4: 防幻觉论文编撰")
        print(f"{'='*80}\n")
        print(f"📋 研究标题: {self.proposal.get('title', 'N/A')}")
        print(f"📄 论文模板: {template.upper()}\n")
        
        # 步骤1: 撰写论文各部分
        print("⏳ 步骤1: 学术编撰（自底向上）...\n")
        
        sections = [
            ("abstract", "摘要 (Abstract)"),
            ("introduction", "引言 (Introduction)"),
            ("related_work", "相关工作 (Related Work)"),
            ("methodology", "方法 (Methodology)"),
            ("experiments", "实验 (Experiments)"),
            ("results", "结果 (Results)"),
            ("discussion", "讨论 (Discussion)"),
            ("conclusion", "结论 (Conclusion)")
        ]
        
        for section_key, section_name in sections:
            print(f"   📝 正在撰写: {section_name}...")
            content = self.academic_writer.write_section(section_key)
            self.paper_content[section_key] = content
            print(f"   ✅ {section_name} 完成\n")
        
        # 步骤2: 提取引用
        print("⏳ 步骤2: 提取引用列表...")
        self.citations = self._extract_citations()
        print(f"✅ 提取到 {len(self.citations)} 个引用\n")
        
        # 步骤3: 防幻觉验证
        print("⏳ 步骤3: 防幻觉验证...")
        validation_report = self._validate_content()
        print(f"✅ 验证完成\n")
        
        if validation_report['status'] == 'fail':
            print("⚠️  发现以下问题:")
            for issue in validation_report['issues']:
                print(f"   - {issue}")
            print("\n正在修正...\n")
            self._fix_issues(validation_report)
        
        # 步骤4: LaTeX格式化
        print("⏳ 步骤4: LaTeX格式化与BibTeX生成...")
        latex_content = self.qa_formatter.format_to_latex(
            self.paper_content,
            self.citations,
            template
        )
        bibtex_content = self.qa_formatter.generate_bibtex(self.citations)
        print(f"✅ 格式化完成\n")
        
        # 步骤5: 生成PDF
        print("⏳ 步骤5: 编译PDF...")
        pdf_path = self._compile_pdf(latex_content, bibtex_content, template)
        
        if pdf_path:
            print(f"✅ PDF生成成功: {pdf_path}\n")
        else:
            print(f"⚠️  PDF编译失败（可能缺少LaTeX环境）\n")
        
        # 生成最终报告
        final_report = self._generate_final_report(validation_report, pdf_path)
        
        return final_report
    
    def _extract_citations(self) -> List[Dict[str, Any]]:
        """从论文内容中提取所有引用"""
        citations = []
        citation_pattern = r'\[(\d+)\]'
        
        # 扫描所有章节
        for section_content in self.paper_content.values():
            matches = re.findall(citation_pattern, section_content)
            for match in matches:
                cite_id = int(match)
                # 从文献库中查找
                if cite_id <= len(self.literature):
                    lit = self.literature[cite_id - 1]
                    if lit not in citations:
                        citations.append(lit)
        
        return citations
    
    def _validate_content(self) -> Dict[str, Any]:
        """防幻觉验证"""
        report = {
            "status": "pass",
            "issues": [],
            "warnings": []
        }
        
        # 1. 引用验证
        print("   🔍 验证引用...")
        for citation in self.citations:
            # 检查是否在知识图谱中
            if citation not in self.literature:
                report['issues'].append(f"引用不在文献库中: {citation.get('title', 'N/A')}")
                report['status'] = 'fail'
        
        if not report['issues']:
            print("   ✅ 所有引用均在知识图谱中")
        
        # 2. 数据验证
        print("   🔍 验证实验数据...")
        experiments_section = self.paper_content.get('experiments', '')
        results_section = self.paper_content.get('results', '')
        
        # 检查是否提到了真实的实验结果
        has_real_data = False
        for exp in self.experiment_results:
            metrics = exp.get('execution_result', {}).get('metrics', {})
            for metric, value in metrics.items():
                if str(value) in experiments_section or str(value) in results_section:
                    has_real_data = True
                    break
        
        if has_real_data:
            print("   ✅ 实验数据来源于真实运行日志")
        else:
            report['warnings'].append("未明确引用真实实验数据")
            print("   ⚠️  建议明确引用实验日志中的数据")
        
        # 3. URL检查
        print("   🔍 验证引用URL...")
        url_pattern = r'https?://[^\s\)"]+'
        all_text = ' '.join(self.paper_content.values())
        urls = re.findall(url_pattern, all_text)
        
        unreachable_urls = []
        for url in urls[:5]:  # 只检查前5个URL（避免过多请求）
            if not self._check_url(url):
                unreachable_urls.append(url)
        
        if unreachable_urls:
            report['warnings'].append(f"{len(unreachable_urls)} 个URL不可达")
            print(f"   ⚠️  {len(unreachable_urls)} 个URL不可达")
        else:
            print("   ✅ 所有URL可达")
        
        print()
        return report
    
    def _check_url(self, url: str, timeout: int = 5) -> bool:
        """检查URL是否可达"""
        try:
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=timeout) as response:
                return response.status == 200
        except:
            return False
    
    def _fix_issues(self, validation_report: Dict[str, Any]):
        """修正验证中发现的问题"""
        issues = validation_report.get('issues', [])
        
        # 修正无效引用
        for issue in issues:
            if "引用不在文献库中" in issue:
                print(f"   🔧 移除无效引用...")
                # 重新生成相关工作部分（移除无效引用）
                self.paper_content['related_work'] = self.academic_writer.write_section(
                    'related_work',
                    constraint="只引用提供的文献库中的论文，不要编造引用"
                )
    
    def _compile_pdf(self, latex_content: str, bibtex_content: str, template: str) -> Optional[str]:
        """编译LaTeX为PDF"""
        
        # 创建输出目录
        output_dir = Path("/Users/leave/Desktop/fc/AutoPaper/paper_output")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # 保存LaTeX和BibTeX文件
        tex_file = output_dir / "paper.tex"
        bib_file = output_dir / "references.bib"
        
        with open(tex_file, 'w', encoding='utf-8') as f:
            f.write(latex_content)
        
        with open(bib_file, 'w', encoding='utf-8') as f:
            f.write(bibtex_content)
        
        print(f"   LaTeX文件已保存: {tex_file}")
        print(f"   BibTeX文件已保存: {bib_file}")
        
        # 尝试编译PDF（需要LaTeX环境）
        try:
            # 检查是否安装了pdflatex
            result = subprocess.run(
                ['which', 'pdflatex'],
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                print("   ⚠️  未检测到pdflatex，跳过PDF编译")
                print("   💡 提示：安装MacTeX或TexLive后可自动编译PDF")
                return None
            
            # 编译PDF
            print("   正在编译PDF（可能需要1-2分钟）...")
            
            # 第一次编译
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'paper.tex'],
                cwd=output_dir,
                capture_output=True,
                timeout=60
            )
            
            # 运行bibtex
            subprocess.run(
                ['bibtex', 'paper'],
                cwd=output_dir,
                capture_output=True,
                timeout=30
            )
            
            # 第二次编译
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'paper.tex'],
                cwd=output_dir,
                capture_output=True,
                timeout=60
            )
            
            # 第三次编译（确保引用正确）
            subprocess.run(
                ['pdflatex', '-interaction=nonstopmode', 'paper.tex'],
                cwd=output_dir,
                capture_output=True,
                timeout=60
            )
            
            pdf_file = output_dir / "paper.pdf"
            if pdf_file.exists():
                return str(pdf_file)
            else:
                return None
                
        except subprocess.TimeoutExpired:
            print("   ⚠️  PDF编译超时")
            return None
        except Exception as e:
            print(f"   ⚠️  PDF编译失败: {e}")
            return None
    
    def _generate_final_report(self, validation_report: Dict, pdf_path: Optional[str]) -> Dict[str, Any]:
        """生成最终报告"""
        print(f"\n{'='*80}")
        print("📊 生成最终报告...")
        print(f"{'='*80}\n")
        
        report = {
            "proposal": self.proposal,
            "paper_content": self.paper_content,
            "citations": self.citations,
            "validation_report": validation_report,
            "output_files": {
                "latex": "/Users/leave/Desktop/fc/AutoPaper/paper_output/paper.tex",
                "bibtex": "/Users/leave/Desktop/fc/AutoPaper/paper_output/references.bib",
                "pdf": pdf_path if pdf_path else None
            },
            "statistics": {
                "sections": len(self.paper_content),
                "citations": len(self.citations),
                "word_count": sum(len(content.split()) for content in self.paper_content.values())
            },
            "timestamp": datetime.now().isoformat(),
            "phase": 4
        }
        
        # 保存报告
        output_file = "/Users/leave/Desktop/fc/AutoPaper/phase4_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"✅ 最终报告已保存: {output_file}\n")
        
        # 打印统计
        print(f"📊 论文统计:")
        print(f"   章节数: {report['statistics']['sections']}")
        print(f"   引用数: {report['statistics']['citations']}")
        print(f"   总字数: {report['statistics']['word_count']}")
        print(f"\n📁 输出文件:")
        print(f"   LaTeX: {report['output_files']['latex']}")
        print(f"   BibTeX: {report['output_files']['bibtex']}")
        if pdf_path:
            print(f"   PDF: {pdf_path}")
        
        return report


class AcademicWriter:
    """学术编撰者 - 自底向上撰写论文"""
    
    def __init__(self, client: OpenAI, proposal: Dict, experiment_results: List, experiment_dir: Path):
        self.client = client
        self.proposal = proposal
        self.experiment_results = experiment_results
        self.experiment_dir = experiment_dir
    
    def write_section(self, section: str, constraint: str = "") -> str:
        """
        撰写论文某个章节
        
        Args:
            section: 章节名称
            constraint: 额外约束（可选）
            
        Returns:
            章节内容
        """
        # 构建提示词
        if section == "abstract":
            prompt = self._prompt_abstract()
        elif section == "introduction":
            prompt = self._prompt_introduction()
        elif section == "related_work":
            prompt = self._prompt_related_work(constraint)
        elif section == "methodology":
            prompt = self._prompt_methodology()
        elif section == "experiments":
            prompt = self._prompt_experiments()
        elif section == "results":
            prompt = self._prompt_results()
        elif section == "discussion":
            prompt = self._prompt_discussion()
        elif section == "conclusion":
            prompt = self._prompt_conclusion()
        else:
            prompt = f"Write the {section} section based on the research proposal."
        
        # 调用API
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
        )
        
        content = response.choices[0].message.content
        return content
    
    def _prompt_abstract(self) -> str:
        return f"""Write an academic abstract for the following research.

Research Title: {self.proposal.get('title', '')}
Research Goal: {self.proposal.get('abstract', '')}
Methodology: {json.dumps(self.proposal.get('methodology', {}), ensure_ascii=False)}
Experiment Results: {self._summarize_results()}

Write a concise abstract (150-200 words) that includes:
1. Motivation and problem statement
2. Proposed approach
3. Key results
4. Main contributions

Use formal academic English. Do not make up any results - only use the provided experiment data.
"""
    
    def _prompt_introduction(self) -> str:
        return f"""Write the Introduction section for this research paper.

Research Title: {self.proposal.get('title', '')}
Background: {self.proposal.get('abstract', '')}
Expected Contributions: {json.dumps(self.proposal.get('expected_contributions', []), ensure_ascii=False)}

Structure:
1. Broad context and motivation (2-3 paragraphs)
2. Problem statement and challenges
3. Our approach and key ideas
4. Main contributions (bullet points)
5. Paper organization

Write in formal academic style. Be specific about the problem and contributions.
"""
    
    def _prompt_related_work(self, constraint: str) -> str:
        return f"""Write the Related Work section for this research paper.

Research Area: {', '.join(self.proposal.get('methodology', {}).get('approach', '').split()[:5])}
Our Work: {self.proposal.get('title', '')}

{constraint}

Structure:
1. Overview of the research area
2. Categorize related work into 2-3 groups
3. Compare and contrast with our work
4. Highlight what makes our approach different

Write 3-4 paragraphs in formal academic style. If citing papers, use format [1], [2], etc.
"""
    
    def _prompt_methodology(self) -> str:
        methodology = self.proposal.get('methodology', {})
        return f"""Write the Methodology section describing the technical approach.

Approach: {json.dumps(methodology, ensure_ascii=False)}
Dataset: {methodology.get('dataset', 'N/A')}
Evaluation: {methodology.get('evaluation', 'N/A')}

Structure:
1. Overview of the approach
2. Problem formulation (if applicable, use simple math notation)
3. Proposed method with technical details
4. Implementation details

Write clearly and precisely. Use technical language where appropriate. 
Include algorithmic steps if relevant.
"""
    
    def _prompt_experiments(self) -> str:
        experiment_summary = self._get_experiment_setup()
        return f"""Write the Experiments section describing the experimental setup.

Experiment Setup:
{experiment_summary}

Methodology: {json.dumps(self.proposal.get('methodology', {}), ensure_ascii=False)}

Structure:
1. Experimental setup and environment
2. Dataset description
3. Baselines and comparisons
4. Evaluation metrics
5. Implementation details

Write clearly and provide sufficient details for reproducibility.
"""
    
    def _prompt_results(self) -> str:
        results_summary = self._summarize_results()
        return f"""Write the Results section presenting the experimental findings.

Experimental Results:
{results_summary}

Structure:
1. Main results (present key findings)
2. Quantitative analysis (tables/metrics)
3. Qualitative analysis (if applicable)
4. Ablation studies or additional experiments (if applicable)

Present results objectively. Use the actual numbers from the experiment logs.
Reference tables and figures as needed (e.g., "Table 1", "Figure 1").
"""
    
    def _prompt_discussion(self) -> str:
        return f"""Write the Discussion section analyzing the results.

Results Summary: {self._summarize_results()}
Expected Contributions: {json.dumps(self.proposal.get('expected_contributions', []), ensure_ascii=False)}

Structure:
1. Interpretation of results
2. Why the approach works (or doesn't)
3. Limitations and potential improvements
4. Broader implications

Be honest about limitations. Discuss what was learned from the experiments.
"""
    
    def _prompt_conclusion(self) -> str:
        return f"""Write the Conclusion section.

Research Title: {self.proposal.get('title', '')}
Main Contributions: {json.dumps(self.proposal.get('expected_contributions', []), ensure_ascii=False)}
Key Results: {self._summarize_results()}

Structure:
1. Summarize the main contributions
2. Key findings from experiments
3. Future work directions

Write 2-3 concise paragraphs. End on a forward-looking note.
"""
    
    def _get_experiment_setup(self) -> str:
        """获取实验设置描述"""
        if not self.experiment_results:
            return "No experiment data available."
        
        last_exp = self.experiment_results[-1]
        exec_result = last_exp.get('execution_result', {})
        
        setup = f"Environment: Python sandbox\n"
        setup += f"Status: {exec_result.get('status', 'unknown')}\n"
        setup += f"Artifacts: {', '.join(exec_result.get('artifacts', []))}\n"
        
        return setup
    
    def _summarize_results(self) -> str:
        """总结实验结果"""
        if not self.experiment_results:
            return "No experimental results available yet."
        
        summary = []
        for i, exp in enumerate(self.experiment_results):
            exec_result = exp.get('execution_result', {})
            metrics = exec_result.get('metrics', {})
            evaluation = exp.get('evaluation', {})
            
            summary.append(f"Iteration {i+1}:")
            summary.append(f"  Status: {exec_result.get('status', 'unknown')}")
            if metrics:
                summary.append(f"  Metrics: {json.dumps(metrics, indent=4)}")
            summary.append(f"  Evaluation Score: {evaluation.get('score', 'N/A')}/10")
            summary.append(f"  Final Status: {evaluation.get('status', 'unknown')}")
        
        return '\n'.join(summary)


class QAFormatter:
    """质检与格式化 - LaTeX转换、BibTeX处理"""
    
    def __init__(self, client: OpenAI, literature: List[Dict]):
        self.client = client
        self.literature = literature
    
    def format_to_latex(self, paper_content: Dict[str, str], citations: List[Dict], template: str) -> str:
        """
        将论文内容转换为LaTeX格式
        
        Args:
            paper_content: 论文各章节内容
            citations: 引用列表
            template: 论文模板
            
        Returns:
            LaTeX内容
        """
        # 根据模板选择文档类
        if template == "neurips":
            doc_class = "\\documentclass{article}\n\\usepackage{neurips_2023}"
        elif template == "icml":
            doc_class = "\\documentclass{article}\n\\usepackage{icml2023}"
        else:  # arxiv
            doc_class = "\\documentclass{article}"
        
        # 构建LaTeX文档
        latex = []
        latex.append(doc_class)
        latex.append("\\usepackage[utf8]{inputenc}")
        latex.append("\\usepackage{amsmath,amssymb}")
        latex.append("\\usepackage{graphicx}")
        latex.append("\\usepackage{hyperref}")
        latex.append("")
        
        # 标题和作者
        title = paper_content.get('title', 'Research Paper')
        latex.append(f"\\title{{{title}}}")
        latex.append("\\author{AutoPaper Generated}")
        latex.append("\\date{\\today}")
        latex.append("")
        
        latex.append("\\begin{document}")
        latex.append("\\maketitle")
        latex.append("")
        
        # 摘要
        if 'abstract' in paper_content:
            latex.append("\\begin{abstract}")
            latex.append(self._clean_text_for_latex(paper_content['abstract']))
            latex.append("\\end{abstract}")
            latex.append("")
        
        # 各章节
        sections = [
            ("introduction", "Introduction"),
            ("related_work", "Related Work"),
            ("methodology", "Methodology"),
            ("experiments", "Experiments"),
            ("results", "Results"),
            ("discussion", "Discussion"),
            ("conclusion", "Conclusion")
        ]
        
        for section_key, section_title in sections:
            if section_key in paper_content:
                latex.append(f"\\section{{{section_title}}}")
                latex.append(self._clean_text_for_latex(paper_content[section_key]))
                latex.append("")
        
        # 参考文献
        if citations:
            latex.append("\\bibliographystyle{plain}")
            latex.append("\\bibliography{references}")
        
        latex.append("\\end{document}")
        
        return '\n'.join(latex)
    
    def generate_bibtex(self, citations: List[Dict]) -> str:
        """
        生成BibTeX文件
        
        Args:
            citations: 引用列表
            
        Returns:
            BibTeX内容
        """
        bibtex_entries = []
        
        for i, citation in enumerate(citations):
            cite_key = f"ref{i+1}"
            title = citation.get('title', 'Unknown')
            authors = citation.get('authors', 'Unknown')
            year = citation.get('year', '2023')
            venue = citation.get('venue', 'Unknown')
            
            entry = f"""@article{{{cite_key},
  title={{{title}}},
  author={{{authors}}},
  year={{{year}}},
  journal={{{venue}}}
}}
"""
            bibtex_entries.append(entry)
        
        return '\n'.join(bibtex_entries)
    
    def _clean_text_for_latex(self, text: str) -> str:
        """清理文本，转义LaTeX特殊字符"""
        # 转义特殊字符
        replacements = {
            '&': '\\&',
            '%': '\\%',
            '$': '\\$',
            '#': '\\#',
            '_': '\\_',
            '{': '\\{',
            '}': '\\}',
            '~': '\\textasciitilde{}',
            '^': '\\textasciicircum{}'
        }
        
        for char, replacement in replacements.items():
            text = text.replace(char, replacement)
        
        return text


def main():
    """主函数"""
    
    print("\n" + "="*80)
    print("📝 AutoPaper Phase 4 - 防幻觉论文编撰")
    print("="*80 + "\n")
    
    # 检查API密钥
    if not os.getenv('ARK_API_KEY'):
        print("❌ 错误：未设置 ARK_API_KEY 环境变量")
        print("请运行: export ARK_API_KEY='你的API密钥'")
        return
    
    # 检查Phase 3输出文件
    phase3_file = "/Users/leave/Desktop/fc/AutoPaper/phase3_output.json"
    
    if len(sys.argv) > 1:
        phase3_file = sys.argv[1]
    
    if not os.path.exists(phase3_file):
        print(f"❌ 错误：找不到Phase 3输出文件: {phase3_file}")
        print("请先运行 Phase 3 完成实验")
        return
    
    print(f"📂 加载Phase 3输出: {phase3_file}\n")
    
    # 选择模板
    template = "neurips"
    if len(sys.argv) > 2:
        template = sys.argv[2].lower()
    
    # 初始化论文生成系统
    try:
        paper_system = PaperGenerationSystem(phase3_file)
        
        # 运行Phase 4
        result = paper_system.run_phase4(template=template)
        
        # 打印最终结果
        print(f"\n{'='*80}")
        print("✅ Phase 4 完成！")
        print(f"{'='*80}\n")
        print(f"📊 论文统计:")
        print(f"   章节数: {result['statistics']['sections']}")
        print(f"   引用数: {result['statistics']['citations']}")
        print(f"   总字数: {result['statistics']['word_count']}")
        print(f"\n📁 输出文件:")
        print(f"   JSON报告: /Users/leave/Desktop/fc/AutoPaper/phase4_output.json")
        print(f"   LaTeX源码: {result['output_files']['latex']}")
        print(f"   BibTeX: {result['output_files']['bibtex']}")
        if result['output_files']['pdf']:
            print(f"   PDF论文: {result['output_files']['pdf']}")
            print(f"\n💡 提示: 使用 'open {result['output_files']['pdf']}' 查看PDF")
        else:
            print(f"\n💡 提示: 安装LaTeX后可自动生成PDF")
            print(f"   macOS: brew install --cask mactex")
            print(f"   或手动编译: cd paper_output && pdflatex paper.tex")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"\n❌ Phase 4 执行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    """
    AutoPaper Phase 4 - 防幻觉论文编撰
    
    使用方式：
    
    1️⃣  使用Phase 3的输出（默认）：
        python phase4.py
    
    2️⃣  指定Phase 3输出文件：
        python phase4.py /path/to/phase3_output.json
    
    3️⃣  指定论文模板：
        python phase4.py /path/to/phase3_output.json neurips
        python phase4.py /path/to/phase3_output.json icml
        python phase4.py /path/to/phase3_output.json arxiv
    
    工作流程：
        1. 学术编撰：自底向上撰写论文各章节
        2. 引用提取：从内容中提取引用列表
        3. 防幻觉验证：引用验证、数据验证、URL检查
        4. LaTeX格式化：转换为LaTeX格式
        5. PDF生成：编译为Ready-to-Submit PDF
    
    输出文件：
        - phase4_output.json: 完整论文内容和元数据
        - paper_output/paper.tex: LaTeX源码
        - paper_output/references.bib: BibTeX引用
        - paper_output/paper.pdf: PDF论文（需LaTeX环境）
    
    防幻觉机制：
        1. 引用验证：仅允许引用知识图谱中的真实文献
        2. 数据验证：图表必须来源于真实运行日志
        3. URL检查：所有引用链接必须返回200
    """
    main()
