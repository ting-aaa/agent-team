"""测试脚本 - 验证Phase 2功能"""
from agents.roles import Producer, Designer, Programmer, Artist, DevOps
from projects.project import Project, Task
from engine.executor import AgentExecutor
from engine.task_decomposer import TaskDecomposer
from reports.daily_report import DailyReport
from knowledge.knowledge_base import KnowledgeBase
from datetime import datetime
from config import DATE_FORMAT


def test_workflow_execution():
    """测试工作流执行"""
    print("[TEST] Workflow Execution")

    # 创建Agent
    producer = Producer("Producer")
    designer = Designer("Designer")
    programmer = Programmer("Programmer")
    artist = Artist("Artist")
    devops = DevOps("DevOps")

    # 创建项目
    project = Project(
        name="TestProject",
        description="A test project for workflow execution"
    )

    # 创建执行器
    executor = AgentExecutor()

    # 执行工作流
    print(f"  Initial state: {executor.get_workflow_status()['current_state']}")

    # 制作人提出蓝图
    if executor.execute_blueprint(producer, project):
        print(f"  [OK] Producer created blueprint")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Producer failed to create blueprint")
        return

    # 策划生成方案
    if executor.execute_design(designer, project):
        print(f"  [OK] Designer created design proposal")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Designer failed to create design proposal")
        return

    # 制作人审查方案
    if executor.execute_design_review(producer, project):
        print(f"  [OK] Producer reviewed design")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Producer failed to review design")
        return

    # 策划宣讲
    if executor.execute_presentation(designer, project):
        print(f"  [OK] Designer presented design")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Designer failed to present design")
        return

    # 策划调整方案
    if executor.execute_design_adjust(designer, project):
        print(f"  [OK] Designer adjusted design")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Designer failed to adjust design")
        return

    # 制作人确定方案
    if executor.execute_design_confirm(producer, project):
        print(f"  [OK] Producer confirmed design")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Producer failed to confirm design")
        return

    # 程序分析需求
    if executor.execute_requirement_analysis(programmer, project):
        print(f"  [OK] Programmer analyzed requirements")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Programmer failed to analyze requirements")
        return

    # 程序环境搭建
    if executor.execute_environment_setup(programmer, project):
        print(f"  [OK] Programmer set up environment")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Programmer failed to set up environment")
        return

    # 程序开发
    if executor.execute_development(programmer, project):
        print(f"  [OK] Programmer started development")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Programmer failed to start development")
        return

    # 美术制作资源
    if executor.execute_resource_creation(artist, project):
        print(f"  [OK] Artist created resources")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] Artist failed to create resources")
        return

    # 运维部署
    if executor.execute_deployment(devops, project):
        print(f"  [OK] DevOps deployed project")
        print(f"  Current state: {executor.get_workflow_status()['current_state']}")
    else:
        print(f"  [FAIL] DevOps failed to deploy project")
        return

    print(f"  [OK] Workflow completed successfully")


def test_task_decomposition():
    """测试任务分解"""
    print("\n[TEST] Task Decomposition")

    main_task = Task(
        name="Develop API",
        description="Develop REST API",
        assigned_to="Programmer"
    )

    subtasks = [
        {"name": "Design API endpoints", "description": "Design REST endpoints"},
        {"name": "Implement endpoints", "description": "Implement endpoints"},
        {"name": "Write tests", "description": "Write unit tests"},
    ]

    decomposer = TaskDecomposer()
    decomposer.decompose_task(main_task, subtasks)

    print(f"  Main task: {main_task.name}")
    print(f"  Subtasks: {len(main_task.subtasks)}")
    for st in main_task.subtasks:
        print(f"    - {st.name}")

    # 标记子任务完成
    decomposer.mark_subtask_completed(main_task, "Design API endpoints")
    progress = decomposer.get_task_progress(main_task)
    print(f"  Progress: {progress['completed_subtasks']}/{progress['total_subtasks']} ({progress['progress_percentage']:.0f}%)")


def test_daily_report():
    """测试日报生成"""
    print("\n[TEST] Daily Report Generation")

    programmer = Programmer("Programmer")
    executor = AgentExecutor()

    report = executor.generate_daily_report(
        programmer,
        completed_tasks=["Analyzed requirements", "Set up environment"],
        issues=["Database connection issue"],
        tomorrow_plan=["Start development", "Write unit tests"],
        new_knowledge=["PostgreSQL optimization techniques"]
    )

    print(f"  Report date: {report.report_date}")
    print(f"  Completed tasks: {len(report.completed_tasks)}")
    print(f"  Issues: {len(report.issues)}")
    print(f"  Tomorrow plan: {len(report.tomorrow_plan)}")
    print(f"  New knowledge: {len(report.new_knowledge)}")
    print(f"\n{report}")


def test_knowledge_base():
    """测试知识库"""
    print("\n[TEST] Knowledge Base")

    # 添加技术文档
    KnowledgeBase.add_technical_doc(
        "python_best_practices",
        "# Python Best Practices\n\n1. Use type hints\n2. Follow PEP 8"
    )

    # 添加项目文档
    KnowledgeBase.add_project_doc(
        "api_design",
        "# API Design\n\n## Endpoints\n- GET /api/users\n- POST /api/users"
    )

    # 添加经验总结
    KnowledgeBase.add_experience(
        "project_lessons",
        "# Project Lessons\n\n1. Start with clear requirements\n2. Test early and often"
    )

    print(f"  Technical docs: {KnowledgeBase.list_docs('technical')}")
    print(f"  Project docs: {KnowledgeBase.list_docs('projects')}")
    print(f"  Experience: {KnowledgeBase.list_docs('experience')}")


if __name__ == "__main__":
    print("=== Phase 2 Tests ===\n")
    test_workflow_execution()
    test_task_decomposition()
    test_daily_report()
    test_knowledge_base()
    print("\n[OK] All tests completed")
