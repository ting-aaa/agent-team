"""环境搭建和服务搭建"""
from dataclasses import dataclass, asdict, field
from typing import Dict, List, Any, Optional
from datetime import datetime
from config import DATETIME_FORMAT, CAPABILITIES_DIR
import json


@dataclass
class Environment:
    """环境配置"""
    name: str
    description: str
    components: List[str]
    setup_script: str
    created_by: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self):
        """保存环境配置"""
        env_dir = CAPABILITIES_DIR / "environments"
        env_dir.mkdir(parents=True, exist_ok=True)

        file_path = env_dir / f"{self.name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, env_name: str) -> Optional['Environment']:
        """加载环境配置"""
        file_path = CAPABILITIES_DIR / "environments" / f"{env_name}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return None


@dataclass
class Service:
    """服务配置"""
    name: str
    description: str
    service_type: str
    deployment_config: Dict[str, Any]
    created_by: str
    created_at: str = field(default_factory=lambda: datetime.now().strftime(DATETIME_FORMAT))
    version: str = "1.0.0"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def save(self):
        """保存服务配置"""
        svc_dir = CAPABILITIES_DIR / "services"
        svc_dir.mkdir(parents=True, exist_ok=True)

        file_path = svc_dir / f"{self.name}.json"
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, service_name: str) -> Optional['Service']:
        """加载服务配置"""
        file_path = CAPABILITIES_DIR / "services" / f"{service_name}.json"
        if file_path.exists():
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return cls(**data)
        return None


class EnvironmentManager:
    """环境管理器"""

    @staticmethod
    def create_environment(name: str, description: str, components: List[str], setup_script: str, created_by: str) -> Environment:
        """创建环境"""
        env = Environment(
            name=name,
            description=description,
            components=components,
            setup_script=setup_script,
            created_by=created_by
        )
        env.save()
        return env

    @staticmethod
    def list_environments() -> List[str]:
        """列出环境"""
        env_dir = CAPABILITIES_DIR / "environments"
        if not env_dir.exists():
            return []
        return [f.stem for f in env_dir.glob("*.json")]

    @staticmethod
    def get_environment(env_name: str) -> Optional[Environment]:
        """获取环境"""
        return Environment.load(env_name)


class ServiceManager:
    """服务管理器"""

    @staticmethod
    def create_service(name: str, description: str, service_type: str, deployment_config: Dict[str, Any], created_by: str) -> Service:
        """创建服务"""
        service = Service(
            name=name,
            description=description,
            service_type=service_type,
            deployment_config=deployment_config,
            created_by=created_by
        )
        service.save()
        return service

    @staticmethod
    def list_services(service_type: str = None) -> List[str]:
        """列出服务"""
        svc_dir = CAPABILITIES_DIR / "services"
        if not svc_dir.exists():
            return []

        services = [f.stem for f in svc_dir.glob("*.json")]

        if service_type:
            filtered = []
            for svc_name in services:
                svc = Service.load(svc_name)
                if svc and svc.service_type == service_type:
                    filtered.append(svc_name)
            return filtered

        return services

    @staticmethod
    def get_service(service_name: str) -> Optional[Service]:
        """获取服务"""
        return Service.load(service_name)
