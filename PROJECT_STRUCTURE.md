# CodeWatcher 項目結構

## 目錄結構概覽

```
codewatcher/
├── README.md                    # 項目主文檔
├── .gitignore                   # Git忽略文件
├── PROJECT_STRUCTURE.md         # 項目結構說明
│
├── backend/                     # 後端API服務
│   ├── main.py                  # 應用入口點
│   ├── requirements.txt         # Python依賴
│   └── app/                     # 應用代碼
│       ├── api/                 # API層
│       │   └── v1/             # API版本1
│       │       ├── api.py      # API路由配置
│       │       └── endpoints/  # API端點
│       │           ├── auth.py      # 認證端點
│       │           ├── projects.py  # 專案管理端點
│       │           ├── reviews.py   # 程式碼審查端點
│       │           └── analysis.py  # 程式碼分析端點
│       ├── core/               # 核心配置
│       │   ├── config.py       # 應用配置
│       │   └── logging.py      # 日誌配置
│       ├── models/             # 數據模型
│       ├── services/           # 業務邏輯服務
│       │   ├── analysis/       # 程式碼分析服務
│       │   ├── security/       # 安全掃描服務
│       │   ├── compliance/     # 合規性檢查服務
│       │   └── ai_review/      # AI審查服務
│       └── utils/              # 工具函數
│
├── frontend/                    # 前端React應用
│   ├── package.json            # Node.js依賴
│   ├── tsconfig.json           # TypeScript配置
│   └── src/                    # 源代碼
│       ├── App.tsx             # 主應用組件
│       ├── components/         # 可重用組件
│       │   ├── common/         # 通用組件
│       │   ├── layout/         # 佈局組件
│       │   │   └── Layout.tsx  # 主佈局
│       │   ├── forms/          # 表單組件
│       │   └── charts/         # 圖表組件
│       ├── pages/              # 頁面組件
│       │   ├── Dashboard.tsx   # 儀表板
│       │   ├── Projects.tsx    # 專案管理
│       │   ├── CodeReview.tsx  # 程式碼審查
│       │   ├── Settings.tsx    # 設定頁面
│       │   └── Login.tsx       # 登入頁面
│       ├── services/           # API服務
│       ├── utils/              # 工具函數
│       ├── styles/             # 樣式文件
│       └── types/              # TypeScript類型定義
│
├── ml-engine/                   # AI/ML分析引擎
│   ├── models/                 # 機器學習模型
│   ├── data/                   # 訓練數據
│   ├── training/               # 模型訓練腳本
│   └── utils/                  # ML工具函數
│
├── integrations/                # 第三方平台整合
│   ├── github/                 # GitHub整合
│   ├── gitlab/                 # GitLab整合
│   └── ci_cd/                  # CI/CD整合
│
├── docs/                       # 項目文檔
│   ├── README.md               # 文檔主頁
│   ├── api/                    # API文檔
│   ├── deployment/             # 部署文檔
│   └── development/            # 開發文檔
│
└── deploy/                     # 部署配置
    ├── docker/                 # Docker配置
    │   ├── docker-compose.yml  # Docker Compose
    │   ├── backend.Dockerfile  # 後端Dockerfile
    │   └── frontend.Dockerfile # 前端Dockerfile
    ├── kubernetes/             # Kubernetes配置
    └── terraform/              # Terraform配置
```

## 技術架構

### 後端架構 (FastAPI)
- **API層**: RESTful API端點，版本控制
- **服務層**: 業務邏輯，包括程式碼分析、安全掃描、AI審查
- **數據層**: PostgreSQL數據庫，Redis緩存
- **任務隊列**: Celery處理異步任務

### 前端架構 (React + TypeScript)
- **組件化**: 可重用的UI組件
- **狀態管理**: React Query處理服務器狀態
- **路由**: React Router處理頁面導航
- **UI框架**: Material-UI提供現代化界面

### AI/ML架構
- **靜態分析**: 語法檢查、複雜度分析
- **安全掃描**: 漏洞檢測、敏感信息識別
- **AI審查**: OpenAI API整合，模式識別
- **模型管理**: 本地模型緩存和版本控制

## 開發流程

### 1. 環境設置
```bash
# 克隆項目
git clone <repository-url>
cd codewatcher

# 後端設置
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# 前端設置
cd ../frontend
npm install
```

### 2. 啟動開發服務
```bash
# 後端 (終端1)
cd backend
python main.py

# 前端 (終端2)
cd frontend
npm start
```

### 3. 訪問應用
- 前端: http://localhost:3000
- 後端API: http://localhost:8000
- API文檔: http://localhost:8000/docs

## 部署選項

### 開發環境
- Docker Compose (推薦)
- 本地安裝

### 生產環境
- Kubernetes
- Docker Swarm
- 雲端服務 (AWS, GCP, Azure)

## 下一步開發計劃

1. **數據庫設計** - 設計核心數據模型
2. **認證系統** - 實現用戶認證和授權
3. **程式碼分析引擎** - 實現靜態分析功能
4. **AI整合** - 整合OpenAI API進行程式碼審查
5. **前端界面** - 完善用戶界面和交互
6. **CI/CD整合** - 實現GitHub/GitLab Webhook
7. **監控和日誌** - 添加應用監控和日誌系統 