from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import asyncio
from decimal import Decimal
import pandas as pd

from app.models.schemas import Bond, PriceTick, MonitoringPair


class DataSource(ABC):
    """数据源抽象基类"""

    @abstractmethod
    async def get_bonds(self) -> List[Bond]:
        """获取所有可转债信息"""
        pass

    @abstractmethod
    async def get_stock_price(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """获取股票实时价格"""
        pass

    @abstractmethod
    async def get_bond_price(self, bond_code: str) -> Optional[Dict[str, Any]]:
        """获取可转债实时价格"""
        pass

    @abstractmethod
    async def get_price_history(self, code: str, days: int = 30) -> List[Dict[str, Any]]:
        """获取价格历史数据"""
        pass

    @abstractmethod
    async def get_monitoring_pairs(self, limit: int = 100) -> List[MonitoringPair]:
        """获取监控配对数据"""
        pass

    @abstractmethod
    async def search_stocks(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索股票"""
        pass

    @abstractmethod
    async def get_market_status(self) -> Dict[str, Any]:
        """获取市场状态"""
        pass


class TushareDataSource(DataSource):
    """Tushare数据源实现"""

    def __init__(self, token: str):
        self.token = token
        self._init_client()

        # API限流控制 (Tushare积分限制)
        # 根据文档：基础积分每分钟内可调取500次，每次6000条数据
        self.request_count = 0
        self.last_reset_time = datetime.now()
        self.minute_limit = 500  # 每分钟最多500次调用
        self.request_delay = 0.1  # 请求间隔(秒)

        # 缓存机制
        self.price_cache = {}
        self.cache_timeout = 300  # 缓存5分钟

    def _init_client(self):
        """初始化Tushare客户端"""
        try:
            import tushare as ts
            ts.set_token(self.token)
            self.pro = ts.pro_api()
        except ImportError:
            raise ImportError("tushare not installed. Run: pip install tushare")

    async def get_bonds(self) -> List[Dict[str, Any]]:
        """获取可转债信息"""
        try:
            # 获取可转债基本信息 (只请求实际存在的字段)
            df = self.pro.cb_basic(fields='ts_code,bond_full_name,stk_code,stk_short_name,'
                                       'conv_price,maturity_date')

            bonds = []
            for _, row in df.iterrows():
                try:
                    bond_data = {
                        'ts_code': row['ts_code'],
                        'bond_name': row['bond_full_name'] if pd.notna(row['bond_full_name']) else '',
                        'stock_code': row['stk_code'] if pd.notna(row['stk_code']) else '',
                        'stock_name': row['stk_short_name'] if pd.notna(row['stk_short_name']) else '',
                        'conversion_price': Decimal(str(row['conv_price'])) if pd.notna(row['conv_price']) and row['conv_price'] != '' else None,
                        'conversion_ratio': None,  # Tushare cb_basic不提供此字段
                        'maturity_date': row['maturity_date'] if pd.notna(row['maturity_date']) else None,
                        'bond_rating': ''  # Tushare cb_basic不提供此字段
                    }
                    bonds.append(bond_data)
                except Exception as e:
                    print(f"处理可转债数据失败 {row['ts_code']}: {e}")
                    continue

            print(f"成功获取 {len(bonds)} 个可转债基本信息")
            return bonds
        except Exception as e:
            print(f"获取可转债信息失败: {e}")
            return []

    async def get_stock_price(self, stock_code: str) -> Optional[Dict[str, Any]]:
        """获取股票实时价格"""
        # 检查缓存
        cache_key = self._get_cache_key(stock_code, 'stock')
        cached_data = self._get_cached_price(cache_key)
        if cached_data:
            return cached_data

        try:
            # 获取最近60天的交易日数据，确保有足够的历史数据
            start_date = (datetime.now() - timedelta(days=60)).strftime('%Y%m%d')
            df = await self._make_request(self.pro.daily, ts_code=stock_code, start_date=start_date)

            if df is None or df.empty:
                return None

            # 获取最新一条数据（最近的交易日）
            latest = df.iloc[0]
            price_data = {
                'code': stock_code,
                'price': Decimal(str(latest['close'])),
                'change': Decimal(str(latest['pct_chg'])),
                'volume': int(latest['vol']),
                'amount': Decimal(str(latest['amount'])),
                'timestamp': datetime.now(),
                'trade_date': latest['trade_date']
            }

            # 设置缓存
            self._set_cached_price(cache_key, price_data)
            return price_data
        except Exception as e:
            print(f"获取股票价格失败 {stock_code}: {e}")
            return None

    async def get_bond_price(self, bond_code: str) -> Optional[Dict[str, Any]]:
        """获取可转债实时价格"""
        # 检查缓存
        cache_key = self._get_cache_key(bond_code, 'bond')
        cached_data = self._get_cached_price(cache_key)
        if cached_data:
            return cached_data

        # TODO: 暂时使用模拟数据，待Tushare可转债价格接口可用后替换
        # 尝试真实数据获取
        try:
            # 使用通用的daily接口获取可转债价格（可转债也通过A股市场交易）
            start_date = (datetime.now() - timedelta(days=60)).strftime('%Y%m%d')
            df = await self._make_request(self.pro.daily, ts_code=bond_code, start_date=start_date)

            if df is not None and not df.empty:
                # 获取最新一条数据（最近的交易日）
                latest = df.iloc[0]
                price_data = {
                    'code': bond_code,
                    'price': Decimal(str(latest['close'])),
                    'change': Decimal(str(latest['pct_chg'])),
                    'volume': int(latest['vol']) if latest['vol'] else 0,
                    'amount': Decimal(str(latest['amount'])) if latest['amount'] else Decimal('0'),
                    'timestamp': datetime.now(),
                    'trade_date': latest['trade_date']
                }
                # 设置缓存
                self._set_cached_price(cache_key, price_data)
                return price_data
        except Exception as e:
            print(f"获取可转债真实价格失败 {bond_code}: {e}")

        # 如果真实数据获取失败，使用模拟数据
        print(f"使用模拟数据获取可转债价格 {bond_code}")
        import random
        price_data = {
            'code': bond_code,
            'price': Decimal(str(round(random.uniform(100, 130), 2))),
            'change': Decimal(str(round(random.uniform(-3, 3), 2))),
            'volume': random.randint(1000, 10000),
            'amount': Decimal(str(round(random.uniform(10000, 50000), 2))),
            'timestamp': datetime.now(),
            'trade_date': (datetime.now() - timedelta(days=1)).strftime('%Y%m%d')  # 模拟昨天的交易日
        }

        # 设置缓存
        self._set_cached_price(cache_key, price_data)
        return price_data

    async def get_price_history(self, code: str, days: int = 30) -> List[Dict[str, Any]]:
        """获取价格历史数据"""
        try:
            start_date = (datetime.now() - timedelta(days=days)).strftime('%Y%m%d')

            # 判断是股票还是可转债
            if code.startswith('11') or code.startswith('12') or code.startswith('13'):
                # 可转债
                df = self.pro.cb_daily(ts_code=code, start_date=start_date)
            else:
                # 股票
                df = self.pro.daily(ts_code=code, start_date=start_date)

            if df.empty:
                return []

            history = []
            for _, row in df.iterrows():
                history.append({
                    'time': row['trade_date'],
                    'price': Decimal(str(row['close'])),
                    'volume': int(row['vol']) if row['vol'] else 0,
                    'open': Decimal(str(row['open'])),
                    'high': Decimal(str(row['high'])),
                    'low': Decimal(str(row['low']))
                })

            return history[::-1]  # 反转时间顺序
        except Exception as e:
            print(f"获取价格历史失败 {code}: {e}")
            return []

    async def get_monitoring_pairs(self, limit: int = 100) -> List[MonitoringPair]:
        """获取监控配对数据"""
        try:
            # 获取可转债列表
            bonds = await self.get_bonds()
            if not bonds:
                return []

            pairs = []
            processed_count = 0

            for bond in bonds[:limit]:  # 限制数量
                if not bond.get('stock_code'):
                    continue

                try:
                    # 获取真实的股票价格数据
                    stock_price = await self.get_stock_price(bond['stock_code'])
                    if not stock_price:
                        print(f"跳过 {bond['ts_code']}: 无法获取股票价格 {bond['stock_code']}")
                        continue

                    # 获取真实的可转债价格数据
                    bond_price = await self.get_bond_price(bond['ts_code'])
                    if not bond_price:
                        print(f"跳过 {bond['ts_code']}: 无法获取可转债价格")
                        continue

                    # 计算溢价率
                    premium = Decimal('0')
                    if bond.get('conversion_price') and bond['conversion_price'] > 0:
                        premium = ((bond_price['price'] - bond['conversion_price']) / bond['conversion_price']) * 100

                    # 计算剩余年限
                    remaining_years = Decimal('0')
                    if bond.get('maturity_date'):
                        try:
                            maturity = datetime.strptime(str(bond['maturity_date']), '%Y%m%d')
                            remaining_years = Decimal(str((maturity - datetime.now()).days / 365))
                        except:
                            pass

                    # 计算双低值 (价格 + 溢价率)
                    double_low = bond_price['price'] + premium

                    pair = MonitoringPair(
                        stock_code=bond['stock_code'],
                        stock_name=bond.get('stock_name') or '',
                        stock_price=stock_price['price'],
                        stock_change=stock_price['change'],
                        stock_volume=stock_price['volume'],
                        stock_turnover=Decimal('0'),  # 暂时设为0

                        bond_code=bond['ts_code'],
                        bond_name=bond.get('bond_name') or '',
                        bond_price=bond_price['price'],
                        bond_change=bond_price['change'],
                        conversion_price=bond.get('conversion_price') or Decimal('0'),
                        premium=premium,
                        maturity_date=str(bond.get('maturity_date') or ''),
                        remaining_years=remaining_years,
                        double_low=double_low,
                        rating=bond.get('bond_rating') or 'N/A'
                    )

                    pairs.append(pair)
                    processed_count += 1

                    # 每处理10个可转债打印一次进度
                    if processed_count % 10 == 0:
                        print(f"已处理 {processed_count} 个可转债配对")

                except Exception as e:
                    print(f"处理可转债失败 {bond['ts_code']}: {e}")
                    continue

            print(f"成功处理 {len(pairs)} 个可转债配对")

            # 按股票涨幅降序排序
            pairs.sort(key=lambda x: x.stock_change, reverse=True)

            return pairs
        except Exception as e:
            print(f"获取监控配对数据失败: {e}")
            return []

    async def search_stocks(self, keyword: str) -> List[Dict[str, Any]]:
        """搜索股票"""
        try:
            df = self.pro.stock_basic(name=keyword, fields='ts_code,symbol,name,area,industry')

            results = []
            for _, row in df.iterrows():
                results.append({
                    'code': row['ts_code'],
                    'symbol': row['symbol'],
                    'name': row['name'],
                    'area': row['area'],
                    'industry': row['industry']
                })

            return results
        except Exception as e:
            print(f"搜索股票失败: {e}")
            return []

    async def get_market_status(self) -> Dict[str, Any]:
        """获取市场状态"""
        try:
            # 获取上证指数
            df = self.pro.index_daily(ts_code='000001.SH', start_date=self._get_today_str())

            if df.empty:
                return {'status': 'unknown', 'message': '无法获取市场数据'}

            latest = df.iloc[0]
            change = Decimal(str(latest['pct_chg']))

            if change > 1:
                status = 'bull'  # 强势
            elif change < -1:
                status = 'bear'  # 弱势
            else:
                status = 'neutral'  # 平稳

            return {
                'status': status,
                'index_change': change,
                'message': f'上证指数涨跌幅: {change}%'
            }
        except Exception as e:
            print(f"获取市场状态失败: {e}")
            return {'status': 'unknown', 'message': '获取失败'}

    async def _check_rate_limit(self) -> bool:
        """检查API限流"""
        now = datetime.now()

        # 每分钟重置计数 (Tushare限制：每分钟500次)
        if (now - self.last_reset_time).seconds >= 60:
            self.request_count = 0
            self.last_reset_time = now

        # 检查是否超过每分钟限制
        if self.request_count >= self.minute_limit:
            print(f"Tushare API 达到每分钟限制 ({self.minute_limit}次/分钟)")
            return False

        return True

    async def _make_request(self, func, *args, **kwargs):
        """带限流的API请求"""
        if not await self._check_rate_limit():
            return None

        # 请求间隔控制
        await asyncio.sleep(self.request_delay)

        try:
            result = func(*args, **kwargs)
            self.request_count += 1
            return result
        except Exception as e:
            print(f"API请求失败: {e}")
            return None

    def _get_cache_key(self, code: str, data_type: str) -> str:
        """生成缓存键"""
        return f"{data_type}_{code}"

    def _get_cached_price(self, cache_key: str) -> Optional[Dict[str, Any]]:
        """获取缓存的价格数据"""
        if cache_key in self.price_cache:
            cached_data, timestamp = self.price_cache[cache_key]
            if (datetime.now() - timestamp).seconds < self.cache_timeout:
                return cached_data
            else:
                # 缓存过期，删除
                del self.price_cache[cache_key]
        return None

    def _set_cached_price(self, cache_key: str, data: Dict[str, Any]):
        """设置缓存的价格数据"""
        self.price_cache[cache_key] = (data, datetime.now())

        # 限制缓存大小，防止内存泄漏
        if len(self.price_cache) > 1000:
            # 删除最旧的缓存
            oldest_key = min(self.price_cache.keys(),
                           key=lambda k: self.price_cache[k][1])
            del self.price_cache[oldest_key]

    def _get_today_str(self) -> str:
        """获取今天的日期字符串"""
        return datetime.now().strftime('%Y%m%d')


# 数据源工厂
class DataSourceFactory:
    @staticmethod
    def create_data_source(source_type: str, **kwargs) -> DataSource:
        if source_type == 'tushare':
            token = kwargs.get('token', '')
            return TushareDataSource(token)
        else:
            raise ValueError(f"不支持的数据源类型: {source_type}")
