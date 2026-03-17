"""
Pydantic模式 - 绩效考核
支持通用指标和部门专属KPI
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class PerformanceAppraisalBase(BaseModel):
    """绩效考核基础模式"""
    employee_number: Optional[str] = None
    employee_name: Optional[str] = None
    department: Optional[str] = None
    job_level: Optional[str] = None
    performance_month: Optional[str] = None
    
    # 通用指标
    work_hours: Optional[float] = None
    supervisor_score: Optional[int] = None
    peer_score: Optional[int] = None
    resource_cost: Optional[float] = None
    
    # 部门专属KPI（JSON）
    department_kpi: Optional[Dict[str, Any]] = None
    
    # 评分和等级
    common_score: Optional[float] = None
    kpi_score: Optional[float] = None
    total_score: Optional[float] = None
    performance_level: Optional[str] = None
    
    # 备注
    remarks: Optional[str] = None


class PerformanceAppraisalCreate(PerformanceAppraisalBase):
    """绩效考核创建模式"""
    employee_number: str


class PerformanceAppraisalUpdate(BaseModel):
    """绩效考核更新模式"""
    employee_name: Optional[str] = None
    department: Optional[str] = None
    job_level: Optional[str] = None
    performance_month: Optional[str] = None
    work_hours: Optional[float] = None
    supervisor_score: Optional[int] = None
    peer_score: Optional[int] = None
    resource_cost: Optional[float] = None
    department_kpi: Optional[Dict[str, Any]] = None
    common_score: Optional[float] = None
    kpi_score: Optional[float] = None
    total_score: Optional[float] = None
    performance_level: Optional[str] = None
    remarks: Optional[str] = None


class PerformanceAppraisalResponse(PerformanceAppraisalBase):
    """绩效考核响应模式"""
    id: int
    addtime: Optional[datetime] = None
    updatetime: Optional[datetime] = None

    class Config:
        from_attributes = True


