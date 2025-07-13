"""
日誌配置
"""

import logging
import sys
from typing import Any, Dict

import structlog
from structlog.stdlib import LoggerFactory

from app.core.config import settings


def setup_logging() -> None:
    """設置應用日誌"""
    
    # 配置structlog
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    
    # 設置根日誌級別
    logging.basicConfig(
        format=settings.LOG_FORMAT,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
        stream=sys.stdout
    )
    
    # 設置第三方庫日誌級別
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("uvicorn.access").setLevel(logging.INFO)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)
    logging.getLogger("celery").setLevel(logging.INFO)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """獲取結構化日誌記錄器"""
    return structlog.get_logger(name)


# 創建默認日誌記錄器
logger = get_logger(__name__) 