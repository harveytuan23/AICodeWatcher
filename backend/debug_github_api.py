#!/usr/bin/env python3
"""
調試 GitHub API 調用
"""
import os
import requests
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

def debug_github_api():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN 未設置")
        return
    
    print(f"✅ Token: {token[:10]}...")
    
    repo = "harveytuan23/codewatchertest"
    pr_number = 12  # 根據您的 PR 號碼調整
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeWatcher-AI-Review"
    }
    
    print(f"Headers: {headers}")
    
    # 測試 1: 創建 PR 評論
    print("\n🔍 測試 1: 創建 PR 評論")
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    data = {"body": "測試評論"}
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ PR 評論創建成功")
        else:
            print(f"❌ PR 評論創建失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試 2: 更新 PR 狀態
    print("\n🔍 測試 2: 更新 PR 狀態")
    sha = "b0d5adb7abed254fcb1bde64c65e9a08c2d0c7d9"  # 根據您的 commit SHA 調整
    url = f"https://api.github.com/repos/{repo}/statuses/{sha}"
    data = {
        "state": "success",
        "description": "測試狀態更新",
        "context": "CodeWatcher AI Review"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ PR 狀態更新成功")
        else:
            print(f"❌ PR 狀態更新失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")
    
    # 測試 3: 創建行級評論
    print("\n🔍 測試 3: 創建行級評論")
    url = f"https://api.github.com/repos/{repo}/pulls/{pr_number}/comments"
    data = {
        "commit_id": sha,
        "path": "test.py",
        "line": 1,
        "body": "測試行級評論"
    }
    
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"URL: {url}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 201:
            print("✅ 行級評論創建成功")
        else:
            print(f"❌ 行級評論創建失敗: {response.status_code}")
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    print("🔍 調試 GitHub API 調用...")
    debug_github_api() 