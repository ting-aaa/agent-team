"""能力库管理"""
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from config import DATETIME_FORMAT
import json
from pathlib import Path
from config import TEAM_DIR


@dataclass
class Skill:
    """技能"""
    name: str
    description: str
    category: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))
    created_by: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class AgentCapability:
    """Agent能力记录"""
    agent_name: str
    skills: List[str] = field(default_factory=list)
    experience_level: int = 0
    projects_completed: int = 0
    knowledge_docs: int = 0
    last_updated: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self):
        """保存能力记录"""
        cap_file = TEAM_DIR / f"{self.agent_name}_capability.json"
        with open(cap_file, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, agent_name: str) -> Optional['AgentCapability']:
        """加载能力记录"""
        cap_file = TEAM_DIR / f"{agent_name}_capability.json"
        if cap_file.exists():
            with open(cap_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return cls(agent_name=agent_name)


class CapabilityManager:
    """能力库管理器"""

    @staticmethod
    def add_skill(agent_name: str, skill_name: str, description: str, category: str):
        """为Agent添加技能"""
        capability = AgentCapability.load(agent_name)
        if skill_name not in capability.skills:
            capability.skills.append(skill_name)
            capability.last_updated = datetime.now().strftime(DATETIME_FORMAT)
            capability.save()

    @staticmethod
    def increment_experience(agent_name: str, amount: int = 1):
        """增加Agent经验值"""
        capability = AgentCapability.load(agent_name)
        capability.experience_level = min(100, capability.experience_level + amount)
        capability.last_updated = datetime.now().strftime(DATETIME_FORMAT)
        capability.save()

    @staticmethod
    def increment_projects(agent_name: str):
        """增加Agent完成的项目数"""
        capability = AgentCapability.load(agent_name)
        capability.projects_completed += 1
        capability.last_updated = datetime.now().strftime(DATETIME_FORMAT)
        capability.save()

    @staticmethod
    def increment_knowledge(agent_name: str):
        """增加Agent知识文档数"""
        capability = AgentCapability.load(agent_name)
        capability.knowledge_docs += 1
        capability.last_updated = datetime.now().strftime(DATETIME_FORMAT)
        capability.save()

    @staticmethod
    def get_capability(agent_name: str) -> AgentCapability:
        """获取Agent能力"""
        return AgentCapability.load(agent_name)

    @staticmethod
    def get_team_capability_summary() -> Dict[str, Any]:
        """获取团队能力总结"""
        team_dir = TEAM_DIR
        capabilities = {}

        for cap_file in team_dir.glob("*_capability.json"):
            with open(cap_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                capabilities[data['agent_name']] = data

        return capabilities
