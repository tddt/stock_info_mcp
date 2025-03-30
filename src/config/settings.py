import logging
from typing import Literal
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """应用配置类"""
    # 服务配置
    SERVICE_NAME: str = "stock-info"
    TRANSPORT: Literal["stdio", "http"] = "stdio"
    HTTP_PORT: int = 8080
    
    # 日志配置
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = "stock-info.log"
    
    # 数据配置
    DEFAULT_PAGE_SIZE: int = 10
    DEFAULT_HISTORY_DAYS: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True

# 全局配置实例
settings = Settings()

def configure_logging() -> None:
    """配置日志"""
    logging.basicConfig(
        level=getattr(logging, settings.LOG_LEVEL),
        format=settings.LOG_FORMAT,
        filename=settings.LOG_FILE
    )
