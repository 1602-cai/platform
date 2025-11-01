#!/bin/bash

# Railway部署启动脚本

# 切换到backend目录
cd backend

# 等待数据库就绪
echo "等待数据库连接..."
sleep 10

# 查找Python路径
PYTHON_PATH=$(which python || which python3 || which /usr/local/bin/python || which /usr/bin/python || echo "python")

echo "使用Python路径: $PYTHON_PATH"

# 运行数据库迁移
echo "运行数据库迁移..."
$PYTHON_PATH -m alembic upgrade head

# 启动应用
echo "启动FastAPI应用..."
$PYTHON_PATH -m uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
