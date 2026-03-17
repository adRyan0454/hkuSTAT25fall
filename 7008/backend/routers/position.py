"""
岗位管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.models.position import Position
from backend.schemas.position import PositionCreate, PositionUpdate, PositionResponse
from backend.schemas.common import ResponseModel
from backend.utils.auth import get_current_user

router = APIRouter(prefix="/api/position", tags=["岗位管理"])


@router.get("/list", response_model=ResponseModel)
async def get_position_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    position: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取岗位列表（分页）"""
    query = db.query(Position)
    
    if position:
        query = query.filter(Position.position.like(f"%{position}%"))
    
    total = query.count()
    skip = (page - 1) * page_size
    items = query.offset(skip).limit(page_size).all()
    
    return ResponseModel(
        code=200,
        msg="查询成功",
        data={
            "list": [PositionResponse.model_validate(item) for item in items],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/all", response_model=ResponseModel)
async def get_all_position(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取所有岗位（不分页）"""
    items = db.query(Position).all()
    return ResponseModel(
        code=200,
        msg="查询成功",
        data=[PositionResponse.model_validate(item) for item in items]
    )


@router.post("/create", response_model=ResponseModel)
async def create_position(
    position: PositionCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建岗位"""
    existing = db.query(Position).filter(Position.position == position.position).first()
    if existing:
        raise HTTPException(status_code=400, detail="岗位已存在")
    
    db_position = Position(**position.model_dump())
    db.add(db_position)
    db.commit()
    db.refresh(db_position)
    
    return ResponseModel(
        code=200,
        msg="创建成功",
        data=PositionResponse.model_validate(db_position)
    )


@router.put("/update/{position_id}", response_model=ResponseModel)
async def update_position(
    position_id: int,
    position: PositionUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新岗位"""
    db_position = db.query(Position).filter(Position.id == position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="岗位不存在")
    
    update_data = position.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_position, field, value)
    
    db.commit()
    db.refresh(db_position)
    
    return ResponseModel(
        code=200,
        msg="更新成功",
        data=PositionResponse.model_validate(db_position)
    )


@router.delete("/delete/{position_id}", response_model=ResponseModel)
async def delete_position(
    position_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除岗位"""
    db_position = db.query(Position).filter(Position.id == position_id).first()
    if not db_position:
        raise HTTPException(status_code=404, detail="岗位不存在")
    
    db.delete(db_position)
    db.commit()
    
    return ResponseModel(code=200, msg="删除成功")


