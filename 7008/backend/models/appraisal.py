"""
数据库模型 - 绩效考核表
支持通用指标和部门专属KPI
"""
from sqlalchemy import Column, BigInteger, String, Integer, Float, Text, DateTime, JSON
from sqlalchemy.sql import func
from backend.database import Base


class PerformanceAppraisal(Base):
    """绩效考核表 - 支持通用指标和部门专属KPI"""
    __tablename__ = "performance_appraisal"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="主键")
    employee_number = Column(String(200), nullable=False, comment="员工工号")
    employee_name = Column(String(200), comment="员工姓名")
    department = Column(String(200), comment="部门")
    job_level = Column(String(200), comment="职级")
    performance_month = Column(String(200), comment="绩效月份 (YYYY-MM)")
    
    # 通用指标（所有部门共有）
    work_hours = Column(Float, default=0, comment="工作时长（小时）")
    supervisor_score = Column(Integer, default=0, comment="上级评分（0-100）")
    peer_score = Column(Integer, default=0, comment="同级评分（0-100）")
    resource_cost = Column(Float, default=0, comment="员工耗费资源金额（元）")
    
    # 部门专属KPI（使用JSON存储，灵活支持不同部门的不同指标）
    # 技术部: {"project_count": 5, "bug_rate": 0.02, "ontime_rate": 0.95}
    # 运营市场部: {"customer_count": 100, "conversion_rate": 0.15, "revenue": 500000}
    # 等等...
    department_kpi = Column(JSON, comment="部门专属KPI数据（JSON格式）")
    
    # 评分和等级
    common_score = Column(Float, default=0, comment="通用指标得分")
    kpi_score = Column(Float, default=0, comment="专属KPI得分")
    total_score = Column(Float, default=0, comment="总得分")
    performance_level = Column(String(200), comment="绩效等级 (S/A/B/C/D)")
    
    # 备注
    remarks = Column(Text, comment="备注")
    
    addtime = Column(DateTime, server_default=func.now(), comment="创建时间")
    updatetime = Column(DateTime, onupdate=func.now(), comment="更新时间")

    def __repr__(self):
        return f"<PerformanceAppraisal(id={self.id}, employee_number={self.employee_number}, employee_name={self.employee_name}, performance_level={self.performance_level})>"


