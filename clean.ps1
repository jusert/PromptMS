# clean.ps1
Write-Host "cleaning backend..." -ForegroundColor Cyan

# 删除常见的 Python 虚拟环境和缓存
Remove-Item -Path "backend/.venv" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/__pycache__" -Recurse -Force -ErrorAction SilentlyContinue

# 递归删除所有 .pyc 文件
Get-ChildItem -Path "backend" -Filter "*.pyc" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue

# --- 新增内容：清理打包产生的 build 目录和 .spec 文件 ---
Write-Host "cleaning build artifacts..." -ForegroundColor Cyan

# 删除 build 文件夹 (通常在项目根目录或 backend 目录下)
Remove-Item -Path "build" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "backend/build" -Recurse -Force -ErrorAction SilentlyContinue

# 递归删除所有 .spec 文件
Get-ChildItem -Path "." -Filter "*.spec" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue
# ---------------------------------------------------

Write-Host "cleaning database..." -ForegroundColor Cyan
Get-ChildItem -Path "backend/database" -Filter "*.db" -Recurse | Remove-Item -Force -ErrorAction SilentlyContinue

Write-Host "leaning frontend..." -ForegroundColor Cyan
Remove-Item -Path "frontend/node_modules" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "frontend/dist" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "frontend/.vscode" -Recurse -Force -ErrorAction SilentlyContinue

Write-Host "clean done" -ForegroundColor Green