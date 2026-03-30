"""Agent成长记录系统"""
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from config import DATETIME_FORMAT, REPORTS_DIR
import json


@dataclass
class GrowthRecord:
    """成长记录"""
    agent_name: str
    record_date: str
    milestone: str
    description: str
    skills_gained: List[str] = field(default_factory=list)
    experience_gained: int = 0
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self):
        """保存成长记录"""
        growth_dir = REPORTS_DIR / "growth" / self.agent_name
        growth_dir.mkdir(parents=True, exist_ok=True)

        file_path = growth_dir / f"{self.record_date}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, agent_name: str, record_date: str) -> Optional['GrowthRecord']:
        """加载成长记录"""
        file_path = REPORTS_DIR / "growth" / agent_name / f"{record_date}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return None

    @classmethod
    def list_records(cls, agent_name: str) -> List[str]:
        """列出成长记录"""
        growth_dir = REPORTS_DIR / "growth" / agent_name
        if growth_dir.exists():
            return sorted([f.stem for f in growth_dir.glob("*.json")], reverse=True)
        return []


class GrowthTracker:
    """成长追踪器"""

    @staticmethod
    def record_milestone(agent_name: str, milestone: str, description: str, skills_gained: List[str] = None, experience_gained: int = 0):
        """记录里程碑"""
        record_date = datetime.now().strftime("%Y-%m-%d")
        record = GrowthRecord(
            agent_name=agent_name,
            record_date=record_date,
            milestone=milestone,
            description=description,
            skills_gained=skills_gained or [],
            experience_gained=experience_gained,
        )
        record.save()

    @staticmethod
    def get_agent_growth_history(agent_name: str) -> List[Dict[str, Any]]:
        """获取Agent成长历史"""
        records = GrowthRecord.list_records(agent_name)
        history = []

        for record_date in records:
            record = GrowthRecord.load(agent_name, record_date)
            if record:
                history.append(record.to_dict())

        return history

    @staticmethod
    def get_team_growth_summary() -> Dict[str, Any]:
        """获取团队成长总结"""
        growth_dir = REPORTS_DIR / "growth"
        summary = {}

        if growth_dir.exists():
            for agent_dir in growth_dir.iterdir():
                if agent_dir.is_dir():
                    agent_name = agent_dir.name
                    records = GrowthRecord.list_records(agent_name)
                    summary[agent_name] = {
                        "total_milestones": len(records),
                        "latest_milestone": records[0] if records else None,
                    }

        return summary
