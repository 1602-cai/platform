from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime
from decimal import Decimal


# 基础数据模型
class BondBase(BaseModel):
    ts_code: str = Field(..., description="TS代码")
    bond_name: Optional[str] = Field(None, description="债券名称")
    stock_code: Optional[str] = Field(None, description="正股代码")
    stock_name: Optional[str] = Field(None, description="正股名称")
    conversion_price: Optional[Decimal] = Field(None, description="转股价")
    conversion_ratio: Optional[Decimal] = Field(None, description="转股比例")
    maturity_date: Optional[datetime] = Field(None, description="到期日期")
    bond_rating: Optional[str] = Field(None, description="债券评级")


class Bond(BondBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PriceTickBase(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    price: Decimal = Field(..., description="价格")
    volume: Optional[int] = Field(None, description="成交量")
    amount: Optional[Decimal] = Field(None, description="成交额")
    data_source: str = Field("tushare", description="数据源")


class PriceTick(PriceTickBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True


class SignalBase(BaseModel):
    stock_code: str = Field(..., description="股票代码")
    bond_code: Optional[str] = Field(None, description="可转债代码")
    signal_type: str = Field(..., description="信号类型")  # limit_up, big_rise, volume_spike
    trigger_value: Optional[Decimal] = Field(None, description="触发值")
    trigger_price: Optional[Decimal] = Field(None, description="触发价格")


class Signal(SignalBase):
    id: int
    status: str = "pending"
    retry_count: int = 0
    error_message: Optional[str] = None
    created_at: datetime
    processed_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class TradeBase(BaseModel):
    signal_id: Optional[int] = Field(None, description="信号ID")
    bond_code: str = Field(..., description="可转债代码")
    order_type: str = Field(..., description="订单类型")  # buy, sell
    order_volume: int = Field(..., description="订单数量")
    order_price: Decimal = Field(..., description="订单价格")


class Trade(TradeBase):
    id: int
    order_id: Optional[str] = None
    order_status: str = "pending"
    executed_volume: Optional[int] = None
    executed_price: Optional[Decimal] = None
    executed_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True


# API请求/响应模型
class MonitoringPair(BaseModel):
    """监控配对数据"""
    stock_code: str
    stock_name: str
    stock_price: Decimal
    stock_change: Decimal  # 涨跌幅
    stock_volume: Optional[int]
    stock_turnover: Optional[Decimal]  # 换手率

    bond_code: str
    bond_name: str
    bond_price: Decimal
    bond_change: Decimal  # 涨跌幅
    conversion_price: Decimal
    premium: Decimal  # 溢价率
    maturity_date: str
    remaining_years: Decimal
    double_low: Decimal  # 双低值
    rating: str

    signal_type: Optional[str] = None  # 信号类型
    is_favorite: bool = False

    class Config:
        from_attributes = True


class MonitoringResponse(BaseModel):
    """监控数据响应"""
    data: List[MonitoringPair]
    total: int
    page: int = 1
    page_size: int = 20


class CleanupRequest(BaseModel):
    """数据清理请求"""
    data_types: List[str] = Field(..., description="要清理的数据类型")  # signals, trades, price_cache
    time_range: Dict[str, Any] = Field(..., description="时间范围")
    signal_filters: Optional[Dict[str, bool]] = Field(default=None, description="信号过滤")
    preview_only: bool = Field(True, description="是否仅预览")


class CleanupResponse(BaseModel):
    """数据清理响应"""
    signals_deleted: int = 0
    trades_deleted: int = 0
    prices_deleted: int = 0
    cache_cleared: bool = False
    preview_data: Optional[Dict[str, Any]] = None


class DatabaseUsage(BaseModel):
    """数据库使用情况"""
    database: Dict[str, Any]
    tables: List[Dict[str, Any]]
    record_counts: List[Dict[str, Any]]
    last_updated: str


class TradeRequest(BaseModel):
    """交易请求"""
    bond_code: str
    order_type: str = "buy"
    quantity: int
    price: Optional[Decimal] = None


class TradeResponse(BaseModel):
    """交易响应"""
    success: bool
    order_id: Optional[str] = None
    message: str
    executed_quantity: Optional[int] = None
    executed_price: Optional[Decimal] = None


# 图表数据模型
class ChartDataPoint(BaseModel):
    time: str
    price: Decimal
    volume: Optional[int] = None
    ma5: Optional[Decimal] = None
    ma10: Optional[Decimal] = None
    ma20: Optional[Decimal] = None


class DetailChartData(BaseModel):
    stock_chart: List[ChartDataPoint]
    bond_chart: List[ChartDataPoint]
    time_range: str  # 1d, 5d, 1M, 3M, 1Y


# 系统状态模型
class SystemStatus(BaseModel):
    monitoring_active: bool
    total_signals_today: int
    executed_trades_today: int
    pending_signals: int
    database_usage_percent: Decimal
    last_update: datetime
