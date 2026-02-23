from typing import List
from fastapi import APIRouter, Depends, HTTPException,Query
from backend.app.crud import crud_category,crud_prompt
from backend.app.models import *
from backend.app.db import db
from sqlalchemy.orm import Session


router = APIRouter()

@router.post("")
def create_category(
        data: CategoryCreate, 
        db_session: Session = Depends(db.get_db)
    ):
    """ 创建分类 """
    category = crud_category.add_category(db_session, data)
    if not category:
        raise HTTPException(
            status_code=400, 
            detail="该分类已存在"
        )
    return {"status": "ok"}


@router.delete("/{category_id}")
def delete_category(
        category_id: int, 
        db_session: Session = Depends(db.get_db)
    ):
    """ 删除分类 """
    prompts = crud_prompt.list_prompts(
        db_session, 
        category_id=category_id, 
        limit=1
    )
    if prompts: # 提示词不为空
        raise HTTPException(
            status_code=400, 
            detail="该分类下还存在提示词"
        )
    success = crud_category.delete_category(db_session, category_id)
    if not success: # 删除失败
        raise HTTPException(
            status_code=404, 
            detail="该分类不存在"
        )
    return {"status": "ok"}

@router.put("/{category_id}")
def update_category(
        category_id: int, 
        data: CategoryUpdate, 
        db_session: Session = Depends(db.get_db)
    ):
    """ 更新分类 """
    success = crud_category.update_category(db_session, category_id, data)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="该分类不存在"
        )
    return {"status": "ok"}

@router.get("",response_model=List[CategoryOut])
def list_categoris(
        page: int = Query(1, ge=1,description="页码"),
        limit: int = Query(10, ge=1,le=100,description="每页数量"),
        db_session: Session = Depends(db.get_db)
    ):
    """ 分页获取所有分类 """
    skip = (page - 1) * limit
    return crud_category.list_categories(db_session,skip,limit)

@router.get("/{category_id}", response_model=CategoryDetailOut)
def get_category_detail(
        category_id: int, 
        page: int = Query(1, ge=1, description="提示词页码"),
        size: int = Query(10, ge=1, le=100, description="提示词每页数量"),
        db_session: Session = Depends(db.get_db)
    ):
    """ 钻取详情接口：获取指定分类信息、其下的子分类列表、以及分页的提示词内容 """
    skip = (page - 1) * size
    result = crud_category.get_category_detail(
        db_session, 
        category_id=category_id, 
        prompt_skip=skip, 
        prompt_limit=size
    )
    if not result:
        raise HTTPException(
            status_code=404, 
            detail="分类不存在"
        )
    return result
