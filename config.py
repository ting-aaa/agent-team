"""系统配置"""
import os
from pathlib import Path

# 项目根目录
PROJECT_ROOT = Path(__file__).parent

# 数据目录
DATA_DIR = PROJECT_ROOT / "data"
TEAM_DIR = DATA_DIR / "team"
PROJECTS_DIR = DATA_DIR / "projects"
KNOWLEDGE_DIR = DATA_DIR / "knowledge"
REPORTS_DIR = DATA_DIR / "reports"
CAPABILITIES_DIR = DATA_DIR / "capabilities"

# 创建必要目录
for directory in [DATA_DIR, TEAM_DIR, PROJECTS_DIR, KNOWLEDGE_DIR, REPORTS_DIR, CAPABILITIES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Claude API配置
CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "[REDACTED]"

# 日期格式
DATE_FORMAT = "%Y-%m-%d"
DATETIME_FORMAT = "%Y-%m-%d %H:%M:%S"
