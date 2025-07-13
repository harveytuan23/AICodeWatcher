# GitHub 集成設置

## 1. 創建 GitHub Personal Access Token

1. 前往 GitHub Settings > Developer settings > Personal access tokens
2. 點擊 "Generate new token (classic)"
3. 選擇以下權限：
   - `repo` - 完整的倉庫訪問權限
   - `workflow` - 工作流程權限（可選）
4. 生成並複製 token

## 2. 設置環境變量

創建 `.env` 文件並添加：

```bash
# GitHub 配置
GITHUB_TOKEN=your-github-personal-access-token-here

# 其他配置
SECRET_KEY=your-secret-key-here-make-it-long-and-random
DEBUG=True
```

## 3. 配置 GitHub Webhook

1. 前往你的 GitHub 倉庫
2. 點擊 Settings > Webhooks
3. 點擊 "Add webhook"
4. 設置：
   - **Payload URL**: `https://your-domain.com/api/v1/webhooks/github`
   - **Content type**: `application/json`
   - **Secret**: 可選，用於驗證 webhook
   - **Events**: 選擇 "Pull requests"
5. 點擊 "Add webhook"

## 4. 本地測試

使用 ngrok 進行本地測試：

```bash
# 安裝 ngrok
brew install ngrok

# 啟動隧道
ngrok http 8000

# 使用生成的 URL 作為 webhook URL
# 例如：https://abc123.ngrok.io/api/v1/webhooks/github
```

## 5. 測試 PR

1. 創建一個測試 PR
2. 系統會自動：
   - 克隆 PR 代碼
   - 執行靜態分析
   - 在 PR 上發表評論
   - 更新 PR 狀態

## 注意事項

- 確保 GitHub Token 有足夠的權限
- 本地測試時需要使用 ngrok 或類似的隧道服務
- 生產環境請使用 HTTPS
- 定期更新 GitHub Token 