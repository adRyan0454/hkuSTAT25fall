"""
项目绩效评分表
"""
from sqlalchemy import Column, BigInteger, Integer, String, Text, Date, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.database import Base

class ProjectPerformance(Base):
    """项目绩效评分表"""
    __tablename__ = "project_performance"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    project_id = Column(
        BigInteger,
        ForeignKey('project.id', ondelete='CASCADE'),
        nullable=False,
        comment="项目ID"
    )
    employee_id = Column(
        BigInteger,
        ForeignKey('employee.id', ondelete='CASCADE'),
        nullable=False,
        comment="员工ID"
    )
    
    # 评分维度（0-100分）
    task_completion = Column(Integer, default=0, comment="任务完成度（0-100）")
    quality_score = Column(Integer, default=0, comment="工作质量（0-100）")
    cooperation_score = Column(Integer, default=0, comment="团队协作（0-100）")
    innovation_score = Column(Integer, default=0, comment="创新能力（0-100）")
    time_management = Column(Integer, default=0, comment="时间管理（0-100）")
    
    # 总分和等级
    total_score = Column(Integer, default=0, comment="总分（0-500）")
    performance_level = Column(String(20), comment="绩效等级（优秀/良好/中等/及格/不及格）")
    
    # 评价信息
    evaluator_id = Column(BigInteger, comment="评价人ID（通常是项目经理）")
    evaluation_date = Column(Date, comment="评价日期")
    comments = Column(Text, comment="评价意见")
    
    # 权重信息（可选）
    weight = Column(String(20), default="100%", comment="该项目在员工总绩效中的权重")
    
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())
    
    def __repr__(self):
        return f"<ProjectPerformance(project_id={self.project_id}, employee_id={self.employee_id}, score={self.total_score})>"