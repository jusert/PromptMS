from backend.app.db.db import Base
from sqlalchemy import Column, DateTime, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from pydantic import BaseModel, ConfigDict, field_serializer, Field
from datetime import datetime, timezone
from typing import Optional, List

################ SQLAlchemy ORM 模型 (数据库表结构) #####################

class CategoryORM(Base):
    """ 分类表 """
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, autoincrement=True)              # 分类ID
    name = Column(String, unique=True , nullable=False)                     # 分类名称
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True) # 父级分类ID                                 # 描述 
    # 关系映射：方便通过 category.prompts 获取下属所有提示词
    prompts = relationship("PromptORM", back_populates="category")


class PromptORM(Base):
    """ 提示词主表 """
    __tablename__ = "prompts"

    id = Column(Integer, primary_key=True, autoincrement=True)                  # 提示词ID
    title = Column(String, nullable=False)                                      # 提示词标题
    current_version = Column(Integer, default=1)                                # 当前版本号    
    description = Column(Text, nullable=True)                                   # 描述  
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)   # 分类ID
    # 创建时间：使用 lambda 确保在插入数据时生成当前的 UTC 时间
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    # 更新时间：onupdate 确保每次更新记录时都会自动刷新时间
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    # 级联映射：方便通过 prompt.category 获取该提示词所属的分类
    category = relationship("CategoryORM", back_populates="prompts")
    # 级联删除：删除提示词时，自动删除其所有版本历史
    versions = relationship("PromptVersionORM", back_populates="prompt", cascade="all, delete-orphan")


class PromptVersionORM(Base):
    """ 提示词版本内容表：存储具体的提示词内容文本，实现版本追踪 """
    __tablename__ = "prompt_versions"

    id = Column(Integer, primary_key=True, autoincrement=True)              # 版本ID
    prompt_id = Column(Integer, ForeignKey("prompts.id"), nullable=False)   # 提示词ID
    content = Column(Text, nullable=False)                                  # 提示词内容    
    version = Column(Integer, nullable=False)                               # 版本号
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    # 级联映射：方便通过 version.prompt 获取该版本对应的提示词
    prompt = relationship("PromptORM", back_populates="versions")


################ Pydantic 模型 (API 数据验证) #####################

# 基础模型
class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class PromptBase(BaseModel):
    title: str
    category_id: Optional[int] = None
    description: Optional[str] = None

# 创建模型
class PromptCreate(PromptBase):
    """ 创建提示词时，必须同时提供初始内容 """
    content: str

class CategoryCreate(CategoryBase):
    pass

# 更新模型
class PromptUpdate(BaseModel):
    """ 所有字段均为可选，仅更新传入的字段 """
    title: Optional[str] = None
    category_id: Optional[int] = None
    description: Optional[str] = None
    content: Optional[str] = None

class CategoryUpdate(CategoryBase):
    pass

# 输出模型
class PromptOut(PromptBase):
    """ 提示词列表/详情的返回结构 """
    id: int
    content: str = ""
    current_version: int
    updated_at: datetime

    # from_attributes: 允许 Pydantic 直接读取 SQLAlchemy ORM 对象
    model_config = ConfigDict(from_attributes=True)

    # 字段序列化器：将 Python datetime 对象转换为易读的字符串格式
    @field_serializer('updated_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None

class PromptVersionOut(BaseModel):
    """ 版本历史记录的返回结构 """
    version: int
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    @field_serializer('created_at')
    def serialize_dt(self, dt: datetime, _info):
        return dt.strftime("%Y-%m-%d %H:%M:%S") if dt else None

class CategoryOut(CategoryBase):
    """ 分类的基础返回结构 """
    id: int

    model_config = ConfigDict(from_attributes=True)

class CategoryDetailOut(CategoryOut):
    """ 分类详情返回结构：包含该分类下的子分类列表、提示词列表以及汇总数据 """
    sub_categories: List[CategoryOut] = Field(default_factory=list)
    prompts: List[PromptOut] = Field(default_factory=list)
    total_prompts: int = 0

    model_config = ConfigDict(from_attributes=True)

class OptimizeRequest(BaseModel):
    """ 优化提示词的请求结构 """
    prompt: str


class ConfigUpdate(BaseModel):
    """ 配置更新请求结构 """
    api_key: str
    base_url: str | None = None
    provider: str | None = None