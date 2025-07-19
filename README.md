# CodeWatcher AI - Automated Code Review & Reliability Platform

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18+-blue.svg)](https://reactjs.org)
[![TypeScript](https://img.shields.io/badge/TypeScript-4.9+-blue.svg)](https://typescriptlang.org)
[![Docker](https://img.shields.io/badge/Docker-Ready-blue.svg)](https://docker.com)

> 🚀 **Intelligent Automated Code Review Platform** - Providing instant code review feedback for your GitHub projects through AI-driven static analysis, security scanning, and quality assessment.

## 📋 Table of Contents

- [Features](#-features)
- [Technical Architecture](#-technical-architecture)
- [Quick Start](#-quick-start)
- [Installation & Deployment](#-installation--deployment)
- [Usage Guide](#-usage-guide)
- [API Documentation](#-api-documentation)
- [Configuration](#-configuration)
- [Development Guide](#-development-guide)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

### 🤖 Automated Code Review
- **GitHub Webhook Integration**: Automatically triggers code analysis when PRs are created
- **Real-time Comment Publishing**: Automatically posts detailed comments on PRs after analysis completion
- **Status Updates**: Real-time PR status updates showing analysis progress and results

### 🔍 Multi-dimensional Code Analysis
- **Static Code Analysis**:
  - Python: Using Flake8 for code style and error checking
  - JavaScript/TypeScript: Using ESLint for code quality checking
- **Security Vulnerability Scanning**:
  - Hardcoded secret detection (API Keys, passwords, tokens, etc.)
  - Regex pattern matching
  - Support for multiple file formats
- **Code Quality Scoring**:
  - Intelligent scoring system based on errors, warnings, and security issues
  - 5 points deducted per error, 2 points per warning, 10-15 points per security issue
  - Provides specific improvement suggestions

### 📊 Intelligent Scoring System
- **Comprehensive Scoring**: Multi-dimensional code quality assessment
- **Detailed Reports**: Includes error details, warning information, security issues, and improvement suggestions
- **Visualization**: Intuitive frontend interface displaying analysis results

### 🎯 User-Friendly Interface
- **Modern UI**: Responsive design based on Material-UI
- **Real-time Updates**: Live display of analysis progress and results
- **Manual Analysis**: Support for manual repository information input for analysis
- **History Records**: View past analysis results

## 🏗️ Technical Architecture

### Backend Tech Stack
- **FastAPI**: High-performance Python web framework
- **Pydantic**: Data validation and serialization
- **structlog**: Structured logging
- **requests**: HTTP client
- **python-dotenv**: Environment variable management

### Frontend Tech Stack
- **React 18**: Modern frontend framework
- **TypeScript**: Type-safe JavaScript
- **Material-UI**: UI component library
- **React Router**: Route management
- **React Query**: Server state management
- **react-hot-toast**: Notification system

### Development Tools
- **Docker**: Containerized deployment
- **ESLint**: JavaScript/TypeScript code checking
- **Flake8**: Python code checking
- **GitHub API**: GitHub integration

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional)
- GitHub Personal Access Token

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/codewatcher.git
cd codewatcher
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Frontend Setup
```bash
cd frontend
npm install
```

### 4. Environment Configuration
```bash
# Backend .env file
cp backend/.env.example backend/.env
# Edit .env file and add your GitHub Token
```

### 5. Start Services
```bash
# Backend (Terminal 1)
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Frontend (Terminal 2)
cd frontend
npm start
```

## 📦 Installation & Deployment

### Docker Deployment
```bash
# Using Docker Compose
docker-compose up -d

# Or build separately
docker build -t codewatcher-backend ./backend
docker build -t codewatcher-frontend ./frontend
```

### Production Deployment
```bash
# Backend production deployment
cd backend
pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4

# Frontend production build
cd frontend
npm run build
```

## 📖 Usage Guide

### GitHub Webhook Setup

1. **Create GitHub Token**
   - Visit GitHub Settings > Developer settings > Personal access tokens
   - Generate new token with `repo` and `workflow` permissions

2. **Configure Webhook**
   - In repository settings, go to Webhooks
   - Add webhook URL: `https://your-domain.com/api/v1/webhooks/github`
   - Select `Pull requests` events

3. **Environment Variable Configuration**
   ```env
   GITHUB_TOKEN=your_github_token_here
   SECRET_KEY=your_secret_key_here
   ```

### Manual Analysis

1. Visit frontend interface: `http://localhost:3000`
2. Enter repository information in the "Manual Analysis" tab
3. Click "Start Analysis" button
4. View real-time analysis results

### Automated Analysis Workflow

```
GitHub PR Creation
    ↓
Webhook Trigger
    ↓
Code Cloning
    ↓
Multi-dimensional Analysis
    ↓
Score Calculation
    ↓
Automatic Comment Publishing
```

## 📚 API Documentation

### Main Endpoints

#### Webhook Endpoints
- `POST /api/v1/webhooks/github` - Receive GitHub webhook events

#### Analysis Endpoints
- `POST /api/v1/analysis/manual` - Manually trigger code analysis
- `GET /api/v1/analysis/{analysis_id}` - Get analysis results

#### Project Endpoints
- `GET /api/v1/projects` - Get project list
- `POST /api/v1/projects` - Create new project

### Request Examples

```bash
# Manual analysis
curl -X POST "http://localhost:8000/api/v1/analysis/manual" \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "https://github.com/username/repo",
    "branch": "main"
  }'
```

## ⚙️ Configuration

### Backend Configuration (.env)
```env
# GitHub Configuration
GITHUB_TOKEN=your_github_token_here

# Application Configuration
SECRET_KEY=your_secret_key_here
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Analysis Configuration
MAX_FILE_SIZE=10485760  # 10MB
SUPPORTED_LANGUAGES=python,javascript,typescript
```

### Frontend Configuration
```typescript
// src/config/api.ts
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
```

## 🛠️ Development Guide

### Project Structure
```
codewatcher/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       └── api.py
│   │   ├── core/
│   │   │   └── config.py
│   │   └── services/
│   │       ├── analysis_service.py
│   │       └── github_service.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
└── docker-compose.yml
```

### Development Commands
```bash
# Backend development
cd backend
uvicorn main:app --reload

# Frontend development
cd frontend
npm start

# Code linting
cd backend && flake8 .
cd frontend && npm run lint

# Testing
cd backend && python -m pytest
cd frontend && npm test
```

### Adding New Analysis Tools

1. Add new analysis functions in `backend/app/services/analysis_service.py`
2. Integrate new tools in the `run_analysis` method
3. Update scoring logic to include results from new tools

## 🤝 Contributing

We welcome all forms of contributions!

### Contribution Process
1. Fork this project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Code Standards
- Use Black for Python code formatting
- Use Prettier for frontend code formatting
- Follow PEP 8 (Python) and ESLint (JavaScript) standards
- Add appropriate comments and documentation

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [React](https://reactjs.org/) - User interface library
- [Material-UI](https://mui.com/) - React UI component library
- [GitHub API](https://docs.github.com/en/rest) - GitHub integration
- [Flake8](https://flake8.pycqa.org/) - Python code checking tool
- [ESLint](https://eslint.org/) - JavaScript code checking tool

## 📞 Contact

- Project Homepage: [GitHub Repository](https://github.com/yourusername/codewatcher)
- Issue Reports: [Issues](https://github.com/yourusername/codewatcher/issues)
- Feature Suggestions: [Discussions](https://github.com/yourusername/codewatcher/discussions)

---

⭐ If this project helps you, please give us a star! 