from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ProjectMemberCreate(BaseModel):
    project_id: int
    employee_id: int
    role: Optional[str] = None
    workload: Optional[str] = "100%"

class ProjectMemberResponse(BaseModel):
    id: int
    project_id: int
    employee_id: int
    role: Optional[str]
    workload: Optional[str]
    join_date: datetime
    is_active: str
    
    class Config:
        from_attributes = True