# 🚀 PromptMS — Prompt 管理工具

PromptMS 是一个基于 **FastAPI + Vue** 构建的提示词管理工具，旨在解决 Prompt 分散、难复用、版本不可控等问题，支持 Prompt 的结构化管理、版本控制与组合调用，适用于 AI Agent 与 Prompt Engineering 场景。

------

## 🧱 技术栈

### 后端

- FastAPI
- SQLite / SQLAlchemy
- uv（Python 依赖管理）
- PyInstaller（打包发布）

### 前端

- Vue 3
- Vite
- Axios

------

## ⚙️ 项目环境安装

### 后端环境

```bash
cd backend
uv venv
uv sync
```


### 前端环境

```bash
cd frontend
npm install
```

------

## ▶️ 本地开发运行

### 启动后端

```bash
uv run python -m backend.run
```

默认地址：

```
http://127.0.0.1:8787
```


### 启动前端

```bash
cd frontend
npm run dev
```

------

## 📦 项目打包

### 后端打包

```bash
# 在 Linux 下运行
uv run pyinstaller backend/run.py \
  --name prompt-backend \
  --noconsole \
  --onefile \
  --distpath ./backend/dist \
  --workpath ./backend/build

# 在 Windows 下运行
uv run pyinstaller backend/run.py `
  --name prompt-backend `
  --noconsole `
  --onefile `
  --distpath ./backend/dist `
  --workpath ./backend/build 
```

### 前端打包

```bash
cd frontend
npm run build
```

------

**如果这个项目对你有帮助，欢迎 Star ⭐ 与 Issue 交流。**