FROM node:18-alpine

# 設置工作目錄
WORKDIR /app

# 複製package文件
COPY frontend/package*.json ./

# 安裝依賴
RUN npm ci --only=production

# 複製源代碼
COPY frontend/ .

# 構建應用
RUN npm run build

# 安裝serve
RUN npm install -g serve

# 暴露端口
EXPOSE 3000

# 啟動命令
CMD ["serve", "-s", "build", "-l", "3000"] 