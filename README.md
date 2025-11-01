# 可转债信号监控平台

一个智能的可转债信号监控和自动交易平台，实时监控股票异动并自动买入对应可转债。

## 🚀 项目特性

- **实时监控**：毫秒级股票价格监控，自动检测涨停和大涨信号
- **智能交易**：信号触发时自动执行可转债买入交易
- **可视化界面**：直观的卡片式股票-可转债配对显示
- **深度分析**：双图表详情页面提供技术分析
- **云端架构**：零本地存储，所有数据托管在云端
- **灵活清理**：智能数据清理，控制存储成本

## 🏗️ 技术架构

### 前端技术栈
- **框架**：Next.js 14 + React 18
- **样式**：Tailwind CSS + shadcn/ui
- **图表**：Recharts
- **状态管理**：Zustand
- **部署**：Vercel

### 后端技术栈
- **框架**：Python + FastAPI
- **数据库**：PostgreSQL (Railway)
- **数据源**：Tushare API
- **部署**：Railway

### 系统架构图
```
用户界面 (Vercel) ↔ API服务 (Railway) ↔ 云数据库 (Railway PostgreSQL)
                              ↕
                         数据源 (Tushare)
                              ↕
                         交易接口 (待集成)
```

## 📋 开发环境要求

### 系统要求
- Node.js 18+
- Python 3.9+
- Git
- Railway 账户
- Vercel 账户

### 环境变量
```bash
# 后端环境变量 (Railway)
DATABASE_URL=postgresql://...
TUSHARE_TOKEN=a0c3518c35f2494d5ee0b99792e0359005d793f3af65dcf13892c5e0
REDIS_URL=redis://... (可选)

# 前端环境变量 (Vercel)
NEXT_PUBLIC_API_URL=https://your-railway-app.railway.app
```

## 🚀 快速开始

### 1. 克隆项目
```bash
git clone <repository-url>
cd bond-monitoring-platform
```

### 2. 后端设置
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # 配置环境变量
uvicorn app.main:app --reload
```

### 3. 前端设置
```bash
cd frontend
npm install
cp .env.example .env.local  # 配置环境变量
npm run dev
```

### 4. 数据库迁移
```bash
# Railway 会自动创建数据库
# 运行初始化脚本
python backend/scripts/init_db.py
```

## 📁 项目结构

```
bond-monitoring-platform/
├── backend/                    # 后端服务
│   ├── app/
│   │   ├── api/               # API路由
│   │   ├── core/              # 核心业务逻辑
│   │   ├── models/            # 数据模型
│   │   ├── services/          # 外部服务集成
│   │   └── utils/             # 工具函数
│   ├── scripts/               # 数据库脚本
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                   # 前端应用
│   ├── components/            # React组件
│   ├── pages/                 # Next.js页面
│   ├── hooks/                 # 自定义hooks
│   ├── lib/                   # 工具库
│   ├── styles/                # 样式文件
│   └── public/                # 静态资源
├── docs/                      # 项目文档
└── README.md
```

## 🔌 API 接口文档

### 核心API

#### 获取监控数据
```http
GET /api/monitoring/pairs
```
获取股票-可转债配对监控数据

**响应示例：**
```json
{
  "data": [
    {
      "stockCode": "000001.SZ",
      "stockName": "平安银行",
      "stockPrice": 10.50,
      "stockChange": 2.5,
      "bondCode": "113048.SZ",
      "bondName": "华正转债",
      "bondPrice": 125.50,
      "bondChange": 1.8,
      "conversionPrice": 8.50,
      "premium": 45.2,
      "maturityDate": "2026-12-31",
      "signalType": "big_rise"
    }
  ],
  "total": 100,
  "page": 1,
  "pageSize": 20
}
```

#### 执行交易
```http
POST /api/trading/execute
```

**请求体：**
```json
{
  "bondCode": "113048.SZ",
  "orderType": "buy",
  "quantity": 100,
  "price": 125.50
}
```

#### 数据清理
```http
POST /api/admin/cleanup
```

**请求体：**
```json
{
  "dataTypes": ["signals", "trades"],
  "timeRange": {
    "hours": 24
  },
  "previewOnly": false
}
```

## 🗄️ 数据库设计

### 核心表结构

#### bonds (可转债基础信息)
```sql
CREATE TABLE bonds (
    id SERIAL PRIMARY KEY,
    ts_code VARCHAR(20) UNIQUE NOT NULL,
    bond_name VARCHAR(100),
    stock_code VARCHAR(20),
    stock_name VARCHAR(100),
    conversion_price DECIMAL(10,2),
    maturity_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### price_ticks (实时价格数据)
```sql
CREATE TABLE price_ticks (
    id SERIAL PRIMARY KEY,
    stock_code VARCHAR(20) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    volume BIGINT,
    timestamp TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_price_ticks_stock_time ON price_ticks(stock_code, timestamp DESC);
```

#### signals (信号记录)
```sql
CREATE TABLE signals (
    id SERIAL PRIMARY KEY,
    stock_code VARCHAR(20) NOT NULL,
    bond_code VARCHAR(20),
    signal_type VARCHAR(20),
    trigger_value DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### trades (交易记录)
```sql
CREATE TABLE trades (
    id SERIAL PRIMARY KEY,
    signal_id INTEGER REFERENCES signals(id),
    bond_code VARCHAR(20),
    order_id VARCHAR(50),
    order_volume INTEGER,
    order_price DECIMAL(10,2),
    executed_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## 🎯 核心业务逻辑

### 信号检测算法

#### 涨停信号
```python
def detect_limit_up(price_data: List[PriceTick]) -> bool:
    """检测涨停信号"""
    if not price_data:
        return False

    current_price = price_data[-1].price
    prev_close = price_data[-2].price if len(price_data) > 1 else current_price

    # 计算涨跌幅
    change_percent = (current_price - prev_close) / prev_close * 100

    # 涨停阈值 (不同市场不同)
    limit_up_threshold = 10.0  # A股涨停10%

    return change_percent >= limit_up_threshold
```

#### 大涨信号
```python
def detect_big_rise(price_data: List[PriceTick], time_window: int = 5) -> bool:
    """检测大涨信号 (5分钟内涨幅超过3%)"""
    if len(price_data) < time_window:
        return False

    # 获取时间窗口内的价格
    window_prices = price_data[-time_window:]
    start_price = window_prices[0].price
    end_price = window_prices[-1].price

    # 计算涨幅
    rise_percent = (end_price - start_price) / start_price * 100

    return rise_percent >= 3.0
```

### 数据清理策略

#### 自动清理
- **价格数据**：保留24小时
- **信号记录**：已执行保留24小时，未执行保留6小时
- **交易记录**：保留7天

#### 手动清理
支持自定义清理范围：
- 时间范围：最近N小时/日期范围
- 数据类型：信号/交易/缓存
- 预览模式：先预览再执行

## 🚀 部署指南

### Railway 后端部署
1. 连接GitHub仓库
2. 配置环境变量
3. 部署服务
4. 配置数据库

### Vercel 前端部署
1. 连接GitHub仓库
2. 配置环境变量
3. 自动部署

## 📊 监控和维护

### 系统监控
- 数据库容量监控
- API响应时间
- 信号检测准确率
- 交易执行成功率

### 日志管理
- 应用日志
- 错误日志
- 交易日志
- 清理日志

## 🔒 安全考虑

### API安全
- 请求频率限制
- 输入验证
- 错误信息过滤

### 数据安全
- 敏感信息加密
- 访问权限控制
- 数据备份

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

项目维护者 - your-email@example.com

项目链接: [https://github.com/your-username/bond-monitoring-platform](https://github.com/your-username/bond-monitoring-platform)
