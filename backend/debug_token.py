#!/usr/bin/env python3
"""
檢查後端服務實際使用的 token
"""
import os
from dotenv import load_dotenv

# 加載環境變量
load_dotenv()

def check_token():
    token = os.getenv("GITHUB_TOKEN")
    print(f"Token: {token}")
    print(f"Token length: {len(token) if token else 0}")
    print(f"Token prefix: {token[:10] if token else 'None'}...")
    
    # 測試 token 是否有效
    if token:
        import requests
        headers = {
            "Authorization": f"token {token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "CodeWatcher-Test"
        }
        
        try:
            response = requests.get("https://api.github.com/user", headers=headers)
            print(f"GitHub API test: {response.status_code}")
            if response.status_code == 200:
                user_data = response.json()
                print(f"User: {user_data.get('login')}")
            else:
                print(f"Error: {response.text}")
        except Exception as e:
            print(f"Exception: {e}")
    else:
        print("No token found!")

if __name__ == "__main__":
    check_token() 