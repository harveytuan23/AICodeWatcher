"""
代碼分析服務：整合各種代碼分析工具
"""
import subprocess
import re
import os
from typing import Dict, List, Any, Optional
from structlog import get_logger

logger = get_logger()

class CodeAnalysisService:
    def __init__(self):
        self.logger = logger
    
    def analyze_code(self, code_path: str) -> Dict[str, Any]:
        """執行完整的代碼分析"""
        results = {
            "score": 100,  # 初始滿分
            "static_analysis": {},
            "security": {},
            "suggestions": []
        }
        
        # 靜態分析
        static_results = self.run_static_analysis(code_path)
        results["static_analysis"] = static_results
        
        # 安全檢查
        security_results = self.run_security_scan(code_path)
        results["security"] = security_results
        
        # 計算評分
        results["score"] = self.calculate_score(results)
        
        # 生成建議
        results["suggestions"] = self.generate_suggestions(results)
        
        return results
    
    def run_static_analysis(self, code_path: str) -> Dict[str, Any]:
        """執行靜態代碼分析"""
        results = {
            "errors": [],
            "warnings": [],
            "info": []
        }
        
        # 使用 flake8 進行 Python 代碼分析
        if self._has_python_files(code_path):
            flake8_results = self._run_flake8(code_path)
            results["errors"].extend(flake8_results["errors"])
            results["warnings"].extend(flake8_results["warnings"])
        
        # 使用 eslint 進行 JavaScript 代碼分析（如果可用）
        if self._has_js_files(code_path):
            eslint_results = self._run_eslint(code_path)
            results["errors"].extend(eslint_results["errors"])
            results["warnings"].extend(eslint_results["warnings"])
        
        return results
    
    def run_security_scan(self, code_path: str) -> Dict[str, Any]:
        """執行安全掃描"""
        results = {
            "vulnerabilities": [],
            "secrets": [],
            "dependencies": {}
        }
        
        # 檢查硬編碼的密鑰和密碼
        secrets = self._scan_for_secrets(code_path)
        results["secrets"] = secrets
        
        # 檢查依賴項安全問題
        if self._has_python_files(code_path):
            deps = self._check_python_dependencies(code_path)
            results["dependencies"] = deps
        
        return results
    
    def _has_python_files(self, code_path: str) -> bool:
        """檢查是否包含 Python 文件"""
        for root, dirs, files in os.walk(code_path):
            for file in files:
                if file.endswith('.py'):
                    return True
        return False
    
    def _has_js_files(self, code_path: str) -> bool:
        """檢查是否包含 JavaScript 文件"""
        for root, dirs, files in os.walk(code_path):
            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    return True
        return False
    
    def _run_flake8(self, code_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """運行 flake8 靜態分析"""
        results = {"errors": [], "warnings": []}
        
        try:
            cmd = ["flake8", code_path, "--format=%(path)s:%(row)d:%(col)d:%(code)s:%(text)s"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        parts = line.split(':', 4)
                        if len(parts) >= 5:
                            file_path, line_num, col_num, code, message = parts
                            issue = {
                                "file": os.path.relpath(file_path, code_path),
                                "line": int(line_num),
                                "column": int(col_num),
                                "code": code,
                                "message": message
                            }
                            
                            # 根據錯誤代碼分類
                            if code.startswith('E'):  # 錯誤
                                results["errors"].append(issue)
                            elif code.startswith('W'):  # 警告
                                results["warnings"].append(issue)
                            else:  # 其他
                                results["warnings"].append(issue)
        
        except subprocess.TimeoutExpired:
            self.logger.warning("Flake8 analysis timed out", path=code_path)
        except Exception as e:
            self.logger.error("Flake8 analysis failed", path=code_path, error=str(e))
        
        return results
    
    def _run_eslint(self, code_path: str) -> Dict[str, List[Dict[str, Any]]]:
        """運行 ESLint 靜態分析（如果可用）"""
        results = {"errors": [], "warnings": []}
        
        # 檢查是否有 ESLint 配置
        eslint_configs = ['.eslintrc.js', '.eslintrc.json', '.eslintrc.yml', '.eslintrc.yaml']
        has_config = any(os.path.exists(os.path.join(code_path, config)) for config in eslint_configs)
        
        if not has_config:
            return results
        
        try:
            cmd = ["npx", "eslint", code_path, "--format=compact"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.stdout:
                # 解析 ESLint 輸出
                for line in result.stdout.strip().split('\n'):
                    if line and ':' in line:
                        # 簡單的解析，實際可能需要更複雜的處理
                        parts = line.split(':')
                        if len(parts) >= 3:
                            file_path = parts[0]
                            line_num = parts[1]
                            message = ':'.join(parts[2:]).strip()
                            
                            issue = {
                                "file": os.path.relpath(file_path, code_path),
                                "line": int(line_num),
                                "message": message
                            }
                            
                            # 簡單分類
                            if "error" in message.lower():
                                results["errors"].append(issue)
                            else:
                                results["warnings"].append(issue)
        
        except subprocess.TimeoutExpired:
            self.logger.warning("ESLint analysis timed out", path=code_path)
        except Exception as e:
            self.logger.error("ESLint analysis failed", path=code_path, error=str(e))
        
        return results
    
    def _scan_for_secrets(self, code_path: str) -> List[Dict[str, Any]]:
        """掃描硬編碼的密鑰和密碼"""
        secrets = []
        secret_patterns = [
            r'password\s*=\s*["\'][^"\']+["\']',
            r'secret\s*=\s*["\'][^"\']+["\']',
            r'api_key\s*=\s*["\'][^"\']+["\']',
            r'token\s*=\s*["\'][^"\']+["\']',
            r'private_key\s*=\s*["\'][^"\']+["\']',
        ]
        
        for root, dirs, files in os.walk(code_path):
            # 跳過 .git 目錄
            if '.git' in dirs:
                dirs.remove('.git')
            
            for file in files:
                if file.endswith(('.py', '.js', '.jsx', '.ts', '.tsx', '.env', '.config')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            
                        for pattern in secret_patterns:
                            matches = re.finditer(pattern, content, re.IGNORECASE)
                            for match in matches:
                                line_num = content[:match.start()].count('\n') + 1
                                secrets.append({
                                    "file": os.path.relpath(file_path, code_path),
                                    "line": line_num,
                                    "pattern": pattern,
                                    "severity": "high"
                                })
                    except Exception as e:
                        self.logger.warning("Failed to scan file for secrets", file=file_path, error=str(e))
        
        return secrets
    
    def _check_python_dependencies(self, code_path: str) -> Dict[str, Any]:
        """檢查 Python 依賴項"""
        results = {
            "requirements_files": [],
            "vulnerabilities": []
        }
        
        # 查找 requirements 文件
        req_files = ['requirements.txt', 'requirements-dev.txt', 'pyproject.toml', 'setup.py']
        for req_file in req_files:
            req_path = os.path.join(code_path, req_file)
            if os.path.exists(req_path):
                results["requirements_files"].append(req_file)
        
        # 這裡可以集成安全掃描工具如 safety
        # 目前返回基本信息
        return results
    
    def calculate_score(self, results: Dict[str, Any]) -> int:
        """計算代碼質量評分"""
        score = 100
        
        # 靜態分析扣分
        static = results.get("static_analysis", {})
        score -= len(static.get("errors", [])) * 5  # 每個錯誤扣 5 分
        score -= len(static.get("warnings", [])) * 2  # 每個警告扣 2 分
        
        # 安全問題扣分
        security = results.get("security", {})
        score -= len(security.get("secrets", [])) * 10  # 每個密鑰洩露扣 10 分
        score -= len(security.get("vulnerabilities", [])) * 15  # 每個漏洞扣 15 分
        
        return max(0, score)  # 最低 0 分
    
    def generate_suggestions(self, results: Dict[str, Any]) -> List[str]:
        """生成改進建議"""
        suggestions = []
        
        static = results.get("static_analysis", {})
        if static.get("errors"):
            suggestions.append("修復靜態分析發現的錯誤以提高代碼質量")
        
        if static.get("warnings"):
            suggestions.append("處理代碼警告以改善代碼風格和可維護性")
        
        security = results.get("security", {})
        if security.get("secrets"):
            suggestions.append("移除硬編碼的密鑰和密碼，使用環境變量或安全的配置管理")
        
        if security.get("vulnerabilities"):
            suggestions.append("修復安全漏洞以保護應用程序安全")
        
        if results.get("score", 100) < 70:
            suggestions.append("整體代碼質量需要改進，建議進行代碼重構")
        
        return suggestions 