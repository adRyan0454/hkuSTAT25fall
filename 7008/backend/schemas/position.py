"""
Pydantic模式 - 岗位
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PositionBase(BaseModel):
    """岗位基础模式"""
    position: str


class PositionCreate(PositionBase):
    """岗位创建模式"""
    pass


class PositionUpdate(BaseModel):
    """岗位更新模式"""
    position: Optional[str] = None


class PositionResponse(PositionBase):
    """岗位响应模式"""
    id: int
    addtime: Optional[datetime] = None

    class Config:
        from_attributes = True


