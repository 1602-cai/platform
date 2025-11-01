import { useState, useEffect } from 'react';

interface CleanupStats {
  total_records: number;
  old_records: number;
  last_cleanup: string;
  next_cleanup: string;
}

interface CleanupResult {
  success: boolean;
  message: string;
  deleted_count: number;
}

export function DataCleanup() {
  const [stats, setStats] = useState<CleanupStats | null>(null);
  const [loading, setLoading] = useState(true);
  const [cleaning, setCleaning] = useState(false);
  const [result, setResult] = useState<CleanupResult | null>(null);

  useEffect(() => {
    fetchCleanupStats();
  }, []);

  const fetchCleanupStats = async () => {
    try {
      // 这里可以调用后端API获取清理统计信息
      // 暂时使用模拟数据
      setStats({
        total_records: 15420,
        old_records: 2340,
        last_cleanup: '2025-11-01 08:00:00',
        next_cleanup: '2025-11-02 08:00:00'
      });
    } catch (error) {
      console.error('获取清理统计失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const performCleanup = async () => {
    setCleaning(true);
    setResult(null);

    try {
      // 这里可以调用后端API执行数据清理
      // 暂时模拟清理过程
      await new Promise(resolve => setTimeout(resolve, 2000));

      setResult({
        success: true,
        message: '数据清理完成',
        deleted_count: 2340
      });

      // 重新获取统计信息
      await fetchCleanupStats();
    } catch (error) {
      setResult({
        success: false,
        message: '数据清理失败，请重试',
        deleted_count: 0
      });
    } finally {
      setCleaning(false);
    }
  };

  const scheduleCleanup = async () => {
    try {
      // 这里可以调用后端API设置定时清理
      alert('定时清理功能开发中...');
    } catch (error) {
      console.error('设置定时清理失败:', error);
    }
  };

  return (
    <div className="p-6">
      <div className="mb-6">
        <h2 className="text-2xl font-bold text-gray-900 mb-2">数据清理管理</h2>
        <p className="text-gray-600">清理过期数据，优化数据库性能</p>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
        </div>
      ) : (
        <div className="space-y-6">
          {/* 统计信息卡片 */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-white rounded-lg shadow-sm border p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">总记录数</p>
                  <p className="text-2xl font-bold text-gray-900">
                    {stats?.total_records?.toLocaleString() || 0}
                  </p>
                </div>
                <div className="text-blue-500">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">可清理记录</p>
                  <p className="text-2xl font-bold text-orange-600">
                    {stats?.old_records?.toLocaleString() || 0}
                  </p>
                </div>
                <div className="text-orange-500">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.732 16.5c-.77.833.192 2.5 1.732 2.5z" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">上次清理</p>
                  <p className="text-sm font-bold text-gray-900">
                    {stats?.last_cleanup ? new Date(stats.last_cleanup).toLocaleString() : '从未清理'}
                  </p>
                </div>
                <div className="text-green-500">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm border p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">下次清理</p>
                  <p className="text-sm font-bold text-gray-900">
                    {stats?.next_cleanup ? new Date(stats.next_cleanup).toLocaleString() : '未设置'}
                  </p>
                </div>
                <div className="text-blue-500">
                  <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
              </div>
            </div>
          </div>

          {/* 清理操作区域 */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">清理操作</h3>
            </div>
            <div className="px-6 py-6">
              <div className="space-y-4">
                {/* 手动清理 */}
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">手动清理</h4>
                    <p className="text-sm text-gray-600">立即清理过期数据（30天前的历史数据）</p>
                  </div>
                  <button
                    onClick={performCleanup}
                    disabled={cleaning}
                    className={`px-4 py-2 text-sm font-medium rounded-md ${
                      cleaning
                        ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                        : 'bg-red-600 text-white hover:bg-red-700'
                    }`}
                  >
                    {cleaning ? '清理中...' : '立即清理'}
                  </button>
                </div>

                {/* 定时清理设置 */}
                <div className="flex items-center justify-between p-4 border border-gray-200 rounded-lg">
                  <div>
                    <h4 className="text-sm font-medium text-gray-900">定时清理</h4>
                    <p className="text-sm text-gray-600">设置每日自动清理过期数据</p>
                  </div>
                  <button
                    onClick={scheduleCleanup}
                    className="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 border border-blue-200 rounded-md hover:bg-blue-100"
                  >
                    设置定时
                  </button>
                </div>
              </div>

              {/* 清理结果 */}
              {result && (
                <div className={`mt-4 p-4 rounded-md ${
                  result.success
                    ? 'bg-green-50 border border-green-200'
                    : 'bg-red-50 border border-red-200'
                }`}>
                  <div className="flex">
                    <div className="flex-shrink-0">
                      {result.success ? (
                        <svg className="h-5 w-5 text-green-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                      ) : (
                        <svg className="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                          <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                        </svg>
                      )}
                    </div>
                    <div className="ml-3">
                      <p className={`text-sm font-medium ${
                        result.success ? 'text-green-800' : 'text-red-800'
                      }`}>
                        {result.message}
                      </p>
                      {result.deleted_count > 0 && (
                        <p className="text-sm text-gray-600 mt-1">
                          已删除 {result.deleted_count.toLocaleString()} 条记录
                        </p>
                      )}
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* 清理历史记录 */}
          <div className="bg-white rounded-lg shadow-sm border">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">清理历史</h3>
            </div>
            <div className="px-6 py-4">
              <div className="space-y-3">
                <div className="flex items-center justify-between py-2">
                  <div>
                    <p className="text-sm font-medium text-gray-900">2025-11-01 08:00:00</p>
                    <p className="text-xs text-gray-600">清理了 2,340 条过期记录</p>
                  </div>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    成功
                  </span>
                </div>
                <div className="flex items-center justify-between py-2">
                  <div>
                    <p className="text-sm font-medium text-gray-900">2025-10-31 08:00:00</p>
                    <p className="text-xs text-gray-600">清理了 1,890 条过期记录</p>
                  </div>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    成功
                  </span>
                </div>
                <div className="flex items-center justify-between py-2">
                  <div>
                    <p className="text-sm font-medium text-gray-900">2025-10-30 08:00:00</p>
                    <p className="text-xs text-gray-600">清理了 2,156 条过期记录</p>
                  </div>
                  <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    成功
                  </span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
