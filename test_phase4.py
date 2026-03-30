"""Phase 4测试 - 能力扩展系统"""
from capabilities.skill_manager import SkillManager
from capabilities.tool_manager import ToolManager
from capabilities.infrastructure import EnvironmentManager, ServiceManager
from capabilities.recruiter import AgentRecruiter
from agents.roles import AgentRole, Programmer, Designer


def test_skill_management():
    """测试Skill管理"""
    print("[TEST] Skill Management")

    # 创建Skill
    skill = SkillManager.create_skill(
        name="API_Development",
        description="REST API development",
        category="backend",
        implementation="FastAPI framework",
        created_by="Programmer",
        tags=["python", "api"]
    )
    print(f"  Created skill: {skill.name}")

    # 列出Skill
    skills = SkillManager.list_skills()
    print(f"  Total skills: {len(skills)}")

    # 按分类获取
    by_category = SkillManager.get_skills_by_category()
    print(f"  Skills by category: {list(by_category.keys())}")


def test_tool_management():
    """测试工具管理"""
    print("\n[TEST] Tool Management")

    # 创建工具
    tool = ToolManager.create_tool(
        name="DockerBuilder",
        description="Docker image builder",
        tool_type="devops",
        implementation="Docker CLI wrapper",
        created_by="DevOps",
        dependencies=["docker"]
    )
    print(f"  Created tool: {tool.name}")

    # 列出工具
    tools = ToolManager.list_tools()
    print(f"  Total tools: {len(tools)}")

    # 按类型获取
    by_type = ToolManager.get_tools_by_type()
    print(f"  Tools by type: {list(by_type.keys())}")


def test_environment_management():
    """测试环境管理"""
    print("\n[TEST] Environment Management")

    # 创建环境
    env = EnvironmentManager.create_environment(
        name="dev_environment",
        description="Development environment",
        components=["Python 3.10", "PostgreSQL", "Redis"],
        setup_script="#!/bin/bash\npip install -r requirements.txt",
        created_by="Programmer"
    )
    print(f"  Created environment: {env.name}")

    # 列出环境
    envs = EnvironmentManager.list_environments()
    print(f"  Total environments: {len(envs)}")


def test_service_management():
    """测试服务管理"""
    print("\n[TEST] Service Management")

    # 创建服务
    service = ServiceManager.create_service(
        name="api_service",
        description="REST API service",
        service_type="backend",
        deployment_config={
            "port": 8000,
            "workers": 4,
            "framework": "FastAPI"
        },
        created_by="Programmer"
    )
    print(f"  Created service: {service.name}")

    # 列出服务
    services = ServiceManager.list_services()
    print(f"  Total services: {len(services)}")

    # 按类型获取
    by_type = ServiceManager.list_services(service_type="backend")
    print(f"  Backend services: {len(by_type)}")


def test_agent_recruitment():
    """测试Agent招募"""
    print("\n[TEST] Agent Recruitment")

    # 招募新Agent
    new_agent = AgentRecruiter.recruit_agent(
        name="QA_Engineer",
        role=AgentRole.PROGRAMMER,
        skills=["Testing", "Automation", "Python"],
        description="Quality assurance engineer"
    )
    print(f"  Recruited: {new_agent.name} ({new_agent.role.value})")

    # 获取团队规模
    team_size = AgentRecruiter.get_team_size()
    print(f"  Team size: {team_size}")

    # 获取团队组成
    composition = AgentRecruiter.get_team_composition()
    print(f"  Team composition:")
    for role, count in composition.items():
        print(f"    - {role}: {count}")

    # 获取招募历史
    history = AgentRecruiter.get_recruitment_history()
    print(f"  Recruitment history: {len(history)} records")


if __name__ == "__main__":
    print("=== Phase 4 Tests ===\n")
    test_skill_management()
    test_tool_management()
    test_environment_management()
    test_service_management()
    test_agent_recruitment()
    print("\n[OK] All Phase 4 tests completed")
