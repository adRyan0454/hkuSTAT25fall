"""
Pydantic模式 - 员工
"""
from pydantic import BaseModel, field_validator
from typing import Optional, Union
from datetime import datetime, date


class EmployeeBase(BaseModel):
    """员工基础模式"""
    employee_number: Optional[str] = None
    employee_name: Optional[str] = None
    age: Optional[int] = None
    education: Optional[str] = None
    department: Optional[str] = None
    supervisor_number: Optional[str] = None
    job_level: Optional[str] = None
    join_date: Optional[date] = None


class EmployeeCreate(BaseModel):
    """员工创建模式"""
    employee_number: str
    employee_name: str
    password: str
    age: Optional[int] = None
    education: Optional[str] = None
    department: Optional[str] = None
    supervisor_number: Optional[str] = None
    job_level: Optional[str] = None
    join_date: Optional[date] = None


class EmployeeUpdate(BaseModel):
    """员工更新模式"""
    employee_number: Optional[str] = None
    password: Optional[str] = None
    employee_name: Optional[str] = None
    age: Optional[int] = None
    education: Optional[str] = None
    department: Optional[str] = None
    supervisor_number: Optional[str] = None
    job_level: Optional[str] = None
    join_date: Optional[date] = None


class EmployeeResponse(EmployeeBase):
    """员工响应模式"""
    id: int
    addtime: Optional[datetime] = None

    class Config:
        from_attributes = True
    
    @field_validator('join_date', mode='before')
    @classmethod
    def convert_datetime_to_date(cls, v):
        """将 datetime 转换为 date"""
        if isinstance(v, datetime):
            return v.date()
        return v


class EmployeeLogin(BaseModel):
    """员工登录模式"""
    employee_number: str
    password: str
    
    class Config:
        from_attributes = True


