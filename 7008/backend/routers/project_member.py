"""
项目成员路由
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend.models.project_member import ProjectMember
from backend.models.employee import Employee
from backend.schemas.common import ResponseModel
from backend.utils.auth import get_current_user

router = APIRouter(prefix="/api/project/member", tags=["项目成员"])


@router.post("/add", response_model=ResponseModel)
async def add_member(
    project_id: int,
    employee_id: int,
    role: str = "成员",
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """添加项目成员"""
    # 检查是否已存在
    exists = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.employee_id == employee_id
    ).first()
    
    if exists:
        raise HTTPException(status_code=400, detail="该员工已是项目成员")
    
    member = ProjectMember(
        project_id=project_id,
        employee_id=employee_id,
        role=role
    )
    db.add(member)
    db.commit()
    db.refresh(member)
    
    return ResponseModel(code=200, msg="添加成功", data=member)


@router.get("/list/{project_id}", response_model=ResponseModel)
async def get_project_members(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取项目成员列表"""
    members = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id
    ).all()
    
    # 关联查询员工信息
    result = []
    for member in members:
        employee = db.query(Employee).filter(Employee.id == member.employee_id).first()
        if employee:
            result.append({
                "id": member.id,
                "project_id": member.project_id,
                "employee_id": member.employee_id,
                "employee_name": employee.xingming,
                "employee_no": employee.gonghao,
                "role": member.role,
                "joined_at": member.joined_at
            })
    
    return ResponseModel(code=200, msg="查询成功", data=result)


@router.delete("/{member_id}", response_model=ResponseModel)
async def remove_member(
    member_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """移除项目成员"""
    member = db.query(ProjectMember).filter(ProjectMember.id == member_id).first()
    if not member:
        raise HTTPException(status_code=404, detail="成员不存在")
    
    db.delete(member)
    db.commit()
    
    return ResponseModel(code=200, msg="移除成功")

