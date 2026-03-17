from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.project_performance import ProjectPerformance
from backend.schemas.project_performance import *
from backend.schemas.common import ResponseModel

router = APIRouter(prefix="/api/project/performance", tags=["项目绩效"])

@router.post("/evaluate", response_model=ResponseModel)
def create_performance_evaluation(
    evaluation: ProjectPerformanceCreate,
    db: Session = Depends(get_db)
):
    """创建项目绩效评价"""
    # 计算总分
    total_score = (
        evaluation.task_completion +
        evaluation.quality_score +
        evaluation.cooperation_score +
        evaluation.innovation_score +
        evaluation.time_management
    )
    
    # 判断等级
    if total_score >= 450:
        level = "优秀"
    elif total_score >= 400:
        level = "良好"
    elif total_score >= 350:
        level = "中等"
    elif total_score >= 300:
        level = "及格"
    else:
        level = "不及格"
    
    # 检查是否已评价
    existing = db.query(ProjectPerformance).filter(
        ProjectPerformance.project_id == evaluation.project_id,
        ProjectPerformance.employee_id == evaluation.employee_id
    ).first()
    
    if existing:
        # 更新
        for key, value in evaluation.model_dump().items():
            setattr(existing, key, value)
        existing.total_score = total_score
        existing.performance_level = level
        db.commit()
        db.refresh(existing)
        result = existing
    else:
        # 新建
        new_eval = ProjectPerformance(
            **evaluation.model_dump(),
            total_score=total_score,
            performance_level=level
        )
        db.add(new_eval)
        db.commit()
        db.refresh(new_eval)
        result = new_eval
    
    return ResponseModel(msg="评价成功", data=result)

@router.get("/project/{project_id}", response_model=ResponseModel)
def get_project_performances(project_id: int, db: Session = Depends(get_db)):
    """获取项目所有成员的绩效"""
    performances = db.query(ProjectPerformance).filter(
        ProjectPerformance.project_id == project_id
    ).all()
    
    return ResponseModel(data=performances)

@router.get("/employee/{employee_id}", response_model=ResponseModel)
def get_employee_project_performances(employee_id: int, db: Session = Depends(get_db)):
    """获取员工在各项目的绩效"""
    performances = db.query(ProjectPerformance).filter(
        ProjectPerformance.employee_id == employee_id
    ).all()
    
    return ResponseModel(data=performances)