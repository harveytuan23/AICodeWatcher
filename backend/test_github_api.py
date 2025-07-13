#!/usr/bin/env python3
"""
测试 GitHub API 调用
"""
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_github_api():
    token = os.getenv("GITHUB_TOKEN")
    repo = "harveytuan23/codewatchertest"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeWatcher-AI-Review"
    }
    
    print(f"Token: {token[:20]}..." if token else "No token")
    print(f"Repo: {repo}")
    
    # 测试1: 获取仓库信息
    print("\n1. 测试获取仓库信息...")
    try:
        response = requests.get(f"https://api.github.com/repos/{repo}", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Repo name: {data['name']}")
            print(f"Private: {data['private']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # 测试2: 获取PR列表
    print("\n2. 测试获取PR列表...")
    try:
        response = requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            prs = response.json()
            print(f"Found {len(prs)} PRs")
            for pr in prs[:3]:  # 显示前3个PR
                print(f"  PR #{pr['number']}: {pr['title']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")
    
    # 测试3: 测试创建评论（不实际创建）
    print("\n3. 测试评论API权限...")
    try:
        # 获取最新的PR
        response = requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=headers)
        if response.status_code == 200:
            prs = response.json()
            if prs:
                latest_pr = prs[0]
                pr_number = latest_pr['number']
                print(f"Latest PR: #{pr_number}")
                
                # 测试获取PR评论（只读操作）
                response = requests.get(f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments", headers=headers)
                print(f"Comments API Status: {response.status_code}")
                if response.status_code == 200:
                    comments = response.json()
                    print(f"Found {len(comments)} comments")
                else:
                    print(f"Error: {response.text}")
        else:
            print("Could not get PRs")
    except Exception as e:
        print(f"Exception: {e}")
    
    # 测试4: 测试状态API权限
    print("\n4. 测试状态API权限...")
    try:
        # 获取最新的commit
        response = requests.get(f"https://api.github.com/repos/{repo}/commits", headers=headers)
        print(f"Commits API Status: {response.status_code}")
        if response.status_code == 200:
            commits = response.json()
            if commits:
                latest_commit = commits[0]
                sha = latest_commit['sha']
                print(f"Latest commit: {sha[:8]}...")
                
                # 测试获取状态（只读操作）
                response = requests.get(f"https://api.github.com/repos/{repo}/statuses/{sha}", headers=headers)
                print(f"Statuses API Status: {response.status_code}")
                if response.status_code == 200:
                    statuses = response.json()
                    print(f"Found {len(statuses)} statuses")
                else:
                    print(f"Error: {response.text}")
        else:
            print("Could not get commits")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_github_api() 