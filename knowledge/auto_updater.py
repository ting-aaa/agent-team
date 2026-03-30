"""知识库自动更新系统"""
from typing import Dict, Any, List
from knowledge.knowledge_base import KnowledgeBase
from knowledge.capability import CapabilityManager
from reports.daily_report import DailyReport
from reports.growth_tracker import GrowthTracker
from datetime import datetime
from config import DATE_FORMAT


class KnowledgeAutoUpdater:
    """知识库自动更新器"""

    @staticmethod
    def process_daily_report(agent_name: str, report_date: str):
        """处理日报 - 自动更新知识库"""
        report = DailyReport.load(agent_name, report_date)
        if not report:
            return

        # 处理新增知识
        for knowledge in report.new_knowledge:
            KnowledgeAutoUpdater._save_knowledge_from_report(agent_name, knowledge)
            CapabilityManager.increment_knowledge(agent_name)

        # 增加经验值
        if report.completed_tasks:
            CapabilityManager.increment_experience(agent_name, len(report.completed_tasks))

    @staticmethod
    def _save_knowledge_from_report(agent_name: str, knowledge_item: str):
        """从日报中保存知识"""
        doc_name = f"{agent_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        content = f"# {knowledge_item}\n\nRecorded by: {agent_name}\nDate: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        KnowledgeBase.add_technical_doc(doc_name, content)

    @staticmethod
    def process_project_completion(agent_name: str, project_name: str):
        """处理项目完成 - 自动更新能力库"""
        CapabilityManager.increment_projects(agent_name)

        # 记录里程碑
        GrowthTracker.record_milestone(
            agent_name=agent_name,
            milestone=f"Completed project: {project_name}",
            description=f"Successfully completed {project_name}",
            experience_gained=10,
        )

    @staticmethod
    def process_skill_acquisition(agent_name: str, skill_name: str, description: str = ""):
        """处理技能获得 - 自动更新能力库"""
        CapabilityManager.add_skill(agent_name, skill_name, description, "acquired")

        # 记录里程碑
        GrowthTracker.record_milestone(
            agent_name=agent_name,
            milestone=f"Acquired skill: {skill_name}",
            description=description or f"Acquired new skill: {skill_name}",
            skills_gained=[skill_name],
            experience_gained=5,
        )

    @staticmethod
    def generate_agent_growth_report(agent_name: str) -> Dict[str, Any]:
        """生成Agent成长报告"""
        from knowledge.capability import AgentCapability

        capability = AgentCapability.load(agent_name)
        growth_history = GrowthTracker.get_agent_growth_history(agent_name)

        return {
            "agent_name": agent_name,
            "current_capability": capability.to_dict(),
            "growth_history": growth_history,
            "summary": {
                "total_skills": len(capability.skills),
                "experience_level": capability.experience_level,
                "projects_completed": capability.projects_completed,
                "knowledge_docs": capability.knowledge_docs,
                "total_milestones": len(growth_history),
            }
        }

    @staticmethod
    def generate_team_growth_report() -> Dict[str, Any]:
        """生成团队成长报告"""
        from knowledge.capability import CapabilityManager

        team_capability = CapabilityManager.get_team_capability_summary()
        team_growth = GrowthTracker.get_team_growth_summary()

        return {
            "team_capability": team_capability,
            "team_growth": team_growth,
            "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
