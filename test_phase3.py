"""Phase 3测试 - 日报和知识积累"""
from agents.roles import Programmer, Designer
from engine.executor import AgentExecutor
from knowledge.auto_updater import KnowledgeAutoUpdater
from knowledge.capability import CapabilityManager
from reports.growth_tracker import GrowthTracker
from datetime import datetime
from config import DATE_FORMAT


def test_knowledge_auto_update():
    """测试知识库自动更新"""
    print("[TEST] Knowledge Auto Update")

    programmer = Programmer("Programmer")

    # 生成日报
    executor = AgentExecutor()
    report = executor.generate_daily_report(
        programmer,
        completed_tasks=["Implemented API", "Wrote tests"],
        issues=["Performance issue"],
        tomorrow_plan=["Optimize database"],
        new_knowledge=["Database indexing strategies", "Query optimization"]
    )

    print(f"  Generated report for {report.agent_name}")

    # 自动更新知识库
    report_date = datetime.now().strftime(DATE_FORMAT)
    KnowledgeAutoUpdater.process_daily_report(programmer.name, report_date)

    print(f"  [OK] Knowledge auto-updated from daily report")


def test_capability_management():
    """测试能力库管理"""
    print("\n[TEST] Capability Management")

    programmer = Programmer("Programmer")

    # 添加技能
    CapabilityManager.add_skill(programmer.name, "Python", "Python programming", "language")
    CapabilityManager.add_skill(programmer.name, "PostgreSQL", "Database management", "database")

    # 增加经验
    CapabilityManager.increment_experience(programmer.name, 10)

    # 增加项目数
    CapabilityManager.increment_projects(programmer.name)

    # 获取能力
    capability = CapabilityManager.get_capability(programmer.name)
    print(f"  Agent: {capability.agent_name}")
    print(f"  Skills: {capability.skills}")
    print(f"  Experience: {capability.experience_level}")
    print(f"  Projects: {capability.projects_completed}")


def test_growth_tracking():
    """测试成长追踪"""
    print("\n[TEST] Growth Tracking")

    designer = Designer("Designer")

    # 记录里程碑
    GrowthTracker.record_milestone(
        designer.name,
        "Completed first design",
        "Successfully designed system architecture",
        skills_gained=["System Design", "Architecture"],
        experience_gained=15
    )

    GrowthTracker.record_milestone(
        designer.name,
        "Mastered design patterns",
        "Learned and applied design patterns",
        skills_gained=["Design Patterns"],
        experience_gained=10
    )

    # 获取成长历史
    history = GrowthTracker.get_agent_growth_history(designer.name)
    print(f"  Agent: {designer.name}")
    print(f"  Total milestones: {len(history)}")
    for record in history:
        print(f"    - {record['milestone']} ({record['record_date']})")


def test_agent_growth_report():
    """测试Agent成长报告"""
    print("\n[TEST] Agent Growth Report")

    programmer = Programmer("Programmer")

    # 模拟成长
    CapabilityManager.add_skill(programmer.name, "Python", "Python programming", "language")
    CapabilityManager.add_skill(programmer.name, "Docker", "Container management", "devops")
    CapabilityManager.increment_experience(programmer.name, 20)
    CapabilityManager.increment_projects(programmer.name)
    CapabilityManager.increment_knowledge(programmer.name)

    GrowthTracker.record_milestone(
        programmer.name,
        "Completed first project",
        "Successfully completed TestProject",
        experience_gained=10
    )

    # 生成报告
    report = KnowledgeAutoUpdater.generate_agent_growth_report(programmer.name)

    print(f"  Agent: {report['agent_name']}")
    print(f"  Summary:")
    for key, value in report['summary'].items():
        print(f"    - {key}: {value}")


def test_team_growth_report():
    """测试团队成长报告"""
    print("\n[TEST] Team Growth Report")

    # 模拟多个Agent的成长
    programmer = Programmer("Programmer")
    designer = Designer("Designer")

    CapabilityManager.add_skill(programmer.name, "Python", "Python programming", "language")
    CapabilityManager.increment_experience(programmer.name, 15)

    CapabilityManager.add_skill(designer.name, "Figma", "UI Design", "design")
    CapabilityManager.increment_experience(designer.name, 10)

    # 生成团队报告
    report = KnowledgeAutoUpdater.generate_team_growth_report()

    print(f"  Team capability summary:")
    for agent_name, capability in report['team_capability'].items():
        print(f"    - {agent_name}: {capability['experience_level']} exp, {len(capability['skills'])} skills")


if __name__ == "__main__":
    print("=== Phase 3 Tests ===\n")
    test_knowledge_auto_update()
    test_capability_management()
    test_growth_tracking()
    test_agent_growth_report()
    test_team_growth_report()
    print("\n[OK] All Phase 3 tests completed")
