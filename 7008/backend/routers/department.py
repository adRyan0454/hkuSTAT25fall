"""
部门管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
from backend.database import get_db
from backend.models.department import Department
from backend.schemas.department import DepartmentCreate, DepartmentUpdate, DepartmentResponse
from backend.schemas.common import ResponseModel, PaginatedResponse
from backend.utils.auth import get_current_user

router = APIRouter(prefix="/api/department", tags=["部门管理"])


@router.get("/list", response_model=ResponseModel)
async def get_department_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=1000),
    department: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取部门列表（分页）"""
    query = db.query(Department)
    
    # 搜索过滤
    if department:
        query = query.filter(Department.department.like(f"%{department}%"))
    
    # 总数
    total = query.count()
    
    # 分页
    skip = (page - 1) * page_size
    items = query.offset(skip).limit(page_size).all()
    
    return ResponseModel(
        code=200,
        msg="查询成功",
        data={
            "list": [DepartmentResponse.model_validate(item) for item in items],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/all", response_model=ResponseModel)
async def get_all_department(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取所有部门（不分页）"""
    items = db.query(Department).all()
    return ResponseModel(
        code=200,
        msg="查询成功",
        data=[DepartmentResponse.model_validate(item) for item in items]
    )


@router.get("/{department_id}", response_model=ResponseModel)
async def get_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取部门详情"""
    department = db.query(Department).filter(Department.id == department_id).first()
    if not department:
        raise HTTPException(status_code=404, detail="部门不存在")
    return ResponseModel(
        code=200,
        msg="查询成功",
        data=DepartmentResponse.model_validate(department)
    )


@router.post("/create", response_model=ResponseModel)
async def create_department(
    department: DepartmentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建部门"""
    # 检查部门是否已存在
    existing = db.query(Department).filter(Department.department == department.department).first()
    if existing:
        raise HTTPException(status_code=400, detail="部门已存在")
    
    # 创建部门
    db_department = Department(**department.model_dump())
    db.add(db_department)
    db.commit()
    db.refresh(db_department)
    
    return ResponseModel(
        code=200,
        msg="创建成功",
        data=DepartmentResponse.model_validate(db_department)
    )


@router.put("/update/{department_id}", response_model=ResponseModel)
async def update_department(
    department_id: int,
    department: DepartmentUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新部门"""
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="部门不存在")
    
    # 更新字段
    update_data = department.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_department, field, value)
    
    db.commit()
    db.refresh(db_department)
    
    return ResponseModel(
        code=200,
        msg="更新成功",
        data=DepartmentResponse.model_validate(db_department)
    )


@router.delete("/delete/{department_id}", response_model=ResponseModel)
async def delete_department(
    department_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除部门"""
    db_department = db.query(Department).filter(Department.id == department_id).first()
    if not db_department:
        raise HTTPException(status_code=404, detail="部门不存在")
    
    db.delete(db_department)
    db.commit()
    
    return ResponseModel(code=200, msg="删除成功")


