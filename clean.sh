#!/usr/bin/env bash

# 遇到错误立即停止执行
set -e

# 删除 backend 目录下的环境依赖等
echo -e "cleaning backend... "
rm -rf backend/.venv
find backend -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
find backend -name "*.pyc" -type f -delete 2>/dev/null || true

# 删除 frontend 目录下的环境依赖等
echo -e "cleaning frontend... "
rm -rf frontend/node_modules
rm -rf frontend/.vscode

# 删除打包文件
echo -e "cleaning build... "
rm -rf build
rm -rf backend/build
rm -rf dist
rm -rf backend/dist
find . -name "*.spec" -type f -delete 2>/dev/null || true
rm -rf frontend/dist

# 删除数据库文件
echo -e "cleaning database... "
find database -name "*.db" -type f -delete 2>/dev/null || true

echo -e "clean done "