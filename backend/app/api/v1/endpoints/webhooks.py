"""
Webhook 端點：接收 GitHub/GitLab PR 事件，並自動拉取 PR 代碼進行分析
"""
from fastapi import APIRouter, Request, Header
from starlette.responses import JSONResponse
import subprocess
import tempfile
import shutil
import os
from structlog import get_logger

from app.services.github_service import GitHubService
from app.services.analysis_service import CodeAnalysisService

router = APIRouter()
logger = get_logger()

def clone_pr_repo(clone_url, branch, sha):
    tmp_dir = tempfile.mkdtemp()
    try:
        subprocess.run([
            "git", "clone", "--depth", "1", "--branch", branch, clone_url, tmp_dir
        ], check=True)
        # checkout 到指定 commit（可選）
        subprocess.run(["git", "checkout", sha], cwd=tmp_dir, check=True)
        return tmp_dir
    except Exception as e:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise e

@router.post("/github")
async def github_webhook(
    request: Request,
    x_github_event: str = Header(None),
    x_hub_signature_256: str = Header(None)
):
    """接收 GitHub PR webhook 事件，並自動分析 PR 代碼"""
    payload = await request.json()
    
    if x_github_event != "pull_request":
        return JSONResponse({"msg": "Not a pull_request event, ignored."}, status_code=200)
    
    action = payload.get("action")
    if action not in ["opened", "synchronize", "reopened"]:
        return JSONResponse({"msg": f"PR action {action} ignored."}, status_code=200)
    
    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    clone_url = repo.get("clone_url")
    pr_branch = pr.get("head", {}).get("ref")
    pr_sha = pr.get("head", {}).get("sha")
    pr_title = pr.get("title")
    pr_number = pr.get("number")
    repo_name = repo.get("full_name")
    
    logger.info("Processing PR webhook", 
                action=action, pr_title=pr_title, repo=repo_name, pr_number=pr_number)
    
    # 初始化服務
    github_service = GitHubService()
    analysis_service = CodeAnalysisService()
    
    try:
        # 克隆代碼
        code_dir = clone_pr_repo(clone_url, pr_branch, pr_sha)
        logger.info("Code cloned successfully", path=code_dir)
        
        # 執行代碼分析
        analysis_results = analysis_service.analyze_code(code_dir)
        logger.info("Code analysis completed", score=analysis_results.get("score"))
        
        # 更新 PR 狀態
        try:
            if analysis_results.get("score", 100) >= 70:
                status = "success"
                description = f"代碼質量評分: {analysis_results.get('score')}/100"
            else:
                status = "failure"
                description = f"代碼質量評分: {analysis_results.get('score')}/100 - 需要改進"
            
            github_service.update_pr_status(repo_name, pr_sha, status, description)
        except Exception as e:
            logger.warning("Failed to update PR status", error=str(e))
        
        # 生成並發布分析報告
        try:
            report = github_service.format_analysis_report(analysis_results)
            github_service.create_pr_comment(repo_name, pr_number, report)
            logger.info("Analysis report posted to PR", pr_number=pr_number)
        except Exception as e:
            logger.error("Failed to post analysis report", error=str(e))
        
        # 如果有具體的錯誤，在總評論中列出
        static_analysis = analysis_results.get("static_analysis", {})
        errors = static_analysis.get("errors", [])
        
        # 暫時跳過行級評論，因為需要更複雜的 diff 處理
        # 錯誤信息已經包含在總評論報告中
        
        return {
            "msg": "PR analyzed successfully",
            "pr_title": pr_title,
            "repo": repo_name,
            "score": analysis_results.get("score"),
            "errors_count": len(errors),
            "warnings_count": len(static_analysis.get("warnings", []))
        }
        
    except Exception as e:
        logger.error("Failed to analyze PR", error=str(e))
        return JSONResponse({"msg": "Failed to analyze PR", "error": str(e)}, status_code=500)
    finally:
        if 'code_dir' in locals() and os.path.exists(code_dir):
            shutil.rmtree(code_dir, ignore_errors=True) 