import os
import sys
from pathlib import Path
from datetime import datetime, timezone
from typing import Generator
from sqlalchemy import create_engine, text, event
from sqlalchemy.orm import sessionmaker, Session, declarative_base

def get_data_dir() -> Path:
    """ 获取数据目录 """
    data_dir = Path(os.environ.get("PROMPTMS_DATA_DIR", "./database/data"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

################  路径配置 ################

DATA_DIR = get_data_dir()           # 数据目录
DB_PATH = DATA_DIR / "data.db"      # 数据库文件路径
SCHEMA_DIR = Path(os.environ.get("PROMPTMS_SCHEMA_PATH", "./database/schema")) # 模式文件目录
SEED_PATH = SCHEMA_DIR / "seed.sql" # 种子数据文件路径


################  ORM 配置 ################ 

SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}" # SQLite 数据库 URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False} # 允许 FastAPI 多线程访问
) # 创建数据库引擎

# 开启 SQLite 外键支持 (关键：默认 SQLite 禁用外键)
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# 模型基类 (供 models.py 继承)
Base = declarative_base()


################  核心工具函数 ################ 

def get_db() -> Generator[Session, None, None]:
    """ FastAPI 依赖注入使用的数据库会话获取函数 """
    db = SessionLocal()
    try:
        yield db
        db.commit() # 请求正常结束则自动提交
    except Exception:
        db.rollback() # 只要 API 抛出任何异常就回滚
        raise
    finally:
        db.close()

def now() -> str:
    """ 保持 ISO 格式的时间 """
    return datetime.now(timezone.utc)

def init_db():
    """ 初始化数据库：创建表、执行 SQL 脚本、注入种子数据 """
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    print(f"Checking database (ORM) at {DB_PATH}...")

    # 获取物理连接来执行原始脚本
    with engine.connect() as conn:
        try:
            # 利用 ORM 模型自动创建表
            print("Creating tables using ORM models...")
            Base.metadata.create_all(bind=engine)

            # 注入硬编码的必备数据（如：未分类），使用 INSERT OR IGNORE 防止重复插入
            print("Ensuring default category exists...")
            default_category_sql = text(
                "INSERT OR IGNORE INTO categories (id, name) VALUES (1, '未分类')"
            )
            conn.execute(default_category_sql)

            # 检查是否有seed.sql文件并注入种子
            check_sql = text("SELECT COUNT(*) FROM prompts")
            try:
                count = conn.execute(check_sql).scalar()
            except Exception:
                count = 0

            if count == 0 and SEED_PATH.exists():
                print("Injecting seed data...")
                with open(SEED_PATH, "r", encoding="utf-8") as f:
                    for statement in f.read().split(";"):
                        if statement.strip():
                            conn.execute(text(statement))
                conn.commit()
                print("Seed data injected successfully.")
            elif count > 0:
                print("Database already contains data, skipping seed.")
            
            # 统一提交更改
            conn.commit()
        except Exception as e:
            print(f"Database initialization failed: {e}")
            conn.rollback()
        finally:
            print("Database initialization complete.")