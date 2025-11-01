from sqlalchemy import Column, Integer, String, DECIMAL, TIMESTAMP, BIGINT, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Bond(Base):
    """可转债基础信息表"""
    __tablename__ = "bonds"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ts_code = Column(String(20), unique=True, nullable=False, comment="TS代码")
    bond_name = Column(String(100), comment="债券名称")
    stock_code = Column(String(20), comment="正股代码")
    stock_name = Column(String(100), comment="正股名称")
    conversion_price = Column(DECIMAL(10, 2), comment="转股价")
    conversion_ratio = Column(DECIMAL(10, 4), comment="转股比例")
    maturity_date = Column(TIMESTAMP, comment="到期日期")
    bond_rating = Column(String(10), comment="债券评级")
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())


class PriceTick(Base):
    """实时价格数据表"""
    __tablename__ = "price_ticks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False, comment="股票代码")
    price = Column(DECIMAL(10, 2), nullable=False, comment="价格")
    volume = Column(BIGINT, comment="成交量")
    amount = Column(DECIMAL(15, 2), comment="成交额")
    timestamp = Column(TIMESTAMP, nullable=False, server_default=func.now(), comment="时间戳")
    data_source = Column(String(20), default="tushare", comment="数据源")


class Signal(Base):
    """信号记录表"""
    __tablename__ = "signals"

    id = Column(Integer, primary_key=True, autoincrement=True)
    stock_code = Column(String(20), nullable=False, comment="股票代码")
    bond_code = Column(String(20), comment="可转债代码")
    signal_type = Column(String(20), comment="信号类型")  # limit_up, big_rise, volume_spike
    trigger_value = Column(DECIMAL(10, 2), comment="触发值")
    trigger_price = Column(DECIMAL(10, 2), comment="触发价格")
    status = Column(String(20), default="pending", comment="状态")  # pending, processing, executed, failed
    retry_count = Column(Integer, default=0, comment="重试次数")
    error_message = Column(String(500), comment="错误信息")
    created_at = Column(TIMESTAMP, server_default=func.now())
    processed_at = Column(TIMESTAMP, comment="处理时间")


class Trade(Base):
    """交易记录表"""
    __tablename__ = "trades"

    id = Column(Integer, primary_key=True, autoincrement=True)
    signal_id = Column(Integer, ForeignKey("signals.id"), comment="信号ID")
    bond_code = Column(String(20), comment="可转债代码")
    order_id = Column(String(50), comment="订单ID")
    order_type = Column(String(10), comment="订单类型")  # buy, sell
    order_volume = Column(Integer, comment="订单数量")
    order_price = Column(DECIMAL(10, 2), comment="订单价格")
    order_status = Column(String(20), comment="订单状态")  # pending, filled, cancelled, rejected
    executed_volume = Column(Integer, comment="已执行数量")
    executed_price = Column(DECIMAL(10, 2), comment="执行价格")
    executed_at = Column(TIMESTAMP, comment="执行时间")
    created_at = Column(TIMESTAMP, server_default=func.now())


class SystemSnapshot(Base):
    """系统状态快照表"""
    __tablename__ = "system_snapshots"

    id = Column(Integer, primary_key=True, autoincrement=True)
    snapshot_type = Column(String(50), comment="快照类型")  # price_cache, signal_stats, system_status
    snapshot_data = Column(String, comment="快照数据JSON")
    created_at = Column(TIMESTAMP, server_default=func.now())


# 创建索引
Index('idx_price_ticks_stock_time', PriceTick.stock_code, PriceTick.timestamp.desc())
Index('idx_signals_status_created', Signal.status, Signal.created_at.desc())
Index('idx_signals_stock_created', Signal.stock_code, Signal.created_at.desc())
Index('idx_trades_signal', Trade.signal_id)
Index('idx_trades_status', Trade.order_status)
