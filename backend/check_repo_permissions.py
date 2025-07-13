#!/usr/bin/env python3
"""
檢查 token 對特定倉庫的權限
"""
import os
import requests
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

def check_repo_permissions():
    token = os.getenv("GITHUB_TOKEN")
    repo = "harveytuan23/codewatchertest"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeWatcher-Test"
    }
    
    # 檢查倉庫權限
    try:
        response = requests.get(f"https://api.github.com/repos/{repo}", headers=headers)
        print(f"倉庫信息 API: {response.status_code}")
        if response.status_code == 200:
            repo_data = response.json()
            permissions = repo_data.get("permissions", {})
            print(f"倉庫權限: {permissions}")
            
            # 檢查是否有寫入權限
            if permissions.get("push"):
                print("✅ 有寫入權限")
            else:
                print("❌ 沒有寫入權限")
                
            if permissions.get("admin"):
                print("✅ 有管理權限")
            else:
                print("❌ 沒有管理權限")
        else:
            print(f"❌ 倉庫訪問失敗: {response.text}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試創建評論的權限
    print("\n測試創建評論權限...")
    try:
        # 先獲取最新的 PR
        response = requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=headers)
        if response.status_code == 200:
            prs = response.json()
            if prs:
                latest_pr = prs[0]
                pr_number = latest_pr["number"]
                print(f"測試 PR #{pr_number}")
                
                # 嘗試創建評論
                comment_data = {"body": "權限測試評論"}
                response = requests.post(
                    f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments",
                    headers=headers,
                    json=comment_data
                )
                print(f"創建評論 API: {response.status_code}")
                if response.status_code == 201:
                    print("✅ 可以創建評論")
                else:
                    print(f"❌ 無法創建評論: {response.text}")
            else:
                print("沒有找到 PR")
        else:
            print(f"無法獲取 PR 列表: {response.text}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    check_repo_permissions() 