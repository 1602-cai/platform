from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import datetime

from app.core.database import get_db
from app.models.schemas import (
    MonitoringResponse, MonitoringPair, DatabaseUsage,
    CleanupRequest, CleanupResponse, SystemStatus
)
from app.services.data_source import DataSourceFactory
from app.core.config import settings

router = APIRouter()

# 创建数据源实例
data_source = DataSourceFactory.create_data_source(
    'tushare',
    token=settings.tushare_token
)


@router.get("/pairs", response_model=MonitoringResponse)
async def get_monitoring_pairs(
    limit: int = Query(50, ge=1, le=200, description="返回数量限制"),
    sort_by: str = Query("stock_change", description="排序字段"),
    sort_order: str = Query("desc", description="排序顺序"),
    signal_filter: Optional[str] = Query(None, description="信号过滤")
):
    """获取监控配对数据"""
    try:
        pairs = await data_source.get_monitoring_pairs(limit=limit * 2)  # 获取更多用于筛选

        # 应用筛选
        if signal_filter == "with_signal":
            pairs = [p for p in pairs if p.signal_type]
        elif signal_filter == "no_signal":
            pairs = [p for p in pairs if not p.signal_type]

        # 应用排序
        reverse = sort_order == "desc"
        if sort_by == "stock_change":
            pairs.sort(key=lambda x: x.stock_change, reverse=reverse)
        elif sort_by == "bond_change":
            pairs.sort(key=lambda x: x.bond_change, reverse=reverse)
        elif sort_by == "premium":
            pairs.sort(key=lambda x: x.premium, reverse=reverse)
        elif sort_by == "double_low":
            pairs.sort(key=lambda x: x.double_low, reverse=reverse)

        # 限制返回数量
        pairs = pairs[:limit]

        return MonitoringResponse(
            data=pairs,
            total=len(pairs),
            page=1,
            page_size=limit
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取监控数据失败: {str(e)}")


@router.get("/market-status")
async def get_market_status():
    """获取市场状态"""
    try:
        return await data_source.get_market_status()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取市场状态失败: {str(e)}")


@router.get("/database-usage", response_model=DatabaseUsage)
async def get_database_usage(db: AsyncSession = Depends(get_db)):
    """获取数据库使用情况"""
    try:
        from app.core.database import get_db_size
        usage_data = await get_db_size()

        # 计算使用百分比 (Railway Hobby: 512MB)
        railway_limit_mb = 512
        used_mb = usage_data["database"]["size_bytes"] / (1024 * 1024)
        remaining_mb = railway_limit_mb - used_mb
        usage_percentage = (used_mb / railway_limit_mb) * 100

        return DatabaseUsage(
            database={
                "name": usage_data["database"]["name"],
                "size": usage_data["database"]["size"],
                "size_mb": round(used_mb, 2),
                "limit_mb": railway_limit_mb,
                "remaining_mb": round(remaining_mb, 2),
                "usage_percentage": round(usage_percentage, 2)
            },
            tables=[
                {
                    "name": table["name"],
                    "size": table["size"],
                    "size_mb": round(table["size_bytes"] / (1024 * 1024), 2)
                } for table in usage_data["tables"]
            ],
            record_counts=usage_data["record_counts"],
            last_updated=datetime.now().isoformat()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取数据库使用情况失败: {str(e)}")


@router.post("/cleanup", response_model=CleanupResponse)
async def cleanup_data(
    request: CleanupRequest,
    db: AsyncSession = Depends(get_db)
):
    """数据清理"""
    try:
        signals_deleted = 0
        trades_deleted = 0
        prices_deleted = 0

        # 构建时间条件
        time_condition = ""
        if "hours" in request.time_range:
            hours = request.time_range["hours"]
            time_condition = f"AND created_at < NOW() - INTERVAL '{hours} hours'"
        elif "start_date" in request.time_range and "end_date" in request.time_range:
            start_date = request.time_range["start_date"]
            end_date = request.time_range["end_date"]
            time_condition = f"AND created_at BETWEEN '{start_date}' AND '{end_date}'"

        # 清理信号记录
        if "signals" in request.data_types:
            signal_conditions = [time_condition]

            # 信号状态过滤
            if request.signal_filters:
                status_conditions = []
                if request.signal_filters.get("executed"):
                    status_conditions.append("status = 'executed'")
                if request.signal_filters.get("failed"):
                    status_conditions.append("status = 'failed'")
                if request.signal_filters.get("pending"):
                    status_conditions.append("status = 'pending'")

                if status_conditions:
                    signal_conditions.append(f"({' OR '.join(status_conditions)})")

            signal_where = " AND ".join([c for c in signal_conditions if c])
            if signal_where:
                result = await db.execute(f"DELETE FROM signals WHERE {signal_where}")
                signals_deleted = result.rowcount

        # 清理交易记录
        if "trades" in request.data_types:
            trade_where = time_condition.replace("created_at", "created_at")
            if trade_where:
                result = await db.execute(f"DELETE FROM trades WHERE {trade_where}")
                trades_deleted = result.rowcount

        # 清理价格数据
        if "price_cache" in request.data_types:
            price_where = time_condition.replace("created_at", "timestamp")
            if price_where:
                result = await db.execute(f"DELETE FROM price_ticks WHERE {price_where}")
                prices_deleted = result.rowcount

        # 预览模式
        preview_data = None
        if request.preview_only:
            preview_data = {
                "signals_to_delete": signals_deleted,
                "trades_to_delete": trades_deleted,
                "prices_to_delete": prices_deleted
            }
            # 回滚删除操作
            await db.rollback()
            signals_deleted = 0
            trades_deleted = 0
            prices_deleted = 0

        return CleanupResponse(
            signals_deleted=signals_deleted,
            trades_deleted=trades_deleted,
            prices_deleted=prices_deleted,
            cache_cleared="price_cache" in request.data_types and not request.preview_only,
            preview_data=preview_data
        )
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"数据清理失败: {str(e)}")


@router.get("/system-status", response_model=SystemStatus)
async def get_system_status(db: AsyncSession = Depends(get_db)):
    """获取系统状态"""
    try:
        # 获取今日信号统计
        result = await db.execute("""
            SELECT COUNT(*) as total_signals
            FROM signals
            WHERE DATE(created_at) = CURRENT_DATE
        """)
        total_signals_today = result.scalar() or 0

        # 获取今日执行交易统计
        result = await db.execute("""
            SELECT COUNT(*) as executed_trades
            FROM trades
            WHERE DATE(created_at) = CURRENT_DATE
            AND order_status = 'filled'
        """)
        executed_trades_today = result.scalar() or 0

        # 获取待处理信号
        result = await db.execute("""
            SELECT COUNT(*) as pending_signals
            FROM signals
            WHERE status = 'pending'
        """)
        pending_signals = result.scalar() or 0

        # 获取数据库使用率
        usage_data = await get_db_size()
        used_mb = usage_data["database"]["size_bytes"] / (1024 * 1024)
        usage_percentage = (used_mb / 512) * 100  # Railway Hobby 512MB

        return SystemStatus(
            monitoring_active=True,  # 暂时固定为活跃
            total_signals_today=total_signals_today,
            executed_trades_today=executed_trades_today,
            pending_signals=pending_signals,
            database_usage_percent=round(usage_percentage, 2),
            last_update=datetime.now()
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取系统状态失败: {str(e)}")
