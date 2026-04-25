const path = require("path");

const nextConfig = {
  outputFileTracingRoot: path.join(__dirname),
  poweredByHeader: false,
  reactStrictMode: true
};

module.exports = nextConfig;
