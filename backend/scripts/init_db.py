#!/usr/bin/env python3
"""
数据库初始化脚本
用于创建数据库表和初始数据
"""

import asyncio
import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.database import create_tables
from app.core.config import settings


async def init_database():
    """初始化数据库"""
    print("开始初始化数据库...")

    try:
        # 创建表
        await create_tables()
        print("✅ 数据库表创建成功")

        # 这里可以添加初始数据
        print("✅ 数据库初始化完成")

    except Exception as e:
        print(f"❌ 数据库初始化失败: {e}")
        return False

    return True


if __name__ == "__main__":
    success = asyncio.run(init_database())
    sys.exit(0 if success else 1)
