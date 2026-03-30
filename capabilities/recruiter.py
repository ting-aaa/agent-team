"""Agent招募和初始化系统"""
from typing import Dict, List, Any, Optional
from agents.roles import Agent, AgentRole
from knowledge.capability import AgentCapability
import json
from config import TEAM_DIR
from datetime import datetime
from config import DATETIME_FORMAT


class AgentRecruiter:
    """Agent招募器"""

    @staticmethod
    def recruit_agent(name: str, role: AgentRole, skills: List[str] = None, description: str = "") -> Agent:
        """招募新Agent"""
        agent = Agent(
            name=name,
            role=role,
            skills=skills or [],
        )
        agent.save()

        # 初始化能力记录
        capability = AgentCapability(agent_name=name)
        capability.skills = skills or []
        capability.save()

        # 记录招募信息
        recruitment_file = TEAM_DIR / "recruitment_log.json"
        recruitment_log = []

        if recruitment_file.exists():
            with open(recruitment_file, 'r', encoding='utf-8') as f:
                recruitment_log = json.load(f)

        recruitment_log.append({
            "agent_name": name,
            "role": role.value,
            "recruited_at": datetime.now().strftime(DATETIME_FORMAT),
            "initial_skills": skills or [],
            "description": description,
        })

        with open(recruitment_file, 'w', encoding='utf-8') as f:
            json.dump(recruitment_log, f, ensure_ascii=False, indent=2)

        return agent

    @staticmethod
    def get_recruitment_history() -> List[Dict[str, Any]]:
        """获取招募历史"""
        recruitment_file = TEAM_DIR / "recruitment_log.json"
        if recruitment_file.exists():
            with open(recruitment_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    @staticmethod
    def list_team_members() -> List[Dict[str, Any]]:
        """列出团队成员"""
        team_members = []
        for agent_file in TEAM_DIR.glob("*.json"):
            if agent_file.name != "recruitment_log.json" and not agent_file.name.endswith("_capability.json"):
                with open(agent_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    team_members.append(data)
        return team_members

    @staticmethod
    def get_team_size() -> int:
        """获取团队规模"""
        return len(AgentRecruiter.list_team_members())

    @staticmethod
    def get_team_composition() -> Dict[str, int]:
        """获取团队组成"""
        members = AgentRecruiter.list_team_members()
        composition = {}

        for member in members:
            role = member.get('role', 'unknown')
            composition[role] = composition.get(role, 0) + 1

        return composition
