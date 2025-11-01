import Head from 'next/head';

export default function Test() {
  return (
    <div className="min-h-screen bg-gray-50 flex items-center justify-center">
      <Head>
        <title>测试页面 - 可转债监控平台</title>
        <meta name="description" content="测试页面" />
      </Head>

      <div className="max-w-md mx-auto bg-white rounded-lg shadow-lg p-8">
        <h1 className="text-2xl font-bold text-center text-gray-900 mb-4">
          🎉 部署成功！
        </h1>
        <p className="text-gray-600 text-center mb-6">
          Vercel部署正常工作
        </p>
        <div className="text-center">
          <a
            href="/"
            className="inline-block bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-4 rounded-lg transition-colors"
          >
            返回主页
          </a>
        </div>
      </div>
    </div>
  );
}
