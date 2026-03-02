import os
from pathlib import Path
from pydantic_settings import BaseSettings
# 定位配置文件：backend/app/core/config.py -> core -> app -> backend
BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_PATH = os.path.join(BASE_DIR, ".env")

class Settings(BaseSettings):
    """ 配置文件 """
    API_KEY: str
    BASE_URL: str
    LLM_PROVIDER: str = "deepseek"
    LLM_MODEL: str = "deepseek-chat"
    
    model_config = {
        "env_file": ENV_PATH,        # 使用绝对路径
        "env_file_encoding": "utf-8",
        "extra": "ignore"            # 忽略多余的环境变量
    }

settings = Settings()


def update_env_file(updates: dict):
    """ 动态更新 .env 文件 """
    if not os.path.exists(ENV_PATH):
        # 如果文件不存在，直接创建
        with open(ENV_PATH, "w", encoding="utf-8") as f:
            for k, v in updates.items():
                f.write(f"{k}={v}\n")
        return

    # 读取现有行
    with open(ENV_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # 转换并更新
    new_lines = []
    keys_handled = set()
    
    for line in lines:
        stripped = line.strip()
        # 跳过注释或空行
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            new_lines.append(line)
            continue
            
        key = stripped.split("=")[0].strip()
        if key in updates:
            new_lines.append(f"{key}={updates[key]}\n")
            keys_handled.add(key)
        else:
            new_lines.append(line)

    # 处理原文件中不存在的新键
    for key, value in updates.items():
        if key not in keys_handled:
            new_lines.append(f"{key}={value}\n")

    # 写回文件
    with open(ENV_PATH, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
