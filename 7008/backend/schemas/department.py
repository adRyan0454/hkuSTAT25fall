"""
Pydantic模式 - 部门
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DepartmentBase(BaseModel):
    """部门基础模式"""
    department: Optional[str] = None


class DepartmentCreate(BaseModel):
    """部门创建模式"""
    department: str


class DepartmentUpdate(BaseModel):
    """部门更新模式"""
    department: Optional[str] = None


class DepartmentResponse(DepartmentBase):
    """部门响应模式"""
    id: int
    addtime: Optional[datetime] = None

    class Config:
        from_attributes = True


