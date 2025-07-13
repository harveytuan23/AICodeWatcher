"""
API路由配置
"""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, projects, reviews, analysis, webhooks

api_router = APIRouter()

# 包含各個端點路由
api_router.include_router(auth.router, prefix="/auth", tags=["認證"])
api_router.include_router(projects.router, prefix="/projects", tags=["專案"])
api_router.include_router(reviews.router, prefix="/reviews", tags=["審查"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["分析"])
api_router.include_router(webhooks.router, prefix="/webhooks", tags=["Webhook"]) 