"""Agent基类和角色定义"""
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional
from datetime import datetime
import json
from pathlib import Path
from config import TEAM_DIR, DATE_FORMAT, DATETIME_FORMAT


class AgentRole(Enum):
    """Agent角色枚举"""
    PRODUCER = "producer"
    DESIGNER = "designer"
    PROGRAMMER = "programmer"
    ARTIST = "artist"
    DEVOPS = "devops"


class WorkflowState(Enum):
    """工作流状态"""
    IDLE = "idle"
    BLUEPRINT = "blueprint"
    DESIGN = "design"
    DESIGN_REVIEW = "design_review"
    PRESENTATION = "presentation"
    DESIGN_ADJUST = "design_adjust"
    DESIGN_CONFIRM = "design_confirm"
    REQUIREMENT_ANALYSIS = "requirement_analysis"
    ENVIRONMENT_SETUP = "environment_setup"
    DEVELOPMENT = "development"
    RESOURCE_CREATION = "resource_creation"
    DEPLOYMENT = "deployment"
    COMPLETED = "completed"


@dataclass
class Agent:
    """Agent基类"""
    name: str
    role: AgentRole
    skills: List[str] = field(default_factory=list)
    experience_level: int = 0  # 0-100
    knowledge_base: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['role'] = self.role.value
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Agent':
        """从字典创建Agent"""
        data['role'] = AgentRole(data['role'])
        return cls(**data)

    def save(self):
        """保存Agent配置"""
        agent_file = TEAM_DIR / f"{self.role.value}_{self.name}.json"
        with open(agent_file, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, role: AgentRole, name: str) -> Optional['Agent']:
        """加载Agent配置"""
        agent_file = TEAM_DIR / f"{role.value}_{name}.json"
        if agent_file.exists():
            with open(agent_file, 'r', encoding='utf-8') as f:
                return cls.from_dict(json.load(f))
        return None


class Producer(Agent):
    """制作人"""
    def __init__(self, name: str = "Producer"):
        super().__init__(name=name, role=AgentRole.PRODUCER)


class Designer(Agent):
    """策划"""
    def __init__(self, name: str = "Designer"):
        super().__init__(name=name, role=AgentRole.DESIGNER)


class Programmer(Agent):
    """程序员"""
    def __init__(self, name: str = "Programmer"):
        super().__init__(name=name, role=AgentRole.PROGRAMMER)


class Artist(Agent):
    """美术"""
    def __init__(self, name: str = "Artist"):
        super().__init__(name=name, role=AgentRole.ARTIST)


class DevOps(Agent):
    """运维"""
    def __init__(self, name: str = "DevOps"):
        super().__init__(name=name, role=AgentRole.DEVOPS)
