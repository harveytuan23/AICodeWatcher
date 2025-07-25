"""
GitHub API 服務：處理 PR 評論、狀態更新等操作
"""
import os
import requests
import json
from typing import Optional, List, Dict, Any
from structlog import get_logger

logger = get_logger()

class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv("GITHUB_TOKEN")
        self.base_url = "https://api.github.com"
        
        # 調試信息
        logger.info("GitHubService initialized", 
                   token_length=len(self.token) if self.token else 0,
                   token_prefix=self.token[:10] if self.token else "None")
        
        self.headers = {
            "Authorization": f"token {self.token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CodeWatcher-AI-Review"
        } if self.token else {
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CodeWatcher-AI-Review"
        }
    
    def create_pr_comment(self, repo: str, pr_number: int, body: str) -> Dict[str, Any]:
        """在 PR 上創建評論"""
        url = f"{self.base_url}/repos/{repo}/issues/{pr_number}/comments"
        data = {"body": body}
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            logger.info("PR comment created", repo=repo, pr_number=pr_number)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to create PR comment", 
                        repo=repo, pr_number=pr_number, error=str(e))
            raise
    
    def create_review_comment(self, repo: str, pr_number: int, commit_sha: str, 
                            path: str, line: int, body: str) -> Dict[str, Any]:
        """在 PR 的特定行創建評論"""
        url = f"{self.base_url}/repos/{repo}/pulls/{pr_number}/comments"
        data = {
            "commit_id": commit_sha,
            "path": path,
            "line": line,
            "body": body,
            "position": 1  # 添加 position 參數
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            logger.info("Review comment created", repo=repo, pr_number=pr_number, path=path, line=line)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to create review comment", 
                        repo=repo, pr_number=pr_number, error=str(e))
            raise
    
    def update_pr_status(self, repo: str, sha: str, state: str, 
                        description: str, context: str = "CodeWatcher AI Review") -> Dict[str, Any]:
        """更新 PR 狀態"""
        url = f"{self.base_url}/repos/{repo}/statuses/{sha}"
        data = {
            "state": state,  # "pending", "success", "failure", "error"
            "description": description,
            "context": context
        }
        
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            logger.info("PR status updated", repo=repo, sha=sha, state=state)
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to update PR status", 
                        repo=repo, sha=sha, error=str(e))
            raise
    
    def get_pr_files(self, repo: str, pr_number: int) -> List[Dict[str, Any]]:
        """獲取 PR 中的文件列表"""
        url = f"{self.base_url}/repos/{repo}/pulls/{pr_number}/files"
        
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error("Failed to get PR files", 
                        repo=repo, pr_number=pr_number, error=str(e))
            raise
    
    def format_analysis_report(self, analysis_results: Dict[str, Any]) -> str:
        """格式化分析報告為 Markdown"""
        report = "# 🤖 CodeWatcher AI Review Report\n\n"
        
        # Overall Score
        if "score" in analysis_results:
            score = analysis_results["score"]
            if score >= 90:
                report += f"## ✅ Excellent ({score}/100)\n\n"
            elif score >= 70:
                report += f"## ⚠️ Good ({score}/100)\n\n"
            else:
                report += f"## ❌ Needs Improvement ({score}/100)\n\n"
        
        # Static Analysis Results
        if "static_analysis" in analysis_results:
            static = analysis_results["static_analysis"]
            report += "## 🔍 Static Analysis Results\n\n"
            
            if static.get("errors"):
                report += "### ❌ Errors\n"
                for error in static["errors"]:
                    report += f"- **{error['file']}:{error['line']}** - {error['message']}\n"
                report += "\n"
            
            if static.get("warnings"):
                report += "### ⚠️ Warnings\n"
                for warning in static["warnings"]:
                    report += f"- **{warning['file']}:{warning['line']}** - {warning['message']}\n"
                report += "\n"
            
            if not static.get("errors") and not static.get("warnings"):
                report += "✅ No static analysis issues found\n\n"
        
        # Security Check
        if "security" in analysis_results:
            security = analysis_results["security"]
            report += "## 🔒 Security Check\n\n"
            
            if security.get("vulnerabilities"):
                report += "### 🚨 Vulnerabilities\n"
                for vuln in security["vulnerabilities"]:
                    report += f"- **{vuln['severity']}** - {vuln['description']}\n"
                report += "\n"
            else:
                report += "✅ No security vulnerabilities found\n\n"
        
        # Suggestions for Improvement
        if "suggestions" in analysis_results:
            suggestions = analysis_results["suggestions"]
            if suggestions:
                report += "## 💡 Suggestions for Improvement\n\n"
                for suggestion in suggestions:
                    report += f"- {suggestion}\n"
                report += "\n"
        
        report += "---\n*This report is automatically generated by CodeWatcher AI*"
        return report 