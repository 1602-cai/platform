# 可转债监控平台部署指南

## 📋 部署概述

本项目采用前后端分离架构：
- **前端**: Next.js + Vercel
- **后端**: FastAPI + Railway (PostgreSQL)
- **数据源**: Tushare API

## 🚀 部署步骤

### 1. 准备工作

#### 获取Tushare API Token
1. 访问 [Tushare官网](https://tushare.pro)
2. 注册账号并获取API Token
3. 准备至少2000积分用于数据调用

#### 代码推送
```bash
# 创建GitHub仓库
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/your-username/bond-monitor.git
git push -u origin main
```

### 2. Railway后端部署

#### 2.1 创建Railway项目
1. 访问 [Railway.app](https://railway.app)
2. 点击 "Start a new project"
3. 选择 "Deploy from GitHub repo"
4. 连接你的GitHub仓库

#### 2.2 配置环境变量
在Railway项目设置中添加以下环境变量：

```bash
# 数据库配置 (Railway自动提供)
DATABASE_URL=postgresql://...

# Tushare API配置
TUSHARE_TOKEN=your_tushare_token_here

# 应用配置
APP_ENV=production
```

#### 2.3 数据库设置
Railway会自动创建PostgreSQL数据库，`DATABASE_URL`环境变量会自动设置。

#### 2.4 部署验证
部署完成后，你会获得一个类似 `https://your-project-name.up.railway.app` 的URL。

### 3. Vercel前端部署

#### 3.1 创建Vercel项目
1. 访问 [Vercel.com](https://vercel.com)
2. 点击 "Import Project"
3. 连接GitHub仓库，选择 `frontend` 目录

#### 3.2 配置环境变量
在Vercel项目设置中添加：

```bash
NEXT_PUBLIC_API_URL=https://your-railway-backend-url
```

#### 3.3 修改Vercel配置
更新 `frontend/vercel.json` 中的后端URL：

```json
{
  "routes": [
    {
      "src": "/api/(.*)",
      "dest": "https://your-railway-backend-url/api/$1"
    }
  ],
  "env": {
    "NEXT_PUBLIC_API_URL": "https://your-railway-backend-url"
  }
}
```

#### 3.4 部署验证
部署完成后，你会获得一个类似 `https://your-project.vercel.app` 的URL。

## 🔧 部署文件说明

### Railway配置
- `backend/Procfile` - Railway启动命令
- `backend/start.sh` - 启动脚本
- `backend/requirements.txt` - Python依赖
- `backend/alembic.ini` - 数据库迁移配置

### Vercel配置
- `frontend/vercel.json` - Vercel部署配置
- `frontend/package.json` - Node.js依赖

## 📊 数据库迁移

Railway部署时会自动运行数据库迁移：

```bash
alembic upgrade head
```

## 🌐 域名配置

### 自定义域名（可选）
1. 在Vercel中添加自定义域名
2. 在域名服务商处配置CNAME记录指向Vercel

## 🔍 监控和调试

### 查看日志
- **Railway**: 在Railway控制台查看应用日志
- **Vercel**: 在Vercel控制台查看部署日志

### 常见问题
1. **数据库连接失败**: 检查`DATABASE_URL`环境变量
2. **API调用失败**: 检查Tushare Token和积分
3. **前端API调用失败**: 检查`NEXT_PUBLIC_API_URL`配置

## 💰 成本估算

### Railway (后端)
- **免费额度**: 512MB RAM, 1GB存储
- **付费计划**: 根据使用量，通常每月$5-10

### Vercel (前端)
- **免费**: 个人项目完全免费
- **付费**: 商业用途每月$20+

### Tushare API
- **积分费用**: 根据调用频率
- **建议**: 保持2120积分以上

## 🔄 更新部署

### 代码更新
```bash
git add .
git commit -m "Update features"
git push origin main
```

Railway和Vercel会自动检测代码变更并重新部署。

## 📞 技术支持

如遇到部署问题，请检查：
1. 环境变量配置是否正确
2. 数据库连接是否正常
3. API Token是否有效
4. 网络连接是否正常

## 🎉 部署完成！

部署完成后，你的可转债监控平台将可以通过以下URL访问：
- **前端**: https://your-project.vercel.app
- **后端API**: https://your-project-name.up.railway.app

享受你的量化投资工具！🚀
