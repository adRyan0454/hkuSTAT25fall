"""
数据库模型 - 绩效指标表
"""
from sqlalchemy import Column, BigInteger, String, Integer, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class PerformanceIndicator(Base):
    """绩效指标表"""
    __tablename__ = "performance_indicator"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="主键")
    department = Column(String(200), comment="部门")
    position = Column(String(200), comment="岗位")
    project = Column(String(200), comment="绩效项目")
    indicator1 = Column(String(200), comment="绩效指标1")
    score1 = Column(Integer, comment="分值1")
    indicator2 = Column(String(200), comment="绩效指标2")
    score2 = Column(Integer, comment="分值2")
    indicator3 = Column(String(200), comment="绩效指标3")
    score3 = Column(Integer, comment="分值3")
    total_score = Column(String(200), comment="总评分")
    addtime = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<PerformanceIndicator(id={self.id}, department={self.department}, position={self.position}, project={self.project})>"


