from sqlalchemy.orm import Session
from sqlalchemy import desc
from backend.app.models import PromptORM, PromptVersionORM, PromptCreate, PromptUpdate
from backend.app.db.db import now
from typing import Optional
def add_prompt(
        db: Session, 
        data: PromptCreate
    ) -> int | None:
    """ 新增提示词（涉及两张表） """
    prompt = db.query(PromptORM)\
        .filter(PromptORM.title == data.title).first()
    if prompt:
        return None
    
    ts = now()
    # 插入主表
    new_prompt = PromptORM(
        title=data.title,
        # category_id=target_category_id,
        category_id=data.category_id,
        description=data.description,
        current_version=1,
        created_at=ts,
        updated_at=ts
    )
    db.add(new_prompt)
    db.flush()  # 获取自增 ID

    # 插入版本表
    new_version = PromptVersionORM(
        prompt_id=new_prompt.id,
        content=data.content,
        version=1,
        created_at=ts
    )
    db.add(new_version)
    return new_prompt.id

def delete_prompt(
        db: Session, 
        prompt_id: int
    ) -> bool:
    """ 删除提示词 """
    # 获取主表记录
    prompt = db.query(PromptORM)\
        .filter(PromptORM.id == prompt_id).first()
    if not prompt: 
        return False
    # 删除主表记录
    db.delete(prompt)
    return True


def update_prompt(
        db: Session, 
        prompt_id: int, 
        data: PromptUpdate
    ) -> bool:
    """ 更新提示词并递增版本 """
    ts = now()
    prompt = db.query(PromptORM)\
        .filter(PromptORM.id == prompt_id).first()
    if not prompt: 
        return False
    
    # 获取当前版本的内容进行对比
    current_version_obj = db.query(PromptVersionORM).filter_by(
        prompt_id=prompt_id, 
        version=prompt.current_version
    ).first()

    # 如果有内容更新，创建新版本
    if data.content is not None and (not current_version_obj or data.content != current_version_obj.content):
        new_v_num = prompt.current_version + 1
        new_version = PromptVersionORM(
            prompt_id=prompt.id,
            content=data.content,
            version=new_v_num,
            created_at=ts
        )
        db.add(new_version)
        prompt.current_version = new_v_num

    # 更新其他字段
    if data.title is not None: 
        prompt.title = data.title
    if data.category_id is not None: 
        prompt.category_id = data.category_id
    if data.description is not None:
        prompt.description = data.description
    prompt.updated_at = ts
    db.flush()

    return True


def list_prompts(
        db: Session, 
        category_id: Optional[int] = None, 
        skip: int = 0, 
        limit: int = 10
    ) -> list[PromptORM]:
    # 创建查询对象，同时查 PromptORM 和最新的 PromptVersionORM
    query = db.query(
        PromptORM, 
        PromptVersionORM.content.label("content") # 给内容起个别名，匹配 Pydantic 字段名
    ).join(
        PromptVersionORM, 
        (PromptORM.id == PromptVersionORM.prompt_id) & 
        (PromptORM.current_version == PromptVersionORM.version) # 只联查当前版本
    )

    if category_id:
        query = query.filter(PromptORM.category_id == category_id)

    # 执行分页和排序
    results = query.order_by(PromptORM.updated_at.desc()).offset(skip).limit(limit).all()

    # 关键步骤：将 content 注入到 ORM 对象中
    # results 的每一项是 (PromptORM, "content_text") 这样的元组
    prompts = []
    for p_orm, content in results:
        p_orm.content = content # 动态将内容赋给 ORM 对象
        prompts.append(p_orm)
        
    return prompts

def list_prompt_versions(
        db: Session, 
        prompt_id: int
    ) -> list[PromptVersionORM]:
    """ 获取历史版本 """
    return db.query(PromptVersionORM)\
             .filter(PromptVersionORM.prompt_id == prompt_id)\
             .order_by(desc(PromptVersionORM.version)).all()

def get_prompt_detail(
        db: Session, 
        prompt_id: int
    ):
    """ 获取单个提示词详情 """
    prompt = db.query(PromptORM)\
        .filter(PromptORM.id == prompt_id).first()
    if not prompt: 
        return None
    
    # 找到当前版本对应的内容
    latest_content = ""
    for v in prompt.versions:
        if v.version == prompt.current_version:
            latest_content = v.content
            break  # 找到了就跳出循环
            
    # 手动组装返回的字典数据
    result = {
        "id": prompt.id,
        "title": prompt.title,
        "description": prompt.description,
        "category_id": prompt.category_id,
        "current_version": prompt.current_version,
        "content": latest_content,
        "version": str(prompt.current_version),
        "created_at": prompt.created_at,
        "updated_at": prompt.updated_at
    }
    
    return result
def rollback_prompt(
        db: Session, 
        prompt_id: int, 
        target_version: int
    ) -> bool:
    """ 回滚版本内容，通过改变 current_version 来实现 """
    ts = now()
    # 检查该历史版本是否存在
    exists = db.query(PromptVersionORM)\
        .filter_by(prompt_id=prompt_id, version=target_version).first()
    if not exists: 
        return False

    # 获取主表记录并修改指向
    prompt = db.query(PromptORM).get(prompt_id)
    if not prompt: 
        return False
        
    prompt.current_version = target_version
    prompt.updated_at = ts
    
    return True

