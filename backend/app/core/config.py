from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    # 数据库配置 - 支持Railway的DATABASE_URL
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///./bond_monitoring.db")

    # Tushare API配置
    tushare_token: str = ""

    # Redis配置 (可选)
    redis_url: Optional[str] = None

    # 应用配置
    app_env: str = "development"
    app_port: int = 8000
    app_host: str = "0.0.0.0"

    # 日志配置
    log_level: str = "INFO"
    log_file: str = "logs/app.log"

    # 监控配置
    monitoring_interval: int = 60  # 价格监控间隔(秒)
    signal_check_interval: int = 30  # 信号检测间隔(秒)

    # 清理配置
    auto_cleanup_hours: int = 24  # 自动清理间隔(小时)
    price_retention_hours: int = 24  # 价格数据保留时间
    signal_retention_hours: int = 24  # 信号数据保留时间
    trade_retention_days: int = 7  # 交易数据保留时间

    # 交易配置
    trading_enabled: bool = False
    max_order_quantity: int = 1000  # 最大下单数量
    min_order_amount: int = 1000  # 最小下单金额

    class Config:
        env_file = ".env"
        case_sensitive = False


# 全局设置实例
settings = Settings()
