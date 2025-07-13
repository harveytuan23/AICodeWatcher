FROM python:3.11-slim

# 設置工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# 複製依賴文件
COPY backend/requirements.txt .

# 安裝Python依賴
RUN pip install --no-cache-dir -r requirements.txt

# 複製應用代碼
COPY backend/ .

# 創建必要的目錄
RUN mkdir -p uploads models logs

# 設置環境變量
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# 暴露端口
EXPOSE 8000

# 啟動命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 