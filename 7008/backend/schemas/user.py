"""
Pydantic模式 - 用户
"""
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserBase(BaseModel):
    """用户基础模式"""
    username: str
    role: Optional[str] = "管理员"


class UserCreate(UserBase):
    """用户创建模式"""
    password: str


class UserUpdate(BaseModel):
    """用户更新模式"""
    username: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class UserResponse(UserBase):
    """用户响应模式"""
    id: int
    addtime: Optional[datetime] = None

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    """用户登录模式"""
    username: str
    password: str


