"""
数据库模型 - 用户表
"""
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class User(Base):
    """管理员用户表"""
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="主键")
    username = Column(String(100), unique=True, nullable=False, comment="用户名")
    password = Column(String(100), nullable=False, comment="密码")
    role = Column(String(100), default="管理员", comment="角色")
    addtime = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, role={self.role})>"


