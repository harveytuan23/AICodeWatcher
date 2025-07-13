"""
應用配置管理
"""

from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator


class Settings(BaseSettings):
    """應用設置"""
    
    # 基本設置
    PROJECT_NAME: str = "CodeWatcher"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # 服務器設置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    DEBUG: bool = False
    
    # 安全設置
    SECRET_KEY: str = "codewatcher-super-secret-key-20240608-abcdefg1234567890"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # 數據庫設置
    DATABASE_URL: str = "postgresql://user:password@localhost/codewatcher"
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # CORS設置
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 第三方服務設置
    OPENAI_API_KEY: Optional[str] = None
    GITHUB_TOKEN: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITLAB_CLIENT_ID: Optional[str] = None
    GITLAB_CLIENT_SECRET: Optional[str] = None
    
    # 文件存儲設置
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    
    # 日誌設置
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    # 監控設置
    SENTRY_DSN: Optional[str] = None
    PROMETHEUS_ENABLED: bool = True
    
    # AI/ML設置
    MODEL_CACHE_DIR: str = "./models"
    MAX_TOKENS: int = 4000
    TEMPERATURE: float = 0.1
    
    # 任務隊列設置
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError("SECRET_KEY must be at least 32 characters long")
        return v
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v.startswith(("postgresql://", "sqlite://")):
            raise ValueError("DATABASE_URL must be a valid PostgreSQL or SQLite URL")
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# 創建全局設置實例
settings = Settings() 