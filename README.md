# 环境安装
## 后端
PromptMS\backend> uv venv
PromptMS\backend> uv sync
## 前端
PromptMS\frontend> npm install

# 调试运行指令
## 后端
PromptMS> uv run python -m backend.run
## 前端
PromptMS\frontend> npm run dev


# 打包指令
## 后端
PromptMS> uv run pyinstaller backend/run.py  --name prompt-backend  --noconsole  --onefile  --distpath ./backend/dist
# 前端
PromptMS\frontend> npm run build