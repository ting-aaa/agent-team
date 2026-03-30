"""日报系统"""
from dataclasses import dataclass, asdict, field
from typing import Dict, Any, List, Optional
from datetime import datetime
from config import DATE_FORMAT, DATETIME_FORMAT
from storage.storage import Storage


@dataclass
class DailyReport:
    """日报"""
    agent_name: str
    report_date: str
    completed_tasks: List[str] = field(default_factory=list)
    issues: List[str] = field(default_factory=list)
    tomorrow_plan: List[str] = field(default_factory=list)
    new_knowledge: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))

    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'DailyReport':
        """从字典创建"""
        return cls(**data)

    def save(self):
        """保存日报"""
        Storage.save_daily_report(self.agent_name, self.report_date, self.to_dict())

    @classmethod
    def load(cls, agent_name: str, report_date: str) -> Optional['DailyReport']:
        """加载日报"""
        data = Storage.load_daily_report(agent_name, report_date)
        if data:
            return cls.from_dict(data)
        return None

    def add_completed_task(self, task: str):
        """添加完成的任务"""
        self.completed_tasks.append(task)

    def add_issue(self, issue: str):
        """添加问题"""
        self.issues.append(issue)

    def add_tomorrow_plan(self, plan: str):
        """添加明日计划"""
        self.tomorrow_plan.append(plan)

    def add_knowledge(self, knowledge: str):
        """添加新增知识"""
        self.new_knowledge.append(knowledge)

    def __str__(self) -> str:
        """字符串表示"""
        lines = [
            f"=== {self.agent_name} Daily Report ({self.report_date}) ===",
            "",
            "[COMPLETED TASKS]",
        ]
        for task in self.completed_tasks:
            lines.append(f"  - {task}")

        if self.issues:
            lines.append("\n[ISSUES]")
            for issue in self.issues:
                lines.append(f"  - {issue}")

        if self.tomorrow_plan:
            lines.append("\n[TOMORROW PLAN]")
            for plan in self.tomorrow_plan:
                lines.append(f"  - {plan}")

        if self.new_knowledge:
            lines.append("\n[NEW KNOWLEDGE]")
            for knowledge in self.new_knowledge:
                lines.append(f"  - {knowledge}")

        return "\n".join(lines)
