"""
数据库模型 - 配置表
"""
from sqlalchemy import Column, BigInteger, String
from backend.database import Base


class Config(Base):
    """配置表"""
    __tablename__ = "config"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="主键")
    name = Column(String(100), nullable=False, comment="配置参数名称")
    value = Column(String(100), comment="配置参数值")

    def __repr__(self):
        return f"<Config(id={self.id}, name={self.name}, value={self.value})>"


