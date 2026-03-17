from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.project import Project
from backend.models.project_member import ProjectMember
from backend.models.employee import Employee
from backend.schemas.project import *
from backend.schemas.project_member import *
from backend.schemas.common import ResponseModel

router = APIRouter(prefix="/api/project", tags=["项目管理"])

@router.get("/list", response_model=ResponseModel)
def get_project_list(
    page: int = 1,
    page_size: int = 10,
    status: str = None,
    db: Session = Depends(get_db)
):
    """获取项目列表"""
    query = db.query(Project)
    
    if status:
        query = query.filter(Project.status == status)
    
    total = query.count()
    items = query.offset((page-1)*page_size).limit(page_size).all()
    
    return ResponseModel(data={
        "list": items,
        "total": total,
        "page": page,
        "page_size": page_size
    })

@router.get("/{project_id}/members", response_model=ResponseModel)
def get_project_members(project_id: int, db: Session = Depends(get_db)):
    """获取项目成员列表"""
    members = db.query(ProjectMember, Employee).join(
        Employee, ProjectMember.employee_id == Employee.id
    ).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.is_active == '是'
    ).all()
    
    result = []
    for member, employee in members:
        result.append({
            "member_id": member.id,
            "employee_id": employee.id,
            "employee_name": employee.employee_name,
            "employee_no": employee.employee_number,
            "department": employee.department,
            "position": employee.position,
            "role": member.role,
            "workload": member.workload,
            "join_date": member.join_date
        })
    
    return ResponseModel(data=result)

@router.post("/create", response_model=ResponseModel)
def create_project(project: ProjectCreate, db: Session = Depends(get_db)):
    """创建项目"""
    # 检查项目编号是否存在
    existing = db.query(Project).filter(
        Project.project_no == project.project_no
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="项目编号已存在")
    
    new_project = Project(**project.model_dump())
    db.add(new_project)
    db.commit()
    db.refresh(new_project)
    
    return ResponseModel(msg="创建成功", data=new_project)

@router.post("/{project_id}/add_member", response_model=ResponseModel)
def add_project_member(
    project_id: int,
    member: ProjectMemberCreate,
    db: Session = Depends(get_db)
):
    """添加项目成员"""
    # 检查是否已经是成员
    existing = db.query(ProjectMember).filter(
        ProjectMember.project_id == project_id,
        ProjectMember.employee_id == member.employee_id,
        ProjectMember.is_active == '是'
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="该员工已是项目成员")
    
    new_member = ProjectMember(
        project_id=project_id,
        employee_id=member.employee_id,
        role=member.role,
        workload=member.workload
    )
    db.add(new_member)
    db.commit()
    
    return ResponseModel(msg="添加成功")

@router.delete("/{project_id}/remove_member/{member_id}")
def remove_project_member(
    project_id: int,
    member_id: int,
    db: Session = Depends(get_db)
):
    """移除项目成员"""
    member = db.query(ProjectMember).filter(
        ProjectMember.id == member_id,
        ProjectMember.project_id == project_id
    ).first()
    
    if not member:
        raise HTTPException(status_code=404, detail="成员不存在")
    
    member.is_active = '否'
    member.leave_date = datetime.now()
    db.commit()
    
    return ResponseModel(msg="移除成功")