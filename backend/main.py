from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from backend.app.db import db
from backend.app.api.v1 import categories, prompts, ai

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: 数据库初始化
    try:
        db.init_db()
        print("Database initialized successfully.")
    except Exception as e:
        print(f"Database initialization failed: {e}")
    yield
    # Shutdown: 清理工作


app = FastAPI(
    title="PromptMS API", 
    version="0.1.0",
    lifespan=lifespan
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ai.router, prefix="/ai", tags=["AI"])
app.include_router(prompts.router, prefix="/prompts", tags=["Prompts"])
app.include_router(categories.router, prefix="/categories", tags=["Categories"])
