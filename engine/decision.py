"""决策执行系统 - 集成Claude API"""
from typing import Optional, Dict, Any
import anthropic
from config import CLAUDE_API_KEY


class DecisionEngine:
    """决策引擎"""

    def __init__(self):
        self.client = anthropic.Anthropic(api_key=CLAUDE_API_KEY)

    def analyze_requirements(self, project_name: str, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """分析需求"""
        prompt = f"""
项目名称: {project_name}
项目蓝图: {blueprint}

请分析这个项目的需求，生成详细的需求分析文档，包括：
1. 功能需求
2. 非功能需求
3. 技术栈建议
4. 风险评估
"""
        try:
            response = self.client.messages.create(
                model="[REDACTED]",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return {"analysis": response.content[0].text}
        except Exception as e:
            return {"analysis": f"Error: {str(e)}", "error": True}

    def generate_design_proposal(self, project_name: str, blueprint: Dict[str, Any]) -> Dict[str, Any]:
        """生成设计方案"""
        prompt = f"""
项目名称: {project_name}
项目蓝图: {blueprint}

请生成详细的设计方案，包括：
1. 系统架构设计
2. 模块划分
3. 数据流设计
4. 接口设计
5. 技术方案选型
"""
        try:
            response = self.client.messages.create(
                model="[REDACTED]",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            return {"proposal": response.content[0].text}
        except Exception as e:
            return {"proposal": f"Error: {str(e)}", "error": True}

    def solve_problem(self, problem_description: str, context: Optional[str] = None) -> str:
        """解决问题"""
        prompt = problem_description
        if context:
            prompt = f"{context}\n\n问题: {problem_description}"

        try:
            response = self.client.messages.create(
                model="[REDACTED]",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text
        except Exception as e:
            return f"Error: {str(e)}"

    def review_design(self, design_proposal: Dict[str, Any]) -> Dict[str, Any]:
        """审查设计"""
        prompt = f"""
请审查以下设计方案，并提供反馈：

{design_proposal}

请从以下方面进行审查：
1. 架构合理性
2. 技术可行性
3. 风险识别
4. 改进建议
"""
        try:
            response = self.client.messages.create(
                model="[REDACTED]",
                max_tokens=1500,
                messages=[{"role": "user", "content": prompt}]
            )
            return {"review": response.content[0].text}
        except Exception as e:
            return {"review": f"Error: {str(e)}", "error": True}
