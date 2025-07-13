"""
專案管理API端點
"""

from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_projects():
    """獲取專案列表"""
    # 假資料
    projects = [
        {"id": 1, "name": "AI審查平台", "created_at": "2024-07-10"},
        {"id": 2, "name": "CodeWatcher", "created_at": "2024-07-09"},
    ]
    return {"total": len(projects), "projects": projects}

@router.post("/")
async def create_project():
    """創建新專案"""
    # TODO: 實現創建專案邏輯
    return {"message": "創建專案功能開發中"}

@router.get("/{project_id}")
async def get_project(project_id: str):
    """獲取專案詳情"""
    # TODO: 實現專案詳情邏輯
    return {"message": f"專案 {project_id} 詳情功能開發中"} 