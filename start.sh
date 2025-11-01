#!/bin/bash

# Railway部署启动脚本

# 切换到backend目录
cd backend

# 等待数据库就绪
echo "等待数据库连接..."
sleep 10

# 运行数据库迁移
echo "运行数据库迁移..."
python3 -m alembic upgrade head

# 启动应用
echo "启动FastAPI应用..."
python3 -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
