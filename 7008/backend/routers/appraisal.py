"""
绩效考核管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.models.appraisal import PerformanceAppraisal
from backend.schemas.appraisal import PerformanceAppraisalCreate, PerformanceAppraisalUpdate, PerformanceAppraisalResponse
from backend.schemas.common import ResponseModel
from backend.utils.auth import get_current_user

router = APIRouter(prefix="/api/appraisal", tags=["绩效考核管理"])


@router.get("/list", response_model=ResponseModel)
async def get_appraisal_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100000),
    employee_number: Optional[str] = None,
    employee_name: Optional[str] = None,
    department: Optional[str] = None,
    job_level: Optional[str] = None,
    performance_month: Optional[str] = None,
    performance_level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取绩效考核列表（分页）"""
    query = db.query(PerformanceAppraisal)
    
    # 如果是员工角色，只能查看自己的绩效考核
    if current_user["role"] == "员工":
        employee = current_user["user"]
        query = query.filter(PerformanceAppraisal.employee_number == employee.employee_number)
    
    if employee_number:
        query = query.filter(PerformanceAppraisal.employee_number.like(f"%{employee_number}%"))
    if employee_name:
        query = query.filter(PerformanceAppraisal.employee_name.like(f"%{employee_name}%"))
    if department:
        query = query.filter(PerformanceAppraisal.department == department)
    if job_level:
        query = query.filter(PerformanceAppraisal.job_level == job_level)
    if performance_month:
        query = query.filter(PerformanceAppraisal.performance_month == performance_month)
    if performance_level:
        query = query.filter(PerformanceAppraisal.performance_level == performance_level)
    
    total = query.count()
    skip = (page - 1) * page_size
    items = query.offset(skip).limit(page_size).all()
    
    return ResponseModel(
        code=200,
        msg="查询成功",
        data={
            "list": [PerformanceAppraisalResponse.model_validate(item) for item in items],
            "total": total,
            "page": page,
            "page_size": page_size
        }
    )


@router.get("/{appraisal_id}", response_model=ResponseModel)
async def get_appraisal(
    appraisal_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取绩效考核详情"""
    appraisal = db.query(PerformanceAppraisal).filter(
        PerformanceAppraisal.id == appraisal_id
    ).first()
    if not appraisal:
        raise HTTPException(status_code=404, detail="绩效考核不存在")
    
    # 如果是员工角色，只能查看自己的绩效考核
    if current_user["role"] == "员工":
        employee = current_user["user"]
        if appraisal.employee_number != employee.employee_number:
            raise HTTPException(status_code=403, detail="无权查看该绩效考核")
    
    return ResponseModel(
        code=200,
        msg="查询成功",
        data=PerformanceAppraisalResponse.model_validate(appraisal)
    )


@router.post("/create", response_model=ResponseModel)
async def create_appraisal(
    appraisal: PerformanceAppraisalCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建绩效考核"""
    # 计算总得分和绩效等级
    total_score = 0
    if appraisal.employee_attendance:
        total_score += appraisal.employee_attendance
    if appraisal.work_attitude:
        total_score += appraisal.work_attitude
    if appraisal.work_performance:
        total_score += appraisal.work_performance
    if appraisal.work_performance:
        total_score += appraisal.work_performance
    
    # 判断绩效等级
    if total_score >= 90:
        performance_level = "优秀"
    elif total_score >= 80:
        performance_level = "良好"
    elif total_score >= 70:
        performance_level = "中等"
    elif total_score >= 60:
        performance_level = "及格"
    else:
        performance_level = "不及格"
    
    # 创建绩效考核记录
    db_appraisal = PerformanceAppraisal(
        **appraisal.model_dump(),
        total_score=str(total_score),
        performance_level=performance_level
    )
    db.add(db_appraisal)
    db.commit()
    db.refresh(db_appraisal)
    
    return ResponseModel(
        code=200,
        msg="创建成功",
        data=PerformanceAppraisalResponse.model_validate(db_appraisal)
    )


@router.put("/update/{appraisal_id}", response_model=ResponseModel)
async def update_appraisal(
    appraisal_id: int,
    appraisal: PerformanceAppraisalUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新绩效考核"""
    db_appraisal = db.query(PerformanceAppraisal).filter(
        PerformanceAppraisal.id == appraisal_id
    ).first()
    if not db_appraisal:
        raise HTTPException(status_code=404, detail="绩效考核不存在")
    
    # 更新字段
    update_data = appraisal.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_appraisal, field, value)
    
    # 重新计算总得分和绩效等级
    total_score = 0
    if db_appraisal.employee_attendance:
        total_score += db_appraisal.employee_attendance
    if db_appraisal.work_attitude:
        total_score += db_appraisal.work_attitude
    if db_appraisal.work_performance:
        total_score += db_appraisal.work_performance
    if db_appraisal.work_performance:
        total_score += db_appraisal.work_performance
    
    if total_score >= 90:
        performance_level = "优秀"
    elif total_score >= 80:
        performance_level = "良好"
    elif total_score >= 70:
        performance_level = "中等"
    elif total_score >= 60:
        performance_level = "及格"
    else:
        performance_level = "不及格"
    
    db_appraisal.total_score = str(total_score)
    db_appraisal.performance_level = performance_level
    
    db.commit()
    db.refresh(db_appraisal)
    
    return ResponseModel(
        code=200,
        msg="更新成功",
        data=PerformanceAppraisalResponse.model_validate(db_appraisal)
    )


@router.delete("/delete/{appraisal_id}", response_model=ResponseModel)
async def delete_appraisal(
    appraisal_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除绩效考核"""
    db_appraisal = db.query(PerformanceAppraisal).filter(
        PerformanceAppraisal.id == appraisal_id
    ).first()
    if not db_appraisal:
        raise HTTPException(status_code=404, detail="绩效考核不存在")
    
    db.delete(db_appraisal)
    db.commit()
    
    return ResponseModel(code=200, msg="删除成功")


