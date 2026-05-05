/** @type {import('next').NextConfig} */
const nextConfig = {
  // 'standalone' is for Docker only — removed for AWS Amplify SSR (WEB_COMPUTE)
  eslint: {
    ignoreDuringBuilds: true,
  },
};

export default nextConfig;
