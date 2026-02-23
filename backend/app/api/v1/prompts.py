from backend.app.models import PromptCreate, PromptUpdate, PromptOut, PromptVersionOut
from backend.app.crud import crud_prompt
from backend.app.db import db
from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional

router = APIRouter()

@router.post("")
def create_prompt(
        data: PromptCreate, 
        db_session: Session = Depends(db.get_db)
    ):
    """ 创建提示词 """
    prompt = crud_prompt.add_prompt(db_session, data)
    if not prompt:
        raise HTTPException(
            status_code=400, 
            detail="该分类已存在"
        )
    return {"status": "ok"}


@router.delete("/{prompt_id}")
def delete_prompt(
        prompt_id: int, 
        db_session: Session = Depends(db.get_db)
    ):
    """ 删除提示词及其所有版本 """
    # 这里只需删除主表记录即可（会自动级联删除子表记录）
    from backend.app.models import PromptORM
    db_obj = db_session.query(PromptORM).filter(PromptORM.id == prompt_id).first()
    if not db_obj:
        raise HTTPException(
            status_code=404, 
            detail="删除失败，提示词不存在"
        )
    db_session.delete(db_obj)
    db_session.commit()
    return {"status": "ok"}

@router.put("/{prompt_id}")
def update_prompt(
        prompt_id: int, 
        data: PromptUpdate, 
        db_session: Session = Depends(db.get_db)
    ):
    """ 更新提示词（会自动生成新版本） """
    success = crud_prompt.update_prompt(db_session, prompt_id, data)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="更新失败，提示词不存在"
        )
    return {"status": "ok"}

@router.get("", response_model=List[PromptOut])
def list_prompts(
    category_id: Optional[int] = None, 
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量"),
    db_session: Session = Depends(db.get_db)  # 切换到 ORM Session
):
    """ 分页获取提示词列表 """
    skip = (page - 1) * size
    # 调用 ORM 版 list_prompts
    return crud_prompt.list_prompts(db_session, category_id, skip=skip, limit=size)

@router.get("/{prompt_id}", response_model=PromptOut)
def get_prompt_detail(
    prompt_id: int, 
    db_session: Session = Depends(db.get_db)
):
    """ 获取单个提示词详情（含最新内容） """
    prompt = crud_prompt.get_prompt_detail(db_session, prompt_id)
    if not prompt:
        raise HTTPException(
            status_code=404, 
            detail="提示词不存在"
        )
    return prompt

@router.post("/{prompt_id}/rollback/{version}")
def rollback_prompt_version(
        prompt_id: int, 
        version: int, 
        db_session: Session = Depends(db.get_db)
    ):
    """ 回滚接口：将提示词内容回滚到指定版本，并作为最新的版本号插入 """
    success = crud_prompt.rollback_prompt(db_session, prompt_id, version)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="版本不存在或回滚失败"
        )
    
    return {"status": "ok", "msg": f"已回滚至版本 {version}，版本链已更新"}

@router.get("/{prompt_id}/versions", response_model=List[PromptVersionOut])
def get_prompt_history(
        prompt_id: int, 
        db_session: Session = Depends(db.get_db)
    ):
    """ 获取某个提示词的所有历史版本列表 """
    return crud_prompt.list_prompt_versions(db_session, prompt_id)

