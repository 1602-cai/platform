import { useState, useEffect } from 'react';

interface DatabaseUsageData {
  database: {
    name: string;
    size: string;
    size_mb: number;
    limit_mb: number;
    remaining_mb: number;
    usage_percentage: number;
  };
  tables: Array<{
    name: string;
    size: string;
    size_mb: number;
  }>;
  record_counts: Array<{
    table: string;
    count: number;
  }>;
  last_updated: string;
}

interface DatabaseUsageProps {
  compact?: boolean;
}

export function DatabaseUsage({ compact = false }: DatabaseUsageProps) {
  const [usageData, setUsageData] = useState<DatabaseUsageData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchUsageData();
    // 每5分钟更新一次
    const interval = setInterval(fetchUsageData, 5 * 60 * 1000);
    return () => clearInterval(interval);
  }, []);

  const fetchUsageData = async () => {
    try {
      const response = await fetch('/api/monitoring/database-usage');
      const data = await response.json();
      setUsageData(data);
    } catch (error) {
      console.error('获取数据库使用情况失败:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className={`${compact ? 'text-sm' : ''} text-gray-500`}>
        加载中...
      </div>
    );
  }

  if (!usageData) {
    return (
      <div className={`${compact ? 'text-sm' : ''} text-red-500`}>
        获取失败
      </div>
    );
  }

  const { database } = usageData;

  if (compact) {
    return (
      <div className="flex items-center space-x-2 text-sm">
        <span className="text-gray-600">容量:</span>
        <span className={`font-medium ${
          database.usage_percentage > 80 ? 'text-red-600' :
          database.usage_percentage > 60 ? 'text-orange-600' :
          'text-green-600'
        }`}>
          {database.usage_percentage.toFixed(1)}%
        </span>
        <span className="text-gray-500">
          ({database.size_mb.toFixed(0)}MB/{database.limit_mb}MB)
        </span>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg border p-6">
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">数据库容量监控</h3>
        <button
          onClick={fetchUsageData}
          className="px-3 py-1 text-sm bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
        >
          刷新
        </button>
      </div>

      {/* 容量概览 */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <span className="text-sm font-medium text-gray-700">使用率</span>
          <span className={`text-sm font-bold ${
            database.usage_percentage > 80 ? 'text-red-600' :
            database.usage_percentage > 60 ? 'text-orange-600' :
            'text-green-600'
          }`}>
            {database.usage_percentage.toFixed(1)}%
          </span>
        </div>

        {/* 进度条 */}
        <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
          <div
            className={`h-3 rounded-full transition-all duration-300 ${
              database.usage_percentage > 80 ? 'bg-red-500' :
              database.usage_percentage > 60 ? 'bg-orange-500' :
              'bg-green-500'
            }`}
            style={{ width: `${Math.min(database.usage_percentage, 100)}%` }}
          ></div>
        </div>

        <div className="flex justify-between text-sm text-gray-600">
          <span>{database.size} 已使用</span>
          <span>{database.remaining_mb.toFixed(1)}MB 剩余</span>
        </div>
      </div>

      {/* 表大小统计 */}
      <div className="mb-6">
        <h4 className="text-sm font-medium text-gray-700 mb-3">各表存储情况</h4>
        <div className="space-y-2">
          {usageData.tables.slice(0, 5).map((table) => (
            <div key={table.name} className="flex justify-between items-center text-sm">
              <span className="text-gray-600 truncate" style={{ maxWidth: '120px' }}>
                {table.name}
              </span>
              <span className="font-medium text-gray-900">
                {table.size_mb.toFixed(1)}MB
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 记录数统计 */}
      <div className="mb-4">
        <h4 className="text-sm font-medium text-gray-700 mb-3">数据记录统计</h4>
        <div className="grid grid-cols-2 gap-2">
          {usageData.record_counts.map((record) => (
            <div key={record.table} className="flex justify-between items-center text-sm">
              <span className="text-gray-600 capitalize">
                {record.table.replace('_', ' ')}:
              </span>
              <span className="font-medium text-gray-900">
                {record.count.toLocaleString()}
              </span>
            </div>
          ))}
        </div>
      </div>

      {/* 最后更新时间 */}
      <div className="text-xs text-gray-500 text-right">
        最后更新: {new Date(usageData.last_updated).toLocaleString('zh-CN')}
      </div>

      {/* 容量警告 */}
      {database.usage_percentage > 80 && (
        <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-md">
          <div className="flex items-center">
            <span className="text-red-600 mr-2">⚠️</span>
            <span className="text-sm text-red-800">
              数据库容量使用率过高，建议及时清理数据
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
