"""数据存储层"""
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime
from config import PROJECTS_DIR, KNOWLEDGE_DIR, REPORTS_DIR, DATE_FORMAT, DATETIME_FORMAT


class Storage:
    """数据存储管理"""

    @staticmethod
    def save_project_data(project_name: str, data_type: str, data: Dict[str, Any]):
        """保存项目数据"""
        project_dir = PROJECTS_DIR / project_name
        project_dir.mkdir(parents=True, exist_ok=True)

        file_path = project_dir / f"{data_type}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_project_data(project_name: str, data_type: str) -> Optional[Dict[str, Any]]:
        """加载项目数据"""
        file_path = PROJECTS_DIR / project_name / f"{data_type}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    @staticmethod
    def save_knowledge(category: str, doc_name: str, content: str):
        """保存知识文档"""
        category_dir = KNOWLEDGE_DIR / category
        category_dir.mkdir(parents=True, exist_ok=True)

        file_path = category_dir / f"{doc_name}.md"
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

    @staticmethod
    def load_knowledge(category: str, doc_name: str) -> Optional[str]:
        """加载知识文档"""
        file_path = KNOWLEDGE_DIR / category / f"{doc_name}.md"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        return None

    @staticmethod
    def list_knowledge(category: str) -> List[str]:
        """列出知识文档"""
        category_dir = KNOWLEDGE_DIR / category
        if category_dir.exists():
            return [f.stem for f in category_dir.glob("*.md")]
        return []

    @staticmethod
    def save_daily_report(agent_name: str, report_date: str, report: Dict[str, Any]):
        """保存日报"""
        report_dir = REPORTS_DIR / "daily" / agent_name
        report_dir.mkdir(parents=True, exist_ok=True)

        file_path = report_dir / f"{report_date}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

    @staticmethod
    def load_daily_report(agent_name: str, report_date: str) -> Optional[Dict[str, Any]]:
        """加载日报"""
        file_path = REPORTS_DIR / "daily" / agent_name / f"{report_date}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return None

    @staticmethod
    def list_daily_reports(agent_name: str) -> List[str]:
        """列出日报"""
        report_dir = REPORTS_DIR / "daily" / agent_name
        if report_dir.exists():
            return sorted([f.stem for f in report_dir.glob("*.json")], reverse=True)
        return []
