"""完整集成测试"""
from agents.roles import Producer, Designer, Programmer, Artist, DevOps
from projects.project import Project
from engine.executor import AgentExecutor
from knowledge.auto_updater import KnowledgeAutoUpdater
from capabilities.recruiter import AgentRecruiter
from agents.roles import AgentRole
from datetime import datetime
from config import DATE_FORMAT


def test_complete_workflow():
    """测试完整工作流"""
    print("=== Complete Workflow Integration Test ===\n")

    # 创建项目
    project = Project(
        name="CompleteTest",
        description="Complete workflow test"
    )
    project.save()
    print("[OK] Project created: CompleteTest")

    # 创建执行器
    executor = AgentExecutor()

    # 创建Agent
    producer = Producer("Producer")
    designer = Designer("Designer")
    programmer = Programmer("Programmer")
    artist = Artist("Artist")
    devops = DevOps("DevOps")

    # 执行完整工作流
    steps = [
        ("producer", "blueprint", executor.execute_blueprint),
        ("designer", "design", executor.execute_design),
        ("producer", "design_review", executor.execute_design_review),
        ("designer", "presentation", executor.execute_presentation),
        ("designer", "design_adjust", executor.execute_design_adjust),
        ("producer", "design_confirm", executor.execute_design_confirm),
        ("programmer", "requirement_analysis", executor.execute_requirement_analysis),
        ("programmer", "environment_setup", executor.execute_environment_setup),
        ("programmer", "development", executor.execute_development),
        ("artist", "resource_creation", executor.execute_resource_creation),
        ("devops", "deployment", executor.execute_deployment),
    ]

    agents = {
        "producer": producer,
        "designer": designer,
        "programmer": programmer,
        "artist": artist,
        "devops": devops,
    }

    for role, step, method in steps:
        agent = agents[role]
        if method(agent, project):
            print(f"[OK] {step} completed by {role}")
        else:
            print(f"[ERROR] {step} failed")
            return

    print("\n[OK] Complete workflow executed successfully")

    # 生成日报
    report = executor.generate_daily_report(
        programmer,
        completed_tasks=["Analyzed requirements", "Set up environment", "Developed features"],
        issues=["Performance issue"],
        tomorrow_plan=["Optimize database", "Write tests"],
        new_knowledge=["Database indexing", "Query optimization"]
    )

    print(f"\n[OK] Daily report generated")

    # 自动更新知识库
    report_date = datetime.now().strftime(DATE_FORMAT)
    KnowledgeAutoUpdater.process_daily_report(programmer.name, report_date)
    print(f"[OK] Knowledge base auto-updated")

    # 处理项目完成
    KnowledgeAutoUpdater.process_project_completion(programmer.name, "CompleteTest")
    print(f"[OK] Project completion recorded")

    # 生成成장报告
    growth_report = KnowledgeAutoUpdater.generate_agent_growth_report(programmer.name)
    print(f"\n[OK] Growth report generated")
    print(f"  Skills: {growth_report['summary']['total_skills']}")
    print(f"  Experience: {growth_report['summary']['experience_level']}")
    print(f"  Projects: {growth_report['summary']['projects_completed']}")

    # 招募新Agent
    new_agent = AgentRecruiter.recruit_agent(
        name="DevOps_Engineer",
        role=AgentRole.DEVOPS,
        skills=["Kubernetes", "Docker", "CI/CD"],
        description="Senior DevOps engineer"
    )
    print(f"\n[OK] New agent recruited: {new_agent.name}")

    # 查看团队状态
    composition = AgentRecruiter.get_team_composition()
    print(f"\n[OK] Team composition:")
    for role, count in composition.items():
        print(f"  - {role}: {count}")

    print(f"\n[OK] Complete integration test passed")


if __name__ == "__main__":
    test_complete_workflow()
