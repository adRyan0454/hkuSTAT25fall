"""
数据库模型 - 部门表
"""
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class Department(Base):
    """部门表"""
    __tablename__ = "department"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="主键")
    department = Column(String(200), unique=True, nullable=False, comment="部门")
    addtime = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<Department(id={self.id}, department={self.department})>"