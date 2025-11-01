/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: true,
  // API代理由vercel.json处理，避免冲突
};

module.exports = nextConfig;
