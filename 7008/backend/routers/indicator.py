"""
绩效指标管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.models.indicator import PerformanceIndicator
from backend.schemas.indicator import PerformanceIndicatorCreate, PerformanceIndicatorUpdate, PerformanceIndicatorResponse
from backend.schemas.common import ResponseModel
from backend.utils.auth import get_current_user

router = APIRouter(prefix="/api/indicator", tags=["绩效指标管理"])


@router.get("/list", response_model=ResponseModel)
async def get_indicator_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    department: Optional[str] = None,
    position: Optional[str] = None,
    project: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取绩效指标列表（分页）"""
    query = db.query(PerformanceIndicator)
    
    if department:
        query = query.filter(PerformanceIndicator.department == department)
    if position:
        query = query.filter(PerformanceIndicator.position == position)
    if project:
        query = query.filter(PerformanceIndicator.project == project)
    
    total = query.count()
    skip = (page - 1) * page_size
    items = query.offset(skip).limit(page_size).all()
    
    return ResponseModel(
        code=200,
        msg="查询成功",
        data={
            "list": [PerformanceIndicatorResponse.model_validate(item) for item in items],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/{indicator_id}", response_model=ResponseModel)
async def get_indicator(
    indicator_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取绩效指标详情"""
    indicator = db.query(PerformanceIndicator).filter(
        PerformanceIndicator.id == indicator_id
    ).first()
    if not indicator:
        raise HTTPException(status_code=404, detail="绩效指标不存在")
    return ResponseModel(
        code=200,
        msg="查询成功",
        data=PerformanceIndicatorResponse.model_validate(indicator)
    )


@router.post("/create", response_model=ResponseModel)
async def create_indicator(
    indicator: PerformanceIndicatorCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建绩效指标"""
    db_indicator = PerformanceIndicator(**indicator.model_dump())
    db.add(db_indicator)
    db.commit()
    db.refresh(db_indicator)
    
    return ResponseModel(
        code=200,
        msg="创建成功",
        data=PerformanceIndicatorResponse.model_validate(db_indicator)
    )


@router.put("/update/{indicator_id}", response_model=ResponseModel)
async def update_indicator(
    indicator_id: int,
    indicator: PerformanceIndicatorUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新绩效指标"""
    db_indicator = db.query(PerformanceIndicator).filter(
        PerformanceIndicator.id == indicator_id
    ).first()
    if not db_indicator:
        raise HTTPException(status_code=404, detail="绩效指标不存在")
    
    update_data = indicator.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_indicator, field, value)
    
    db.commit()
    db.refresh(db_indicator)
    
    return ResponseModel(
        code=200,
        msg="更新成功",
        data=PerformanceIndicatorResponse.model_validate(db_indicator)
    )


@router.delete("/delete/{indicator_id}", response_model=ResponseModel)
async def delete_indicator(
    indicator_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除绩效指标"""
    db_indicator = db.query(PerformanceIndicator).filter(
        PerformanceIndicator.id == indicator_id
    ).first()
    if not db_indicator:
        raise HTTPException(status_code=404, detail="绩效指标不存在")
    
    db.delete(db_indicator)
    db.commit()
    
    return ResponseModel(code=200, msg="删除成功")


