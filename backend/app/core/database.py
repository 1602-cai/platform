from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool
from sqlalchemy import text
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.core.config import settings
from app.models.database import Base

# 创建异步数据库引擎
database_url = settings.database_url
if database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://")
elif database_url.startswith("sqlite://"):
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")

engine = create_async_engine(
    database_url,
    echo=settings.app_env == "development",
    poolclass=NullPool if "postgresql" in database_url else None,  # PostgreSQL使用NullPool
    pool_pre_ping=True,  # 连接前检查
)

# 创建异步会话工厂
async_session_factory = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """获取数据库会话"""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables():
    """创建所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables():
    """删除所有表"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def get_db_size() -> dict:
    """获取数据库大小信息"""
    async with async_session_factory() as session:
        # 检查是否为SQLite
        if "sqlite" in database_url:
            # SQLite数据库大小查询
            import os
            db_path = settings.database_url.replace("sqlite:///", "").replace("sqlite+aiosqlite:///", "")
            if os.path.exists(db_path):
                db_size_bytes = os.path.getsize(db_path)
                db_size_mb = db_size_bytes / (1024 * 1024)

                # 获取各表大小和记录数
                result = await session.execute(text("""
                    SELECT name FROM sqlite_master
                    WHERE type='table' AND name NOT LIKE 'sqlite_%'
                """))
                table_names = [row[0] for row in result.fetchall()]

                tables = []
                record_counts = []

                for table_name in table_names:
                    # 获取表记录数
                    result = await session.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    count = result.scalar() or 0
                    record_counts.append({"table": table_name, "count": count})

                    # 估算表大小 (SQLite没有精确的表大小查询，这里用估算值)
                    estimated_size = count * 100  # 粗略估算每条记录100字节
                    tables.append({
                        "name": table_name,
                        "size": f"{estimated_size / (1024*1024):.1f} MB",
                        "size_bytes": estimated_size
                    })

                return {
                    "database": {
                        "name": "bond_monitoring.db",
                        "size": f"{db_size_mb:.1f} MB",
                        "size_bytes": db_size_bytes
                    },
                    "tables": tables,
                    "record_counts": record_counts
                }
            else:
                return {
                    "database": {"name": "bond_monitoring.db", "size": "0 MB", "size_bytes": 0},
                    "tables": [],
                    "record_counts": []
                }
        else:
            # PostgreSQL数据库大小查询
            result = await session.execute("""
                SELECT
                    current_database() as db_name,
                    pg_size_pretty(pg_database_size(current_database())) as db_size,
                    pg_database_size(current_database()) as db_size_bytes
            """)
            db_info = result.first()

            # 获取各表大小
            result = await session.execute("""
                SELECT
                    schemaname,
                    tablename,
                    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as table_size,
                    pg_total_relation_size(schemaname||'.'||tablename) as table_size_bytes
                FROM pg_tables
                WHERE schemaname = 'public'
                ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC
            """)
            tables = result.fetchall()

            # 获取记录数统计
            result = await session.execute("""
                SELECT
                    'bonds' as table_name, COUNT(*) as count FROM bonds
                UNION ALL
                SELECT 'price_ticks' as table_name, COUNT(*) as count FROM price_ticks
                UNION ALL
                SELECT 'signals' as table_name, COUNT(*) as count FROM signals
                UNION ALL
                SELECT 'trades' as table_name, COUNT(*) as count FROM trades
                UNION ALL
                SELECT 'system_snapshots' as table_name, COUNT(*) as count FROM system_snapshots
            """)
            record_counts = result.fetchall()

            return {
                "database": {
                    "name": db_info.db_name,
                    "size": db_info.db_size,
                    "size_bytes": db_info.db_size_bytes
                },
                "tables": [
                    {
                        "name": table.tablename,
                        "size": table.table_size,
                        "size_bytes": table.table_size_bytes
                    } for table in tables
                ],
                "record_counts": [
                    {"table": record.table_name, "count": record.count}
                    for record in record_counts
                ]
            }
