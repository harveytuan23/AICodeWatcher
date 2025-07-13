#!/usr/bin/env python3
"""
测试 GitHub API 写入操作
"""
import os
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_github_write():
    token = os.getenv("GITHUB_TOKEN")
    repo = "harveytuan23/codewatchertest"
    
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "CodeWatcher-AI-Review"
    }
    
    print(f"Token: {token[:20]}..." if token else "No token")
    print(f"Repo: {repo}")
    
    # 获取最新的PR
    print("\n1. 获取最新PR...")
    try:
        response = requests.get(f"https://api.github.com/repos/{repo}/pulls", headers=headers)
        if response.status_code == 200:
            prs = response.json()
            if prs:
                latest_pr = prs[0]
                pr_number = latest_pr['number']
                commit_sha = latest_pr['head']['sha']
                print(f"Latest PR: #{pr_number}")
                print(f"Commit SHA: {commit_sha[:8]}...")
                
                # 测试2: 创建PR评论
                print(f"\n2. 测试创建PR评论...")
                comment_data = {
                    "body": "🤖 **CodeWatcher AI Review Test**\n\nThis is a test comment from the automated review system."
                }
                
                response = requests.post(
                    f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments",
                    headers=headers,
                    json=comment_data
                )
                print(f"Create Comment Status: {response.status_code}")
                if response.status_code == 201:
                    comment = response.json()
                    print(f"✅ Comment created successfully!")
                    print(f"Comment ID: {comment['id']}")
                    print(f"Comment URL: {comment['html_url']}")
                else:
                    print(f"❌ Error: {response.text}")
                
                # 测试3: 更新PR状态
                print(f"\n3. 测试更新PR状态...")
                status_data = {
                    "state": "success",
                    "description": "CodeWatcher AI Review completed",
                    "context": "CodeWatcher AI Review",
                    "target_url": "https://github.com/harveytuan23/codewatchertest"
                }
                
                response = requests.post(
                    f"https://api.github.com/repos/{repo}/statuses/{commit_sha}",
                    headers=headers,
                    json=status_data
                )
                print(f"Update Status Status: {response.status_code}")
                if response.status_code == 201:
                    status = response.json()
                    print(f"✅ Status updated successfully!")
                    print(f"Status ID: {status['id']}")
                    print(f"Status URL: {status['url']}")
                else:
                    print(f"❌ Error: {response.text}")
                    
            else:
                print("No PRs found")
        else:
            print(f"Error getting PRs: {response.text}")
    except Exception as e:
        print(f"Exception: {e}")

if __name__ == "__main__":
    test_github_write() 