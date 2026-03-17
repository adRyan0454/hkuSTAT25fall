"""
Pydantic模式 - 绩效指标
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PerformanceIndicatorBase(BaseModel):
    """绩效指标基础模式"""
    department: Optional[str] = None
    gangwei: Optional[str] = None
    project: Optional[str] = None
    indicator1: Optional[str] = None
    score1: Optional[int] = None
    indicator2: Optional[str] = None
    score2: Optional[int] = None
    indicator3: Optional[str] = None
    score3: Optional[int] = None
    total_score: Optional[str] = None


class PerformanceIndicatorCreate(PerformanceIndicatorBase):
    """绩效指标创建模式"""
    pass


class PerformanceIndicatorUpdate(BaseModel):
    """绩效指标更新模式"""
    department: Optional[str] = None
    position: Optional[str] = None
    project: Optional[str] = None
    indicator1: Optional[str] = None
    score1: Optional[int] = None
    indicator2: Optional[str] = None
    score2: Optional[int] = None
    indicator3: Optional[str] = None
    score3: Optional[int] = None
    total_score: Optional[str] = None


class PerformanceIndicatorResponse(PerformanceIndicatorBase):
    """绩效指标响应模式"""
    id: int
    addtime: Optional[datetime] = None

    class Config:
        from_attributes = True


