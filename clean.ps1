# 遇到错误立即停止执行
$ErrorActionPreference = "Stop"

# 删除 backend 目录下的环境依赖等
Write-Host "cleaning backend... "
Remove-Item -Path "backend/.venv" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "backend" -Filter "__pycache__" -Recurse -Directory | Remove-Item -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "backend" -Filter "*.pyc" -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue

# 删除 frontend 目录下的环境依赖等
Write-Host "cleaning frontend... "
Remove-Item -Path "frontend/node_modules" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "frontend/.vscode" -Recurse -Force -ErrorAction SilentlyContinue

# 删除打包文件
Write-Host "cleaning build... "
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/dist" -Recurse -Force -ErrorAction SilentlyContinue
Get-ChildItem -Path "." -Filter "*.spec" -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue
Remove-Item -Path "frontend/dist" -Recurse -Force -ErrorAction SilentlyContinue

# 删除数据库文件
Write-Host "cleaning database... "
Get-ChildItem -Path "database" -Filter "*.db" -Recurse -File | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "clean done "