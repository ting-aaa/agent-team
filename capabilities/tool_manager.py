"""工具编写框架"""
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime
from config import DATETIME_FORMAT, CAPABILITIES_DIR
import json


@dataclass
class Tool:
    """工具定义"""
    name: str
    description: str
    tool_type: str
    implementation: str
    created_by: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))
    version: str = "1.0.0"
    dependencies: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self):
        """保存工具"""
        tools_dir = CAPABILITIES_DIR / "tools"
        tools_dir.mkdir(parents=True, exist_ok=True)

        file_path = tools_dir / f"{self.name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, tool_name: str) -> Optional['Tool']:
        """加载工具"""
        file_path = CAPABILITIES_DIR / "tools" / f"{tool_name}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return None


class ToolManager:
    """工具管理器"""

    @staticmethod
    def create_tool(name: str, description: str, tool_type: str, implementation: str, created_by: str, dependencies: List[str] = None) -> Tool:
        """创建工具"""
        tool = Tool(
            name=name,
            description=description,
            tool_type=tool_type,
            implementation=implementation,
            created_by=created_by,
            dependencies=dependencies or []
        )
        tool.save()
        return tool

    @staticmethod
    def list_tools(tool_type: str = None) -> List[str]:
        """列出工具"""
        tools_dir = CAPABILITIES_DIR / "tools"
        if not tools_dir.exists():
            return []

        tools = [f.stem for f in tools_dir.glob("*.json")]

        if tool_type:
            filtered = []
            for tool_name in tools:
                tool = Tool.load(tool_name)
                if tool and tool.tool_type == tool_type:
                    filtered.append(tool_name)
            return filtered

        return tools

    @staticmethod
    def get_tool(tool_name: str) -> Optional[Tool]:
        """获取工具"""
        return Tool.load(tool_name)

    @staticmethod
    def delete_tool(tool_name: str) -> bool:
        """删除工具"""
        file_path = CAPABILITIES_DIR / "tools" / f"{tool_name}.json"
        if file_path.exists():
            file_path.unlink()
            return True
        return False

    @staticmethod
    def get_tools_by_type() -> Dict[str, List[str]]:
        """按类型获取工具"""
        tools = ToolManager.list_tools()
        by_type = {}

        for tool_name in tools:
            tool = Tool.load(tool_name)
            if tool:
                if tool.tool_type not in by_type:
                    by_type[tool.tool_type] = []
                by_type[tool.tool_type].append(tool_name)

        return by_type
