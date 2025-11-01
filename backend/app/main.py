from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
import logging

from app.core.config import settings
from app.core.database import create_tables
from app.api.monitoring import router as monitoring_router

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    logger.info("启动可转债监控平台...")

    # 启动时创建数据库表
    try:
        await create_tables()
        logger.info("数据库表创建完成")
    except Exception as e:
        logger.error(f"数据库表创建失败: {e}")

    yield

    logger.info("关闭可转债监控平台...")


# 创建FastAPI应用
app = FastAPI(
    title="可转债信号监控平台",
    description="实时监控股票异动并自动买入对应可转债的量化交易平台",
    version="1.0.0",
    lifespan=lifespan
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(
    monitoring_router,
    prefix="/api/monitoring",
    tags=["monitoring"]
)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "可转债信号监控平台 API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",  # 应该使用实际时间
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host=settings.app_host,
        port=settings.app_port,
        reload=settings.app_env == "development",
        log_level=settings.log_level.lower()
    )
