"""
数据库模型 - 岗位表
"""
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class Position(Base):
    """岗位表"""
    __tablename__ = "position"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="主键")
    position = Column(String(200), unique=True, nullable=False, comment="岗位")
    addtime = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<Position(id={self.id}, position={self.position})>"


