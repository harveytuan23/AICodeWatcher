"""
認證相關API端點
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter()

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """用戶登入"""
    # TODO: 實現登入邏輯
    return {"message": "登入功能開發中"}

@router.post("/register")
async def register():
    """用戶註冊"""
    # TODO: 實現註冊邏輯
    return {"message": "註冊功能開發中"}

@router.post("/logout")
async def logout():
    """用戶登出"""
    # TODO: 實現登出邏輯
    return {"message": "登出功能開發中"} 