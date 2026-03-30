"""Agent工作执行器"""
from typing import Dict, Any, Optional
from agents.roles import Agent, AgentRole, WorkflowState
from engine.workflow import Workflow
from engine.decision import DecisionEngine
from engine.compliance import ComplianceChecker
from projects.project import Project, Task
from reports.daily_report import DailyReport
from storage.storage import Storage
from datetime import datetime
from config import DATE_FORMAT


class AgentExecutor:
    """Agent执行器 - 管理Agent的工作流程"""

    def __init__(self):
        self.workflow = Workflow()
        self.decision_engine = DecisionEngine()

    def execute_blueprint(self, agent: Agent, project: Project) -> bool:
        """执行：制作人提出蓝图"""
        if agent.role != AgentRole.PRODUCER or self.workflow.current_state != WorkflowState.IDLE:
            return False

        project.blueprint = {
            "name": project.name,
            "description": project.description,
            "created_by": agent.name,
            "created_at": datetime.now().isoformat(),
        }
        project.save()
        return self.workflow.transition(agent)

    def execute_design(self, agent: Agent, project: Project) -> bool:
        """执行：策划生成方案设计"""
        if agent.role != AgentRole.DESIGNER or self.workflow.current_state != WorkflowState.BLUEPRINT:
            return False

        # 调用Claude API生成设计方案
        design_result = self.decision_engine.generate_design_proposal(
            project.name,
            project.blueprint
        )
        project.design_proposal = design_result
        project.save()
        return self.workflow.transition(agent)

    def execute_design_review(self, agent: Agent, project: Project) -> bool:
        """执行：制作人审查方案"""
        if agent.role != AgentRole.PRODUCER or self.workflow.current_state != WorkflowState.DESIGN:
            return False

        # 调用Claude API审查设计
        review_result = self.decision_engine.review_design(project.design_proposal)
        project.design_proposal["review"] = review_result
        project.save()
        return self.workflow.transition(agent)

    def execute_presentation(self, agent: Agent, project: Project) -> bool:
        """执行：策划会议宣讲"""
        if agent.role != AgentRole.DESIGNER or self.workflow.current_state != WorkflowState.DESIGN_REVIEW:
            return False

        project.design_proposal["presentation"] = {
            "presented_by": agent.name,
            "presented_at": datetime.now().isoformat(),
            "attendees": ["Programmer", "Artist", "DevOps"],
        }
        project.save()
        return self.workflow.transition(agent)

    def execute_design_adjust(self, agent: Agent, project: Project) -> bool:
        """执行：策划调整方案"""
        if agent.role != AgentRole.DESIGNER or self.workflow.current_state != WorkflowState.PRESENTATION:
            return False

        project.design_proposal["adjusted"] = True
        project.design_proposal["adjusted_at"] = datetime.now().isoformat()
        project.save()
        return self.workflow.transition(agent)

    def execute_design_confirm(self, agent: Agent, project: Project) -> bool:
        """执行：制作人确定方案"""
        if agent.role != AgentRole.PRODUCER or self.workflow.current_state != WorkflowState.DESIGN_ADJUST:
            return False

        project.design_proposal["confirmed"] = True
        project.design_proposal["confirmed_at"] = datetime.now().isoformat()
        project.save()
        return self.workflow.transition(agent)

    def execute_requirement_analysis(self, agent: Agent, project: Project) -> bool:
        """执行：程序分析需求"""
        if agent.role != AgentRole.PROGRAMMER or self.workflow.current_state != WorkflowState.DESIGN_CONFIRM:
            return False

        # 调用Claude API分析需求
        analysis_result = self.decision_engine.analyze_requirements(
            project.name,
            project.blueprint
        )
        project.requirements = analysis_result
        project.save()
        return self.workflow.transition(agent)

    def execute_environment_setup(self, agent: Agent, project: Project) -> bool:
        """执行：程序环境搭建"""
        if agent.role != AgentRole.PROGRAMMER or self.workflow.current_state != WorkflowState.REQUIREMENT_ANALYSIS:
            return False

        # 记录环境搭建信息
        if not hasattr(project, 'environment_setup'):
            project.environment_setup = {}

        project.environment_setup = {
            "setup_by": agent.name,
            "setup_at": datetime.now().isoformat(),
            "components": ["Git", "Jenkins", "Task Board"],
        }
        project.save()
        return self.workflow.transition(agent)

    def execute_development(self, agent: Agent, project: Project) -> bool:
        """执行：程序开发功能"""
        if agent.role != AgentRole.PROGRAMMER or self.workflow.current_state != WorkflowState.ENVIRONMENT_SETUP:
            return False

        if not hasattr(project, 'development'):
            project.development = {}

        project.development = {
            "started_by": agent.name,
            "started_at": datetime.now().isoformat(),
        }
        project.save()
        return self.workflow.transition(agent)

    def execute_resource_creation(self, agent: Agent, project: Project) -> bool:
        """执行：美术制作资源"""
        if agent.role != AgentRole.ARTIST or self.workflow.current_state != WorkflowState.DEVELOPMENT:
            return False

        if not hasattr(project, 'resources'):
            project.resources = {}

        project.resources = {
            "created_by": agent.name,
            "created_at": datetime.now().isoformat(),
        }
        project.save()
        return self.workflow.transition(agent)

    def execute_deployment(self, agent: Agent, project: Project) -> bool:
        """执行：运维部署发布"""
        if agent.role != AgentRole.DEVOPS or self.workflow.current_state != WorkflowState.RESOURCE_CREATION:
            return False

        if not hasattr(project, 'deployment'):
            project.deployment = {}

        project.deployment = {
            "deployed_by": agent.name,
            "deployed_at": datetime.now().isoformat(),
            "status": "completed",
        }
        project.save()
        return self.workflow.transition(agent)

    def generate_daily_report(self, agent: Agent, completed_tasks: list, issues: list = None, tomorrow_plan: list = None, new_knowledge: list = None) -> DailyReport:
        """生成日报"""
        report_date = datetime.now().strftime(DATE_FORMAT)
        report = DailyReport(
            agent_name=agent.name,
            report_date=report_date,
            completed_tasks=completed_tasks,
            issues=issues or [],
            tomorrow_plan=tomorrow_plan or [],
            new_knowledge=new_knowledge or [],
        )
        report.save()
        return report

    def get_workflow_status(self) -> Dict[str, Any]:
        """获取工作流状态"""
        return {
            "current_state": self.workflow.current_state.value,
            "next_state": self.workflow.get_next_state().value if self.workflow.get_next_state() else None,
            "required_role": self.workflow.get_required_role().value if self.workflow.get_required_role() else None,
        }
