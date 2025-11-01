import { useState, useEffect } from 'react';
import Head from 'next/head';
import { MonitoringList } from '../components/MonitoringList';
import { DatabaseUsage } from '../components/DatabaseUsage';
import { SystemStatus } from '../components/SystemStatus';
import { DataCleanup } from '../components/DataCleanup';

export default function Home() {
  const [activeTab, setActiveTab] = useState('monitoring');

  const tabs = [
    { id: 'monitoring', label: '监控面板', icon: '📊' },
    { id: 'cleanup', label: '数据清理', icon: '🗑️' },
    { id: 'status', label: '系统状态', icon: '⚙️' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Head>
        <title>可转债信号监控平台</title>
        <meta name="description" content="实时监控股票异动并自动买入可转债" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      {/* 顶部导航栏 */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <div className="flex items-center">
              <h1 className="text-xl font-bold text-gray-900">
                可转债信号监控平台
              </h1>
            </div>

            <div className="flex items-center space-x-4">
              {/* 数据源选择 */}
              <select className="px-3 py-1 border border-gray-300 rounded-md text-sm">
                <option value="tushare">数据源: Tushare</option>
                <option value="thinktrader">数据源: ThinkTrader</option>
              </select>

              {/* 数据库容量显示 */}
              <DatabaseUsage compact />
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex">
          {/* 侧边栏 */}
          <div className="w-64 mr-6">
            <nav className="bg-white rounded-lg shadow-sm border">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full text-left px-4 py-3 flex items-center space-x-3 hover:bg-gray-50 transition-colors ${
                    activeTab === tab.id
                      ? 'bg-blue-50 border-r-2 border-blue-500 text-blue-700'
                      : 'text-gray-700'
                  }`}
                >
                  <span className="text-lg">{tab.icon}</span>
                  <span className="font-medium">{tab.label}</span>
                </button>
              ))}
            </nav>

            {/* 系统状态卡片 */}
            <div className="mt-6">
              <SystemStatus compact />
            </div>
          </div>

          {/* 主内容区域 */}
          <div className="flex-1">
            <div className="bg-white rounded-lg shadow-sm border min-h-[600px]">
              {activeTab === 'monitoring' && <MonitoringList />}
              {activeTab === 'cleanup' && <DataCleanup />}
              {activeTab === 'status' && <SystemStatus />}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
