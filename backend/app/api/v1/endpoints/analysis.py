"""
代碼分析 API 端點
"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import tempfile
import subprocess
import shutil
import os
from typing import Optional
from structlog import get_logger

from app.services.analysis_service import CodeAnalysisService

router = APIRouter()
logger = get_logger()

class AnalysisRequest(BaseModel):
    repo_url: str
    branch: Optional[str] = "main"

def clone_repo(repo_url: str, branch: str = "main") -> str:
    """克隆倉庫到臨時目錄"""
    tmp_dir = tempfile.mkdtemp()
    try:
        subprocess.run([
            "git", "clone", "--depth", "1", "--branch", branch, repo_url, tmp_dir
        ], check=True, capture_output=True, text=True)
        return tmp_dir
    except subprocess.CalledProcessError as e:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise HTTPException(status_code=400, detail=f"Failed to clone repository: {e.stderr}")

@router.post("/analyze")
async def analyze_repository(request: AnalysisRequest):
    """手動分析 GitHub 倉庫"""
    logger.info("Starting manual analysis", repo_url=request.repo_url, branch=request.branch)
    
    code_dir = None
    try:
        # 克隆倉庫
        code_dir = clone_repo(request.repo_url, request.branch)
        logger.info("Repository cloned successfully", path=code_dir)
        
        # 執行分析
        analysis_service = CodeAnalysisService()
        results = analysis_service.analyze_code(code_dir)
        
        logger.info("Analysis completed", 
                   repo_url=request.repo_url, 
                   score=results.get("score"),
                   errors_count=len(results.get("static_analysis", {}).get("errors", [])),
                   warnings_count=len(results.get("static_analysis", {}).get("warnings", [])))
        
        return {
            "success": True,
            "repo_url": request.repo_url,
            "branch": request.branch,
            "results": results
        }
        
    except Exception as e:
        logger.error("Analysis failed", repo_url=request.repo_url, error=str(e))
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")
    finally:
        if code_dir and os.path.exists(code_dir):
            shutil.rmtree(code_dir, ignore_errors=True)

@router.get("/health")
async def health_check():
    """健康檢查端點"""
    return {"status": "healthy", "service": "code-analysis"} 