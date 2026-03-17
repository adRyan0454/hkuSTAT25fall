"""
Pydantic模式 - 通用响应
"""
from pydantic import BaseModel
from typing import Optional, Any, List


class ResponseModel(BaseModel):
    """通用响应模式"""
    code: int = 200
    msg: str = "成功"
    data: Optional[Any] = None


class PaginatedResponse(BaseModel):
    """分页响应模式"""
    code: int = 200
    msg: str = "成功"
    data: List[Any]
    total: int
    page: int
    page_size: int


