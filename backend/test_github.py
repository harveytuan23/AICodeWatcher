#!/usr/bin/env python3
"""
測試 GitHub API 連接
"""
import os
import requests
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

def test_github_api():
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        print("❌ GITHUB_TOKEN 未設置")
        return False
    
    print(f"✅ Token 已設置: {token[:10]}...")
    
    # 測試 GitHub API
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeWatcher-Test"
    }
    
    try:
        response = requests.get("https://api.github.com/user", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ GitHub API 連接成功")
            print(f"   用戶名: {user_data.get('login')}")
            print(f"   用戶 ID: {user_data.get('id')}")
            return True
        else:
            print(f"❌ GitHub API 連接失敗: {response.status_code}")
            print(f"   錯誤信息: {response.text}")
            return False
    except Exception as e:
        print(f"❌ 連接錯誤: {e}")
        return False

if __name__ == "__main__":
    print("🔍 測試 GitHub API 連接...")
    test_github_api() 