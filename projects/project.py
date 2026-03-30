"""项目管理"""
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, Optional, List
from datetime import datetime
from enum import Enum
import json
from config import PROJECTS_DIR, DATE_FORMAT, DATETIME_FORMAT
from storage.storage import Storage


class ProjectStatus(Enum):
    """项目状态"""
    PLANNING = "planning"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


@dataclass
class Task:
    """任务"""
    name: str
    description: str
    assigned_to: str  # Agent名称
    status: str = "pending"  # pending, in_progress, completed
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))
    completed_at: Optional[str] = None
    subtasks: List['Task'] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['subtasks'] = [st.to_dict() for st in self.subtasks]
        return data

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """从字典创建"""
        subtasks = [cls.from_dict(st) for st in data.pop('subtasks', [])]
        task = cls(**data)
        task.subtasks = subtasks
        return task


@dataclass
class Project:
    """项目"""
    name: str
    description: str
    status: ProjectStatus = ProjectStatus.PLANNING
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))
    blueprint: Optional[Dict[str, Any]] = None
    design_proposal: Optional[Dict[str, Any]] = None
    requirements: Optional[Dict[str, Any]] = None
    tasks: List[Task] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        data = asdict(self)
        data['status'] = self.status.value
        data['tasks'] = [t.to_dict() for t in self.tasks]
        return data

    def save(self):
        """保存项目"""
        project_dir = PROJECTS_DIR / self.name
        project_dir.mkdir(parents=True, exist_ok=True)

        # 保存项目元数据
        meta_file = project_dir / "project.json"
        with open(meta_file, 'w', encoding='utf-8') as f:
            json.dump({
                'name': self.name,
                'description': self.description,
                'status': self.status.value,
                'created_at': self.created_at,
            }, f, ensure_ascii=False, indent=2)

        # 保存任务
        if self.tasks:
            tasks_file = project_dir / "tasks.json"
            with open(tasks_file, 'w', encoding='utf-8') as f:
                json.dump([t.to_dict() for t in self.tasks], f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, project_name: str) -> Optional['Project']:
        """加载项目"""
        meta_file = PROJECTS_DIR / project_name / "project.json"
        if not meta_file.exists():
            return None

        with open(meta_file, 'r', encoding='utf-8') as f:
            data = json.load(f)

        project = cls(
            name=data['name'],
            description=data['description'],
            status=ProjectStatus(data['status']),
            created_at=data['created_at'],
        )

        # 加载任务
        tasks_file = PROJECTS_DIR / project_name / "tasks.json"
        if tasks_file.exists():
            with open(tasks_file, 'r', encoding='utf-8') as f:
                tasks_data = json.load(f)
                project.tasks = [Task.from_dict(t) for t in tasks_data]

        return project

    def add_task(self, task: Task):
        """添加任务"""
        self.tasks.append(task)

    def get_task(self, task_name: str) -> Optional[Task]:
        """获取任务"""
        for task in self.tasks:
            if task.name == task_name:
                return task
        return None
