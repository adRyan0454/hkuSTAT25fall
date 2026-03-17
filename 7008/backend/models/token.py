"""
数据库模型 - Token表
"""
from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class Token(Base):
    """Token表"""
    __tablename__ = "token"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="主键")
    userid = Column(BigInteger, nullable=False, comment="用户id")
    username = Column(String(100), nullable=False, comment="用户名")
    tablename = Column(String(100), comment="表名")
    role = Column(String(100), comment="角色")
    token = Column(String(200), nullable=False, comment="Token")
    addtime = Column(DateTime, server_default=func.now(), comment="新增时间")
    expiratedtime = Column(DateTime, server_default=func.now(), comment="过期时间")

    def __repr__(self):
        return f"<Token(id={self.id}, username={self.username}, role={self.role})>"


