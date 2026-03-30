"""Skill管理系统"""
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from config import DATETIME_FORMAT, CAPABILITIES_DIR
import json


@dataclass
class Skill:
    """Skill定义"""
    name: str
    description: str
    category: str
    implementation: str
    created_by: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))
    version: str = "1.0.0"
    tags: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self):
        """保存Skill"""
        skills_dir = CAPABILITIES_DIR / "skills"
        skills_dir.mkdir(parents=True, exist_ok=True)

        file_path = skills_dir / f"{self.name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, skill_name: str) -> Optional['Skill']:
        """加载Skill"""
        file_path = CAPABILITIES_DIR / "skills" / f"{skill_name}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return None


class SkillManager:
    """Skill管理器"""

    @staticmethod
    def create_skill(name: str, description: str, category: str, implementation: str, created_by: str, tags: List[str] = None) -> Skill:
        """创建Skill"""
        skill = Skill(
            name=name,
            description=description,
            category=category,
            implementation=implementation,
            created_by=created_by,
            tags=tags or []
        )
        skill.save()
        return skill

    @staticmethod
    def list_skills(category: str = None) -> List[str]:
        """列出Skill"""
        skills_dir = CAPABILITIES_DIR / "skills"
        if not skills_dir.exists():
            return []

        skills = [f.stem for f in skills_dir.glob("*.json")]

        if category:
            filtered = []
            for skill_name in skills:
                skill = Skill.load(skill_name)
                if skill and skill.category == category:
                    filtered.append(skill_name)
            return filtered

        return skills

    @staticmethod
    def get_skill(skill_name: str) -> Optional[Skill]:
        """获取Skill"""
        return Skill.load(skill_name)

    @staticmethod
    def delete_skill(skill_name: str) -> bool:
        """删除Skill"""
        file_path = CAPABILITIES_DIR / "skills" / f"{skill_name}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    @staticmethod
    def get_skills_by_category() -> Dict[str, List[str]]:
        """按分类获取Skill"""
        skills = SkillManager.list_skills()
        by_category = {}

        for skill_name in skills:
            skill = Skill.load(skill_name)
            if skill:
                if skill.category not in by_category:
                    by_category[skill.category] = []
                by_category[skill.category].append(skill_name)

        return by_category
