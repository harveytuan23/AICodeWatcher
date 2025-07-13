"""
CodeWatcher Backend API
AI程式碼審查與可靠性平台後端服務
"""
from dotenv import load_dotenv
load_dotenv()

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.api.v1.api import api_router
from app.core.logging import setup_logging

# 設置日誌
setup_logging()

# 創建FastAPI應用
app = FastAPI(
    title="CodeWatcher API",
    description="AI程式碼審查與可靠性平台API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# 添加CORS中間件
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 添加可信主機中間件
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# 包含API路由
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """根端點"""
    return {
        "message": "Welcome to CodeWatcher API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    ) 