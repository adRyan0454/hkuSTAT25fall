from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional, List

class ProjectCreate(BaseModel):
    project_no: str
    project_name: str
    description: Optional[str] = None
    department_id: Optional[int] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    manager_id: Optional[int] = None
    budget: Optional[str] = None

class ProjectUpdate(BaseModel):
    project_name: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    actual_end_date: Optional[date] = None
    actual_cost: Optional[str] = None

class ProjectResponse(BaseModel):
    id: int
    project_no: str
    project_name: str
    description: Optional[str]
    status: str
    start_date: Optional[date]
    end_date: Optional[date]
    manager_id: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProjectWithMembers(ProjectResponse):
    """带成员信息的项目"""
    members: List[dict] = []  # 项目成员列表