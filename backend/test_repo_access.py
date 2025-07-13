#!/usr/bin/env python3
"""
測試 GitHub 倉庫訪問權限
"""
import os
import requests
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

def test_repo_access():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN 未設置")
        return False
    
    print(f"✅ Token 已設置: {token[:10]}...")
    
    # 測試倉庫訪問
    repo = "harveytuan23/codewatchertest"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeWatcher-Test"
    }
    
    # 測試倉庫信息
    try:
        response = requests.get(f"https://api.github.com/repos/{repo}", headers=headers)
        print(f"倉庫信息 API: {response.status_code}")
        if response.status_code == 200:
            repo_data = response.json()
            print(f"✅ 倉庫訪問成功: {repo_data.get('name')}")
            print(f"   權限: {repo_data.get('permissions', {})}")
        else:
            print(f"❌ 倉庫訪問失敗: {response.text}")
    except Exception as e:
        print(f"❌ 倉庫訪問錯誤: {e}")
    
    # 測試 PR 列表
    try:
        response = requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=headers)
        print(f"PR 列表 API: {response.status_code}")
        if response.status_code == 200:
            prs = response.json()
            print(f"✅ PR 列表訪問成功: 找到 {len(prs)} 個 PR")
        else:
            print(f"❌ PR 列表訪問失敗: {response.text}")
    except Exception as e:
        print(f"❌ PR 列表訪問錯誤: {e}")
    
    # 測試 Issue 列表
    try:
        response = requests.get(f"https://api.github.com/repos/{repo}/issues", headers=headers)
        print(f"Issue 列表 API: {response.status_code}")
        if response.status_code == 200:
            issues = response.json()
            print(f"✅ Issue 列表訪問成功: 找到 {len(issues)} 個 Issue")
        else:
            print(f"❌ Issue 列表訪問失敗: {response.text}")
    except Exception as e:
        print(f"❌ Issue 列表訪問錯誤: {e}")

if __name__ == "__main__":
    print("🔍 測試 GitHub 倉庫訪問權限...")
    test_repo_access() 