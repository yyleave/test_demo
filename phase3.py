#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
AutoPaper Phase 3: 沙盒执行与评估闭环

在严格隔离的沙盒环境中执行实验，通过客观评估闭环确保质量。

核心Agent:
1. Task Decomposer - 任务分解器：将研究方向拆解为DAG形式的实验步骤
2. Code Generator - 代码生成器：编写实验代码，配置运行环境
3. Sentinel - 哨兵：监控数值异常（NaN/Inf），熔断并触发Debug
4. Evaluator - 评估器：读取真实探针数据，客观评估结果

FARS机制：所有运行日志强制Commit入库，过程可回溯、可审计
"""

import os
import json
import sys
import subprocess
import tempfile
import shutil
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
from pathlib import Path
from openai import OpenAI

# 尝试导入dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class ExecutionSystem:
    """Phase 3 执行系统管理器"""
    
    def __init__(self, phase2_output_path: str, workspace_dir: Optional[str] = None):
        """
        初始化执行系统
        
        Args:
            phase2_output_path: Phase 2输出文件路径
            workspace_dir: 工作目录（用于代码和日志）
        """
        # 加载Phase 2输出
        with open(phase2_output_path, 'r', encoding='utf-8') as f:
            self.phase2_data = json.load(f)
        
        # 初始化API客户端
        api_key = os.getenv('ARK_API_KEY')
        if not api_key:
            raise ValueError("ARK_API_KEY 环境变量未设置")
        
        self.client = OpenAI(
            base_url="https://ark.cn-beijing.volces.com/api/coding/v3",
            api_key=api_key
        )
        
        # 提取Research Proposal（上下文硬重置）
        self.proposal = self.phase2_data.get('research_proposal', {})
        
        # 设置工作目录
        if workspace_dir is None:
            workspace_dir = "/Users/leave/Desktop/fc/AutoPaper/experiments"
        self.workspace = Path(workspace_dir)
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # 创建实验子目录
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exp_name = self.proposal.get('title', 'experiment').replace(' ', '_')[:30]
        self.experiment_dir = self.workspace / f"{exp_name}_{timestamp}"
        self.experiment_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化Git仓库（FARS机制）
        self._init_git_repo()
        
        # 初始化四个Agent
        self.task_decomposer = TaskDecomposer(self.client, self.proposal)
        self.code_generator = CodeGenerator(self.client, self.proposal, self.experiment_dir)
        self.sentinel = Sentinel()
        self.evaluator = Evaluator(self.client, self.proposal)
        
        # 执行历史
        self.execution_history = []
        self.task_dag = None
    
    def _init_git_repo(self):
        """初始化Git仓库（FARS机制）"""
        try:
            subprocess.run(
                ['git', 'init'],
                cwd=self.experiment_dir,
                check=True,
                capture_output=True
            )
            
            # 配置Git
            subprocess.run(
                ['git', 'config', 'user.name', 'AutoPaper'],
                cwd=self.experiment_dir,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ['git', 'config', 'user.email', 'autopaper@example.com'],
                cwd=self.experiment_dir,
                check=True,
                capture_output=True
            )
            
            print(f"✅ Git仓库初始化完成: {self.experiment_dir}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git初始化失败: {e}")
    
    def _git_commit(self, message: str, files: Optional[List[str]] = None):
        """Git提交（FARS机制）"""
        try:
            # 添加文件
            if files:
                for f in files:
                    subprocess.run(
                        ['git', 'add', f],
                        cwd=self.experiment_dir,
                        check=True,
                        capture_output=True
                    )
            else:
                subprocess.run(
                    ['git', 'add', '.'],
                    cwd=self.experiment_dir,
                    check=True,
                    capture_output=True
                )
            
            # 提交
            subprocess.run(
                ['git', 'commit', '-m', message],
                cwd=self.experiment_dir,
                check=True,
                capture_output=True
            )
            print(f"✅ Git提交成功: {message}")
        except subprocess.CalledProcessError as e:
            print(f"⚠️  Git提交失败: {e}")
    
    def run_phase3(self, max_iterations: int = 5) -> Dict[str, Any]:
        """
        执行完整的Phase 3流程
        
        Args:
            max_iterations: 最大迭代次数
            
        Returns:
            执行结果
        """
        print(f"\n{'='*80}")
        print("🚀 Phase 3: 沙盒执行与评估闭环")
        print(f"{'='*80}\n")
        print(f"📂 实验目录: {self.experiment_dir}")
        print(f"📋 研究标题: {self.proposal.get('title', 'N/A')}\n")
        
        # 步骤1: 任务分解
        print("⏳ 步骤1: 任务分解（DAG）...")
        self.task_dag = self.task_decomposer.decompose()
        self._git_commit("Phase3: Task decomposition", ["task_dag.json"])
        print(f"✅ 任务分解完成，共 {len(self.task_dag.get('tasks', []))} 个任务\n")
        
        # 保存任务DAG
        with open(self.experiment_dir / "task_dag.json", 'w', encoding='utf-8') as f:
            json.dump(self.task_dag, f, ensure_ascii=False, indent=2)
        
        # 迭代执行
        for iteration in range(1, max_iterations + 1):
            print(f"\n{'='*80}")
            print(f"🔄 迭代 {iteration}/{max_iterations}")
            print(f"{'='*80}\n")
            
            # 步骤2: 代码生成
            print("⏳ 步骤2: 代码生成...")
            code_files = self.code_generator.generate_code(self.task_dag, iteration)
            self._git_commit(f"Iteration {iteration}: Code generation", list(code_files.keys()))
            print(f"✅ 代码生成完成，共 {len(code_files)} 个文件\n")
            
            # 步骤3: 沙盒执行
            print("⏳ 步骤3: 沙盒执行...")
            execution_result = self._execute_in_sandbox(code_files)
            
            # 保存执行日志
            log_file = f"execution_log_iter{iteration}.json"
            with open(self.experiment_dir / log_file, 'w', encoding='utf-8') as f:
                json.dump(execution_result, f, ensure_ascii=False, indent=2)
            self._git_commit(f"Iteration {iteration}: Execution logs", [log_file])
            
            # 步骤4: 哨兵监控
            print("⏳ 步骤4: 哨兵监控...")
            sentinel_report = self.sentinel.monitor(execution_result)
            
            # 步骤5: 评估器校验
            print("⏳ 步骤5: 评估器校验...")
            evaluation = self.evaluator.evaluate(execution_result, sentinel_report)
            
            # 保存评估结果
            eval_file = f"evaluation_iter{iteration}.json"
            with open(self.experiment_dir / eval_file, 'w', encoding='utf-8') as f:
                json.dump(evaluation, f, ensure_ascii=False, indent=2)
            self._git_commit(f"Iteration {iteration}: Evaluation", [eval_file])
            
            # 记录历史
            self.execution_history.append({
                "iteration": iteration,
                "execution_result": execution_result,
                "sentinel_report": sentinel_report,
                "evaluation": evaluation,
                "timestamp": datetime.now().isoformat()
            })
            
            # 判断是否通过
            if evaluation.get('status') == 'pass':
                print(f"\n✅ 实验通过评估！\n")
                break
            elif evaluation.get('status') == 'fail':
                print(f"\n⚠️  实验未通过，需要修正\n")
                print(f"问题: {evaluation.get('issues', [])}")
                print(f"建议: {evaluation.get('suggestions', [])}\n")
                
                if iteration < max_iterations:
                    print(f"准备进行第 {iteration + 1} 轮迭代...\n")
                    # 更新代码生成器的上下文
                    self.code_generator.update_context(evaluation)
                else:
                    print(f"⚠️  达到最大迭代次数 ({max_iterations})，停止执行\n")
        
        # 生成最终报告
        final_report = self._generate_final_report()
        
        return final_report
    
    def _execute_in_sandbox(self, code_files: Dict[str, str]) -> Dict[str, Any]:
        """
        在沙盒环境中执行代码
        
        Args:
            code_files: {文件名: 代码内容}
            
        Returns:
            执行结果
        """
        execution_result = {
            "status": "unknown",
            "stdout": "",
            "stderr": "",
            "return_code": None,
            "metrics": {},
            "artifacts": []
        }
        
        try:
            # 找到主执行文件
            main_file = None
            for filename in code_files.keys():
                if filename in ['main.py', 'train.py', 'experiment.py']:
                    main_file = filename
                    break
            
            if not main_file:
                main_file = list(code_files.keys())[0]
            
            # 执行
            print(f"   执行文件: {main_file}")
            result = subprocess.run(
                ['python', main_file],
                cwd=self.experiment_dir,
                capture_output=True,
                text=True,
                timeout=300  # 5分钟超时
            )
            
            execution_result['status'] = 'success' if result.returncode == 0 else 'error'
            execution_result['stdout'] = result.stdout
            execution_result['stderr'] = result.stderr
            execution_result['return_code'] = result.returncode
            
            # 解析输出中的指标
            execution_result['metrics'] = self._parse_metrics(result.stdout)
            
            # 查找生成的文件
            execution_result['artifacts'] = self._find_artifacts()
            
            if result.returncode == 0:
                print(f"   ✅ 执行成功\n")
            else:
                print(f"   ❌ 执行失败 (返回码: {result.returncode})\n")
                if result.stderr:
                    print(f"   错误信息: {result.stderr[:200]}\n")
            
        except subprocess.TimeoutExpired:
            execution_result['status'] = 'timeout'
            execution_result['stderr'] = 'Execution timeout after 300 seconds'
            print(f"   ⏱️  执行超时\n")
        except Exception as e:
            execution_result['status'] = 'error'
            execution_result['stderr'] = str(e)
            print(f"   ❌ 执行异常: {e}\n")
        
        return execution_result
    
    def _parse_metrics(self, output: str) -> Dict[str, Any]:
        """从输出中解析指标"""
        metrics = {}
        
        # 简单的指标解析（查找 key: value 格式）
        lines = output.split('\n')
        for line in lines:
            if ':' in line:
                parts = line.split(':', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    # 尝试转换为数字
                    try:
                        if '.' in value:
                            metrics[key] = float(value)
                        else:
                            metrics[key] = int(value)
                    except ValueError:
                        metrics[key] = value
        
        return metrics
    
    def _find_artifacts(self) -> List[str]:
        """查找生成的文件"""
        artifacts = []
        
        # 查找常见的输出文件
        patterns = ['*.png', '*.jpg', '*.pdf', '*.csv', '*.json', '*.txt', '*.log', '*.pt', '*.pth']
        
        for pattern in patterns:
            for file in self.experiment_dir.glob(pattern):
                if file.is_file() and file.name not in ['task_dag.json']:
                    artifacts.append(file.name)
        
        return artifacts
    
    def _generate_final_report(self) -> Dict[str, Any]:
        """生成最终实验报告"""
        print(f"\n{'='*80}")
        print("📊 生成最终实验报告...")
        print(f"{'='*80}\n")
        
        report = {
            "proposal": self.proposal,
            "task_dag": self.task_dag,
            "execution_history": self.execution_history,
            "summary": {
                "total_iterations": len(self.execution_history),
                "final_status": self.execution_history[-1]['evaluation'].get('status') if self.execution_history else 'unknown',
                "experiment_dir": str(self.experiment_dir)
            },
            "timestamp": datetime.now().isoformat(),
            "phase": 3
        }
        
        # 保存报告
        output_file = "/Users/leave/Desktop/fc/AutoPaper/phase3_output.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        # 也保存到实验目录
        with open(self.experiment_dir / "final_report.json", 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        self._git_commit("Phase3: Final report", ["final_report.json"])
        
        print(f"✅ 最终报告已保存")
        print(f"   全局输出: {output_file}")
        print(f"   实验目录: {self.experiment_dir / 'final_report.json'}\n")
        
        # 打印总结
        print(f"📊 实验总结:")
        print(f"   总迭代次数: {report['summary']['total_iterations']}")
        print(f"   最终状态: {report['summary']['final_status']}")
        print(f"   实验目录: {report['summary']['experiment_dir']}")
        
        return report


class TaskDecomposer:
    """任务分解器 - 将研究方向拆解为DAG形式的实验步骤"""
    
    def __init__(self, client: OpenAI, proposal: Dict):
        self.client = client
        self.proposal = proposal
    
    def decompose(self) -> Dict[str, Any]:
        """
        将Research Proposal分解为DAG任务图
        
        Returns:
            任务DAG
        """
        prompt = f"""基于以下Research Proposal，将研究分解为具体的实验任务（DAG形式）。

Research Proposal:
标题: {self.proposal.get('title', 'N/A')}
研究方法: {json.dumps(self.proposal.get('methodology', {}), ensure_ascii=False)}
时间规划: {json.dumps(self.proposal.get('timeline', {}), ensure_ascii=False)}

请分解为具体的可执行任务，返回JSON格式：

{{
    "tasks": [
        {{
            "id": "task_001",
            "name": "任务名称",
            "description": "详细描述",
            "type": "data_preparation/model_implementation/training/evaluation",
            "dependencies": ["task_000"],
            "estimated_time": "1 hour",
            "outputs": ["output_file.json"],
            "code_template": "简单的代码模板或伪代码"
        }}
    ],
    "dag": {{
        "nodes": ["task_001", "task_002"],
        "edges": [["task_001", "task_002"]]
    }}
}}

注意：
1. 任务要具体可执行
2. 依赖关系要清晰（形成DAG）
3. 每个任务应该在1-2小时内完成
4. 提供简单的代码模板

只返回JSON，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        
        result = response.choices[0].message.content
        
        try:
            task_dag = json.loads(result)
            return task_dag
        except json.JSONDecodeError:
            print("⚠️  任务分解JSON解析失败")
            return {
                "tasks": [],
                "dag": {"nodes": [], "edges": []},
                "raw_content": result
            }


class CodeGenerator:
    """代码生成器 - 编写实验代码，配置运行环境"""
    
    def __init__(self, client: OpenAI, proposal: Dict, experiment_dir: Path):
        self.client = client
        self.proposal = proposal
        self.experiment_dir = experiment_dir
        self.context = []  # 存储之前的错误和建议
    
    def update_context(self, evaluation: Dict):
        """更新上下文（用于迭代改进）"""
        self.context.append({
            "issues": evaluation.get('issues', []),
            "suggestions": evaluation.get('suggestions', [])
        })
    
    def generate_code(self, task_dag: Dict, iteration: int = 1) -> Dict[str, str]:
        """
        生成实验代码
        
        Args:
            task_dag: 任务DAG
            iteration: 当前迭代次数
            
        Returns:
            {文件名: 代码内容}
        """
        # 构建上下文信息
        context_info = ""
        if self.context:
            context_info = f"\n之前迭代的问题和建议:\n{json.dumps(self.context[-1], ensure_ascii=False, indent=2)}\n"
        
        prompt = f"""基于以下任务DAG，生成完整的实验代码（第{iteration}轮迭代）。

任务DAG:
{json.dumps(task_dag, ensure_ascii=False, indent=2)}

Research Proposal:
{json.dumps(self.proposal, ensure_ascii=False, indent=2)}

{context_info}

请生成以下文件的代码：
1. main.py - 主执行文件
2. model.py - 模型定义（如需要）
3. data.py - 数据处理（如需要）
4. utils.py - 工具函数（如需要）
5. requirements.txt - 依赖包

要求：
1. 代码要完整可运行
2. 包含必要的错误处理
3. 输出关键指标（loss, accuracy等）
4. 生成可视化结果（保存为PNG）
5. 使用简单的数据集（如MNIST）进行演示
6. 添加详细的注释

返回JSON格式：
{{
    "files": {{
        "main.py": "代码内容",
        "model.py": "代码内容",
        ...
    }}
}}

只返回JSON，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.6,
        )
        
        result = response.choices[0].message.content
        
        try:
            code_data = json.loads(result)
            code_files = code_data.get('files', {})
            
            # 写入文件
            for filename, content in code_files.items():
                file_path = self.experiment_dir / filename
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
            
            return code_files
            
        except json.JSONDecodeError:
            print("⚠️  代码生成JSON解析失败")
            # 尝试提取代码块
            return self._extract_code_blocks(result)
    
    def _extract_code_blocks(self, text: str) -> Dict[str, str]:
        """从文本中提取代码块"""
        code_files = {}
        
        # 简单的代码块提取
        lines = text.split('\n')
        current_file = None
        current_code = []
        
        for line in lines:
            if line.startswith('# ') and '.py' in line:
                # 保存之前的文件
                if current_file and current_code:
                    code_files[current_file] = '\n'.join(current_code)
                
                # 开始新文件
                current_file = line.split()[-1]
                current_code = []
            elif current_file:
                current_code.append(line)
        
        # 保存最后一个文件
        if current_file and current_code:
            code_files[current_file] = '\n'.join(current_code)
        
        # 写入文件
        for filename, content in code_files.items():
            file_path = self.experiment_dir / filename
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        
        return code_files


class Sentinel:
    """哨兵 - 监控数值异常，熔断并触发Debug"""
    
    def monitor(self, execution_result: Dict) -> Dict[str, Any]:
        """
        监控执行结果，检测异常
        
        Args:
            execution_result: 执行结果
            
        Returns:
            监控报告
        """
        report = {
            "status": "normal",
            "anomalies": [],
            "warnings": []
        }
        
        # 检查执行状态
        if execution_result['status'] == 'error':
            report['status'] = 'error'
            report['anomalies'].append({
                "type": "execution_error",
                "message": execution_result.get('stderr', 'Unknown error'),
                "severity": "critical"
            })
        elif execution_result['status'] == 'timeout':
            report['status'] = 'error'
            report['anomalies'].append({
                "type": "timeout",
                "message": "Execution timeout",
                "severity": "critical"
            })
        
        # 检查指标中的NaN/Inf
        metrics = execution_result.get('metrics', {})
        for key, value in metrics.items():
            if isinstance(value, (int, float)):
                if value != value:  # NaN检测
                    report['anomalies'].append({
                        "type": "nan_detected",
                        "metric": key,
                        "severity": "critical"
                    })
                    report['status'] = 'error'
                elif abs(value) == float('inf'):
                    report['anomalies'].append({
                        "type": "inf_detected",
                        "metric": key,
                        "severity": "critical"
                    })
                    report['status'] = 'error'
                elif key.lower().startswith('loss') and value > 1e6:
                    report['warnings'].append({
                        "type": "loss_explosion",
                        "metric": key,
                        "value": value,
                        "severity": "major"
                    })
        
        # 检查stderr中的警告
        stderr = execution_result.get('stderr', '')
        if 'warning' in stderr.lower():
            report['warnings'].append({
                "type": "runtime_warning",
                "message": stderr[:200],
                "severity": "minor"
            })
        
        # 打印报告
        if report['anomalies']:
            print(f"   ⚠️  发现 {len(report['anomalies'])} 个异常")
            for anomaly in report['anomalies']:
                print(f"      - {anomaly['type']}: {anomaly.get('message', anomaly.get('metric', 'N/A'))}")
        else:
            print(f"   ✅ 未发现异常")
        
        if report['warnings']:
            print(f"   ⚠️  {len(report['warnings'])} 个警告")
        
        print()
        
        return report


class Evaluator:
    """评估器 - 读取真实探针数据，客观评估结果"""
    
    def __init__(self, client: OpenAI, proposal: Dict):
        self.client = client
        self.proposal = proposal
    
    def evaluate(self, execution_result: Dict, sentinel_report: Dict) -> Dict[str, Any]:
        """
        评估实验结果
        
        Args:
            execution_result: 执行结果
            sentinel_report: 哨兵报告
            
        Returns:
            评估结果
        """
        # 如果哨兵发现严重异常，直接失败
        if sentinel_report['status'] == 'error':
            return {
                "status": "fail",
                "score": 0,
                "issues": [a['message'] if 'message' in a else a['type'] for a in sentinel_report['anomalies']],
                "suggestions": ["修复代码中的错误", "检查数值稳定性"]
            }
        
        # 使用AI评估结果质量
        prompt = f"""评估以下实验结果的质量。

Research Proposal目标:
{json.dumps(self.proposal.get('expected_contributions', []), ensure_ascii=False)}

执行结果:
状态: {execution_result['status']}
指标: {json.dumps(execution_result.get('metrics', {}), ensure_ascii=False)}
生成文件: {execution_result.get('artifacts', [])}

哨兵报告:
{json.dumps(sentinel_report, ensure_ascii=False)}

请评估实验是否达到预期目标，返回JSON格式：

{{
    "status": "pass/fail/partial",
    "score": 7.5,
    "issues": ["问题1", "问题2"],
    "suggestions": ["建议1", "建议2"],
    "strengths": ["优点1", "优点2"],
    "next_steps": ["下一步1", "下一步2"]
}}

评分标准：
- 8-10分: 优秀，达到预期目标
- 6-8分: 良好，基本达标
- 4-6分: 及格，需要改进
- 0-4分: 不及格，需要重做

只返回JSON，不要其他文本。"""
        
        response = self.client.chat.completions.create(
            model="doubao-seed-2-0-lite-260215",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
        )
        
        result = response.choices[0].message.content
        
        try:
            evaluation = json.loads(result)
            
            # 打印评估结果
            print(f"   状态: {evaluation.get('status', 'unknown')}")
            print(f"   评分: {evaluation.get('score', 0)}/10")
            
            if evaluation.get('issues'):
                print(f"   问题: {len(evaluation['issues'])}个")
                for issue in evaluation['issues'][:3]:
                    print(f"      - {issue}")
            
            if evaluation.get('strengths'):
                print(f"   优点: {len(evaluation['strengths'])}个")
            
            print()
            
            return evaluation
            
        except json.JSONDecodeError:
            print("⚠️  评估结果JSON解析失败\n")
            return {
                "status": "fail",
                "score": 0,
                "issues": ["评估失败"],
                "suggestions": ["重新运行评估"],
                "raw_content": result
            }


def main():
    """主函数"""
    
    print("\n" + "="*80)
    print("🚀 AutoPaper Phase 3 - 沙盒执行与评估闭环")
    print("="*80 + "\n")
    
    # 检查API密钥
    if not os.getenv('ARK_API_KEY'):
        print("❌ 错误：未设置 ARK_API_KEY 环境变量")
        print("请运行: export ARK_API_KEY='你的API密钥'")
        return
    
    # 检查Phase 2输出文件
    phase2_file = "/Users/leave/Desktop/fc/AutoPaper/phase2_output.json"
    
    if len(sys.argv) > 1:
        phase2_file = sys.argv[1]
    
    if not os.path.exists(phase2_file):
        print(f"❌ 错误：找不到Phase 2输出文件: {phase2_file}")
        print("请先运行 Phase 2 生成Research Proposal")
        return
    
    print(f"📂 加载Phase 2输出: {phase2_file}\n")
    
    # 初始化执行系统
    try:
        execution_system = ExecutionSystem(phase2_file)
        
        # 运行Phase 3
        result = execution_system.run_phase3(max_iterations=5)
        
        # 打印最终结果
        print(f"\n{'='*80}")
        print("✅ Phase 3 完成！")
        print(f"{'='*80}\n")
        print(f"📊 最终状态: {result['summary']['final_status']}")
        print(f"🔁 总迭代次数: {result['summary']['total_iterations']}")
        print(f"📂 实验目录: {result['summary']['experiment_dir']}")
        print(f"\n💡 下一步: 运行 Phase 4 进行论文编撰")
        print(f"{'='*80}\n")
        
    except Exception as e:
        print(f"\n❌ Phase 3 执行失败: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    """
    AutoPaper Phase 3 - 沙盒执行与评估闭环
    
    使用方式：
    
    1️⃣  使用Phase 2的输出（默认）：
        python phase3.py
    
    2️⃣  指定Phase 2输出文件：
        python phase3.py /path/to/phase2_output.json
    
    工作流程：
        1. 任务分解：将Research Proposal分解为DAG任务
        2. 代码生成：自动生成实验代码
        3. 沙盒执行：在隔离环境中运行
        4. 哨兵监控：检测NaN/Inf等异常
        5. 评估器：客观评估结果质量
        6. FARS机制：所有过程Git提交
    
    输出文件：
        - phase3_output.json: 完整执行记录
        - experiments/{exp_name}/: 实验目录（含代码、日志、结果）
    """
    main()
