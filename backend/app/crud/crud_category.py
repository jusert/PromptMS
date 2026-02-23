from backend.app.models import *
from sqlalchemy.orm import Session
from typing import Any

def add_category(
        db: Session, 
        data: CategoryCreate
    ) -> bool:
    """ 添加分类 """
    # 查询对应的分类
    category = db.query(CategoryORM)\
        .filter(CategoryORM.name == data.name).first()
    if category:
        return False
    # 创建分类
    new_category = CategoryORM(
        name=data.name,
        parent_id=data.parent_id
    )
    db.add(new_category)
    db.flush()
    db.refresh(new_category)
    return True

def delete_category(
        db: Session, 
        category_id: int
    ) -> bool:
    """ 删除分类 """
    # 查询对应的分类
    category = db.query(CategoryORM)\
        .filter(CategoryORM.id == category_id).first()
    if not category:
        return False
    # 删除分类
    db.delete(category)
    return True

def update_category(
        db: Session, 
        category_id: int, 
        data: CategoryUpdate
    ) -> bool:
    """ 更新分类 """
    # 查询对应的分类
    category = db.query(CategoryORM)\
        .filter(CategoryORM.id == category_id).first()
    if not category:
        return False
    
    # 更新分类
    if data.name is not None:
            category.name = data.name
    if data.parent_id is not None:
        category.parent_id = data.parent_id
    db.flush()

    return True

def list_categories(
        db:Session,
        skip:int=0,
        limit:int=10
    ) -> list[CategoryORM]:
    """ 分页显示分类 """
    return db.query(CategoryORM).offset(skip).limit(limit).all()


def get_category_detail(
        db: Session, 
        category_id: int, 
        prompt_skip: int = 0,
        prompt_limit: int = 10
    ) -> dict[str, Any] | None:
    """ 获取分类详情  """
    # 获取当前分类对象
    category = db.query(CategoryORM)\
        .filter(CategoryORM.id == category_id).first()
    if not category:
        return None

    # # 获取子分类
    # sub_categories = db.query(CategoryORM)\
    #     .filter(CategoryORM.parent_id == category_id).all()

    # 获取提示词分页
    prompts_query = db.query(PromptORM).filter(PromptORM.category_id == category_id)
    total_prompts = prompts_query.count()
    prompts_slice = prompts_query.offset(prompt_skip).limit(prompt_limit).all()

    for prompt in prompts_slice:
        # 获取该 Prompt 的最新版本
        latest_version = db.query(PromptVersionORM)\
            .filter(PromptVersionORM.prompt_id == prompt.id)\
            .order_by(PromptVersionORM.version.desc()).first()
        
        if latest_version:
            # 这里的属性名必须与 Pydantic 模型 PromptOut 中的字段名完全对应
            prompt.content = latest_version.content  
            prompt.version = str(latest_version.version)
        else:
            prompt.content = ""
            prompt.version = "0"

    # 组装返回数据结构
    return {
        "id": category.id,
        "name": category.name,
        "prompts": prompts_slice,
        "total_prompts": total_prompts,
        # "parent_id": category.parent_id,
        # "sub_categories": sub_categories,
    }

# def search_categories(
#         db: Session, 
#         keyword: str
#     ) -> list[CategoryORM]:
#     """ 搜索分类(暂时不用) """
#     return db.query(CategoryORM).filter(CategoryORM.name.like(f"%{keyword}%")).all()


