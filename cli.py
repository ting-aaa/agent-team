"""CLI命令行界面"""
import argparse
import json
from datetime import datetime
from config import DATE_FORMAT
from engine.executor import AgentExecutor
from engine.workflow import Workflow
from projects.project import Project
from agents.roles import Producer, Designer, Programmer, Artist, DevOps, AgentRole
from knowledge.knowledge_base import KnowledgeBase
from knowledge.auto_updater import KnowledgeAutoUpdater
from capabilities.skill_manager import SkillManager
from capabilities.tool_manager import ToolManager
from capabilities.recruiter import AgentRecruiter
from reports.daily_report import DailyReport


class CLI:
    """命令行界面"""

    def __init__(self):
        self.executor = AgentExecutor()
        self.workflow = Workflow()

    def cmd_project_create(self, args):
        """创建项目"""
        project = Project(name=args.name, description=args.description)
        project.save()
        print(f"[OK] Project created: {args.name}")

    def cmd_project_status(self, args):
        """查看项目状态"""
        project = Project.load(args.name)
        if not project:
            print(f"[ERROR] Project not found: {args.name}")
            return

        status = self.executor.get_workflow_status()
        print(f"Project: {project.name}")
        print(f"Current state: {status['current_state']}")
        print(f"Next state: {status['next_state']}")
        print(f"Required role: {status['required_role']}")

    def cmd_workflow_execute(self, args):
        """执行工作流步骤"""
        project = Project.load(args.project)
        if not project:
            print(f"[ERROR] Project not found: {args.project}")
            return

        role_map = {
            "producer": Producer(),
            "designer": Designer(),
            "programmer": Programmer(),
            "artist": Artist(),
            "devops": DevOps(),
        }

        agent = role_map.get(args.role)
        if not agent:
            print(f"[ERROR] Invalid role: {args.role}")
            return

        methods = {
            "blueprint": self.executor.execute_blueprint,
            "design": self.executor.execute_design,
            "design_review": self.executor.execute_design_review,
            "presentation": self.executor.execute_presentation,
            "design_adjust": self.executor.execute_design_adjust,
            "design_confirm": self.executor.execute_design_confirm,
            "requirement_analysis": self.executor.execute_requirement_analysis,
            "environment_setup": self.executor.execute_environment_setup,
            "development": self.executor.execute_development,
            "resource_creation": self.executor.execute_resource_creation,
            "deployment": self.executor.execute_deployment,
        }

        method = methods.get(args.step)
        if not method:
            print(f"[ERROR] Invalid step: {args.step}")
            return

        if method(agent, project):
            print(f"[OK] {args.step} completed by {agent.name}")
        else:
            print(f"[ERROR] {args.step} failed")

    def cmd_daily_report(self, args):
        """生成日报"""
        role_map = {
            "producer": Producer(),
            "designer": Designer(),
            "programmer": Programmer(),
            "artist": Artist(),
            "devops": DevOps(),
        }

        agent = role_map.get(args.role)
        if not agent:
            print(f"[ERROR] Invalid role: {args.role}")
            return

        report = self.executor.generate_daily_report(
            agent,
            completed_tasks=args.tasks.split(",") if args.tasks else [],
            issues=args.issues.split(",") if args.issues else [],
            tomorrow_plan=args.plan.split(",") if args.plan else [],
            new_knowledge=args.knowledge.split(",") if args.knowledge else []
        )

        print(f"[OK] Daily report generated for {agent.name}")
        print(report)

    def cmd_knowledge_list(self, args):
        """列出知识库"""
        docs = KnowledgeBase.list_docs(args.category)
        print(f"[{args.category}] Documents: {len(docs)}")
        for doc in docs:
            print(f"  - {doc}")

    def cmd_knowledge_add(self, args):
        """添加知识"""
        if args.category == "technical":
            KnowledgeBase.add_technical_doc(args.name, args.content)
        elif args.category == "projects":
            KnowledgeBase.add_project_doc(args.name, args.content)
        elif args.category == "experience":
            KnowledgeBase.add_experience(args.name, args.content)
        elif args.category == "api":
            KnowledgeBase.add_api_doc(args.name, args.content)

        print(f"[OK] Knowledge added: {args.name}")

    def cmd_skill_create(self, args):
        """创建Skill"""
        skill = SkillManager.create_skill(
            name=args.name,
            description=args.description,
            category=args.category,
            implementation=args.implementation,
            created_by=args.created_by
        )
        print(f"[OK] Skill created: {args.name}")

    def cmd_skill_list(self, args):
        """列出Skill"""
        skills = SkillManager.list_skills(args.category)
        print(f"Skills: {len(skills)}")
        for skill in skills:
            print(f"  - {skill}")

    def cmd_tool_create(self, args):
        """创建工具"""
        tool = ToolManager.create_tool(
            name=args.name,
            description=args.description,
            tool_type=args.type,
            implementation=args.implementation,
            created_by=args.created_by
        )
        print(f"[OK] Tool created: {args.name}")

    def cmd_tool_list(self, args):
        """列出工具"""
        tools = ToolManager.list_tools(args.type)
        print(f"Tools: {len(tools)}")
        for tool in tools:
            print(f"  - {tool}")

    def cmd_recruit_agent(self, args):
        """招募Agent"""
        role = AgentRole(args.role)
        agent = AgentRecruiter.recruit_agent(
            name=args.name,
            role=role,
            skills=args.skills.split(",") if args.skills else [],
            description=args.description
        )
        print(f"[OK] Agent recruited: {args.name} ({args.role})")

    def cmd_team_status(self, args):
        """查看团队状态"""
        composition = AgentRecruiter.get_team_composition()
        print(f"Team size: {AgentRecruiter.get_team_size()}")
        print(f"Composition:")
        for role, count in composition.items():
            print(f"  - {role}: {count}")

    def cmd_growth_report(self, args):
        """生成成长报告"""
        report = KnowledgeAutoUpdater.generate_agent_growth_report(args.agent)
        print(f"Agent: {report['agent_name']}")
        print(f"Summary:")
        for key, value in report['summary'].items():
            print(f"  - {key}: {value}")


def main():
    parser = argparse.ArgumentParser(description="AI Harness CLI")
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Project commands
    project_parser = subparsers.add_parser("project", help="Project management")
    project_sub = project_parser.add_subparsers(dest="subcommand")

    create_parser = project_sub.add_parser("create", help="Create project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("description", help="Project description")

    status_parser = project_sub.add_parser("status", help="Project status")
    status_parser.add_argument("name", help="Project name")

    # Workflow commands
    workflow_parser = subparsers.add_parser("workflow", help="Workflow execution")
    workflow_parser.add_argument("project", help="Project name")
    workflow_parser.add_argument("role", help="Agent role")
    workflow_parser.add_argument("step", help="Workflow step")

    # Daily report
    report_parser = subparsers.add_parser("report", help="Daily report")
    report_parser.add_argument("role", help="Agent role")
    report_parser.add_argument("--tasks", help="Completed tasks (comma-separated)")
    report_parser.add_argument("--issues", help="Issues (comma-separated)")
    report_parser.add_argument("--plan", help="Tomorrow plan (comma-separated)")
    report_parser.add_argument("--knowledge", help="New knowledge (comma-separated)")

    # Knowledge commands
    knowledge_parser = subparsers.add_parser("knowledge", help="Knowledge management")
    knowledge_sub = knowledge_parser.add_subparsers(dest="subcommand")

    list_parser = knowledge_sub.add_parser("list", help="List knowledge")
    list_parser.add_argument("category", help="Category")

    add_parser = knowledge_sub.add_parser("add", help="Add knowledge")
    add_parser.add_argument("category", help="Category")
    add_parser.add_argument("name", help="Document name")
    add_parser.add_argument("content", help="Content")

    # Skill commands
    skill_parser = subparsers.add_parser("skill", help="Skill management")
    skill_sub = skill_parser.add_subparsers(dest="subcommand")

    skill_create = skill_sub.add_parser("create", help="Create skill")
    skill_create.add_argument("name", help="Skill name")
    skill_create.add_argument("description", help="Description")
    skill_create.add_argument("category", help="Category")
    skill_create.add_argument("implementation", help="Implementation")
    skill_create.add_argument("created_by", help="Created by")

    skill_list = skill_sub.add_parser("list", help="List skills")
    skill_list.add_argument("--category", help="Filter by category")

    # Tool commands
    tool_parser = subparsers.add_parser("tool", help="Tool management")
    tool_sub = tool_parser.add_subparsers(dest="subcommand")

    tool_create = tool_sub.add_parser("create", help="Create tool")
    tool_create.add_argument("name", help="Tool name")
    tool_create.add_argument("description", help="Description")
    tool_create.add_argument("type", help="Tool type")
    tool_create.add_argument("implementation", help="Implementation")
    tool_create.add_argument("created_by", help="Created by")

    tool_list = tool_sub.add_parser("list", help="List tools")
    tool_list.add_argument("--type", help="Filter by type")

    # Agent commands
    agent_parser = subparsers.add_parser("agent", help="Agent management")
    agent_sub = agent_parser.add_subparsers(dest="subcommand")

    recruit = agent_sub.add_parser("recruit", help="Recruit agent")
    recruit.add_argument("name", help="Agent name")
    recruit.add_argument("role", help="Agent role")
    recruit.add_argument("--skills", help="Skills (comma-separated)")
    recruit.add_argument("--description", help="Description")

    team = agent_sub.add_parser("team", help="Team status")

    # Growth report
    growth_parser = subparsers.add_parser("growth", help="Growth report")
    growth_parser.add_argument("agent", help="Agent name")

    args = parser.parse_args()

    cli = CLI()

    if args.command == "project":
        if args.subcommand == "create":
            cli.cmd_project_create(args)
        elif args.subcommand == "status":
            cli.cmd_project_status(args)

    elif args.command == "workflow":
        cli.cmd_workflow_execute(args)

    elif args.command == "report":
        cli.cmd_daily_report(args)

    elif args.command == "knowledge":
        if args.subcommand == "list":
            cli.cmd_knowledge_list(args)
        elif args.subcommand == "add":
            cli.cmd_knowledge_add(args)

    elif args.command == "skill":
        if args.subcommand == "create":
            cli.cmd_skill_create(args)
        elif args.subcommand == "list":
            cli.cmd_skill_list(args)

    elif args.command == "tool":
        if args.subcommand == "create":
            cli.cmd_tool_create(args)
        elif args.subcommand == "list":
            cli.cmd_tool_list(args)

    elif args.command == "agent":
        if args.subcommand == "recruit":
            cli.cmd_recruit_agent(args)
        elif args.subcommand == "team":
            cli.cmd_team_status(args)

    elif args.command == "growth":
        cli.cmd_growth_report(args)


if __name__ == "__main__":
    main()
