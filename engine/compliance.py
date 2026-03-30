"""团队规范检查"""
from typing import List, Dict, Any
from agents.roles import Agent
from storage.storage import Storage
from knowledge.knowledge_base import KnowledgeBase


class ComplianceChecker:
    """规范检查器"""

    @staticmethod
    def check_learning_compliance(agent: Agent) -> bool:
        """检查学习规范 - 技术文档必须保存"""
        docs = Storage.list_knowledge("technical")
        return len(docs) > 0

    @staticmethod
    def check_documentation_compliance(project_name: str) -> bool:
        """检查文档规范 - 项目文档必须编写"""
        docs = Storage.list_knowledge("projects")
        return len(docs) > 0

    @staticmethod
    def check_experience_compliance() -> bool:
        """检查经验规范 - 必须总结经验"""
        docs = Storage.list_knowledge("experience")
        return len(docs) > 0

    @staticmethod
    def check_daily_report_compliance(agent_name: str, report_date: str) -> bool:
        """检查日报规范 - 每日必须提交日报"""
        from reports.daily_report import DailyReport
        report = DailyReport.load(agent_name, report_date)
        return report is not None

    @staticmethod
    def get_compliance_status(agent: Agent, project_name: str, report_date: str) -> Dict[str, Any]:
        """获取规范遵守状态"""
        return {
            "learning": ComplianceChecker.check_learning_compliance(agent),
            "documentation": ComplianceChecker.check_documentation_compliance(project_name),
            "experience": ComplianceChecker.check_experience_compliance(),
            "daily_report": ComplianceChecker.check_daily_report_compliance(agent.name, report_date),
        }

    @staticmethod
    def enforce_compliance(agent: Agent, project_name: str, report_date: str) -> List[str]:
        """强制执行规范 - 返回未完成的规范列表"""
        violations = []
        status = ComplianceChecker.get_compliance_status(agent, project_name, report_date)

        if not status["learning"]:
            violations.append("未保存技术文档")
        if not status["documentation"]:
            violations.append("未编写项目文档")
        if not status["experience"]:
            violations.append("未总结项目经验")
        if not status["daily_report"]:
            violations.append("未提交日报")

        return violations
