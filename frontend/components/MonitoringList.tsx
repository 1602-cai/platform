import { useState, useEffect } from 'react';

interface MonitoringPair {
  stock_code: string;
  stock_name: string;
  stock_price: number;
  stock_change: number;
  stock_volume?: number;
  stock_turnover?: number;
  bond_code: string;
  bond_name: string;
  bond_price: number;
  bond_change: number;
  conversion_price: number;
  premium: number;
  maturity_date: string;
  remaining_years: number;
  double_low: number;
  rating: string;
  signal_type?: string;
  is_favorite: boolean;
}

export function MonitoringList() {
  const [pairs, setPairs] = useState<MonitoringPair[]>([]);
  const [loading, setLoading] = useState(true);
  const [sortBy, setSortBy] = useState('stock_change');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const [signalFilter, setSignalFilter] = useState('all');

  // 获取监控数据
  const fetchData = async () => {
    try {
      const params = new URLSearchParams({
        limit: '50',
        sort_by: sortBy,
        sort_order: sortOrder,
        signal_filter: signalFilter,
      });

      const apiUrl = process.env.NEXT_PUBLIC_API_URL || '';
      const response = await fetch(`${apiUrl}/api/monitoring/pairs?${params}`);
      const data = await response.json();
      setPairs(data.data || []);
    } catch (error) {
      console.error('获取监控数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    // 每30秒自动刷新
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [sortBy, sortOrder, signalFilter]);

  const handleSort = (field: string) => {
    if (sortBy === field) {
      setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc');
    } else {
      setSortBy(field);
      setSortOrder('desc');
    }
  };

  const toggleFavorite = (stockCode: string) => {
    setPairs(pairs.map(pair =>
      pair.stock_code === stockCode
        ? { ...pair, is_favorite: !pair.is_favorite }
        : pair
    ));
  };

  if (loading) {
    return (
      <div className="p-6">
        <div className="animate-pulse space-y-4">
          {[...Array(5)].map((_, i) => (
            <div key={i} className="h-32 bg-gray-200 rounded-lg"></div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-gray-900">监控面板</h2>

        {/* 控制栏 */}
        <div className="flex items-center space-x-4">
          {/* 信号筛选 */}
          <select
            value={signalFilter}
            onChange={(e) => setSignalFilter(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm"
          >
            <option value="all">全部信号</option>
            <option value="with_signal">有信号</option>
            <option value="no_signal">无信号</option>
          </select>

          {/* 排序选择 */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm"
          >
            <option value="stock_change">股票涨幅</option>
            <option value="bond_change">可转债涨幅</option>
            <option value="premium">溢价率</option>
            <option value="double_low">双低值</option>
          </select>

          {/* 排序方向 */}
          <button
            onClick={() => setSortOrder(sortOrder === 'asc' ? 'desc' : 'asc')}
            className="px-3 py-2 border border-gray-300 rounded-md text-sm hover:bg-gray-50"
          >
            {sortOrder === 'asc' ? '↑' : '↓'}
          </button>
        </div>
      </div>

      {/* 数据列表 */}
      <div className="space-y-4">
        {pairs.map((pair) => (
          <BondStockCard
            key={pair.stock_code}
            pair={pair}
            onToggleFavorite={toggleFavorite}
          />
        ))}
      </div>

      {pairs.length === 0 && (
        <div className="text-center py-12 text-gray-500">
          暂无监控数据
        </div>
      )}
    </div>
  );
}

interface BondStockCardProps {
  pair: MonitoringPair;
  onToggleFavorite: (stockCode: string) => void;
}

function BondStockCard({ pair, onToggleFavorite }: BondStockCardProps) {
  return (
    <div className="bg-white border border-gray-200 rounded-lg p-6 hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        {/* 股票信息 */}
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">
              {pair.stock_name}
            </h3>
            <span className="text-sm text-gray-500">{pair.stock_code}</span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              pair.stock_change >= 0 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
            }`}>
              {pair.stock_change >= 0 ? '+' : ''}{pair.stock_change}%
            </span>
          </div>
          <div className="text-2xl font-bold text-gray-900 mb-1">
            ¥{pair.stock_price.toFixed(2)}
          </div>
          <div className="text-sm text-gray-600">
            成交量: {pair.stock_volume?.toLocaleString() || 'N/A'}
          </div>
        </div>

        {/* 信号指示器 */}
        <div className="flex items-center px-4">
          {pair.signal_type && (
            <div className={`px-3 py-1 rounded-full text-sm font-medium ${
              pair.signal_type === 'limit_up' ? 'bg-red-500 text-white' :
              pair.signal_type === 'big_rise' ? 'bg-orange-500 text-white' :
              'bg-yellow-500 text-black'
            }`}>
              {pair.signal_type === 'limit_up' ? '🚀涨停' :
               pair.signal_type === 'big_rise' ? '📈大涨' :
               '⚡异动'}
            </div>
          )}
        </div>

        {/* 可转债信息 */}
        <div className="flex-1">
          <div className="flex items-center space-x-3 mb-2">
            <h3 className="text-lg font-semibold text-gray-900">
              {pair.bond_name}
            </h3>
            <span className="text-sm text-gray-500">{pair.bond_code}</span>
            <span className={`px-2 py-1 rounded-full text-xs font-medium ${
              pair.bond_change >= 0 ? 'bg-red-100 text-red-800' : 'bg-green-100 text-green-800'
            }`}>
              {pair.bond_change >= 0 ? '+' : ''}{pair.bond_change}%
            </span>
          </div>
          <div className="text-2xl font-bold text-gray-900 mb-1">
            ¥{pair.bond_price.toFixed(2)}
          </div>
          <div className="grid grid-cols-2 gap-2 text-sm">
            <div>
              <span className="text-gray-500">转股价:</span>
              <span className="ml-1 font-medium">¥{pair.conversion_price.toFixed(2)}</span>
            </div>
            <div>
              <span className="text-gray-500">溢价率:</span>
              <span className={`ml-1 font-medium ${
                pair.premium > 50 ? 'text-red-600' :
                pair.premium > 20 ? 'text-orange-600' : 'text-green-600'
              }`}>
                {pair.premium.toFixed(1)}%
              </span>
            </div>
            <div>
              <span className="text-gray-500">到期日:</span>
              <span className="ml-1 font-medium">{pair.maturity_date}</span>
            </div>
            <div>
              <span className="text-gray-500">双低值:</span>
              <span className={`ml-1 font-medium ${
                pair.double_low < 100 ? 'text-blue-600' : 'text-gray-600'
              }`}>
                {pair.double_low.toFixed(1)}
              </span>
            </div>
          </div>
        </div>

        {/* 操作按钮 */}
        <div className="flex flex-col space-y-2 ml-4">
          <button
            onClick={() => window.open(`/detail/${pair.stock_code}`, '_blank')}
            className="px-4 py-2 bg-blue-500 text-white rounded-md hover:bg-blue-600 transition-colors text-sm font-medium"
          >
            📊 详情
          </button>
          <button
            onClick={() => onToggleFavorite(pair.stock_code)}
            className={`px-4 py-2 rounded-md transition-colors text-sm font-medium ${
              pair.is_favorite
                ? 'bg-yellow-500 text-white hover:bg-yellow-600'
                : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
            }`}
          >
            {pair.is_favorite ? '⭐ 已收藏' : '☆ 收藏'}
          </button>
          {pair.signal_type && (
            <button
              className="px-4 py-2 bg-green-500 text-white rounded-md hover:bg-green-600 transition-colors text-sm font-medium"
            >
              💰 交易
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
