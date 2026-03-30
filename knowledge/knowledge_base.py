"""知识库管理"""
from typing import Dict, List, Optional
from storage.storage import Storage


class KnowledgeBase:
    """知识库管理"""

    CATEGORIES = {
        "technical": "技术文档、学习资料",
        "projects": "项目文档、架构设计",
        "experience": "经验总结、最佳实践",
        "api": "API文档",
    }

    @staticmethod
    def add_technical_doc(doc_name: str, content: str):
        """添加技术文档"""
        Storage.save_knowledge("technical", doc_name, content)

    @staticmethod
    def add_project_doc(doc_name: str, content: str):
        """添加项目文档"""
        Storage.save_knowledge("projects", doc_name, content)

    @staticmethod
    def add_experience(doc_name: str, content: str):
        """添加经验总结"""
        Storage.save_knowledge("experience", doc_name, content)

    @staticmethod
    def add_api_doc(doc_name: str, content: str):
        """添加API文档"""
        Storage.save_knowledge("api", doc_name, content)

    @staticmethod
    def get_doc(category: str, doc_name: str) -> Optional[str]:
        """获取文档"""
        return Storage.load_knowledge(category, doc_name)

    @staticmethod
    def list_docs(category: str) -> List[str]:
        """列出分类下的文档"""
        return Storage.list_knowledge(category)

    @staticmethod
    def list_all_categories() -> Dict[str, str]:
        """列出所有分类"""
        return KnowledgeBase.CATEGORIES
