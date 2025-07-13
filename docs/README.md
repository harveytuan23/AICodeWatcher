# CodeWatcher 文檔

## 項目概述

CodeWatcher 是一個自動化AI程式碼審查與可靠性平台，專為中小企業設計。

## 文檔結構

### 開發文檔
- [API文檔](api/README.md) - API接口說明
- [部署指南](deployment/README.md) - 部署和配置說明
- [開發指南](development/README.md) - 開發環境設置和貢獻指南

### 架構文檔
- [系統架構](architecture.md) - 整體系統架構設計
- [數據庫設計](database.md) - 數據庫結構和關係
- [安全設計](security.md) - 安全架構和最佳實踐

## 快速開始

1. **環境設置**
   ```bash
   # 後端
   cd backend
   pip install -r requirements.txt
   
   # 前端
   cd frontend
   npm install
   ```

2. **啟動服務**
   ```bash
   # 後端
   cd backend
   python main.py
   
   # 前端
   cd frontend
   npm start
   ```

3. **訪問應用**
   - 前端: http://localhost:3000
   - 後端API: http://localhost:8000
   - API文檔: http://localhost:8000/docs

## 技術棧

### 後端
- **框架**: FastAPI
- **數據庫**: PostgreSQL
- **緩存**: Redis
- **任務隊列**: Celery
- **AI/ML**: OpenAI API, Transformers

### 前端
- **框架**: React 18
- **UI庫**: Material-UI
- **狀態管理**: React Query
- **路由**: React Router
- **語言**: TypeScript

## 貢獻指南

請參考 [開發指南](development/README.md) 了解如何參與項目開發。

## 授權

MIT License 