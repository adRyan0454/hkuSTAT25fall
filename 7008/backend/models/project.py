"""
项目信息表
"""
from sqlalchemy import Column, BigInteger, String, Text, Date, DateTime, Enum
from sqlalchemy.sql import func
from backend.database import Base
import enum

class ProjectStatus(str, enum.Enum):
    """项目状态枚举"""
    PLANNING = "planning"      # 规划中
    IN_PROGRESS = "in_progress"  # 进行中
    COMPLETED = "completed"    # 已完成
    SUSPENDED = "suspended"    # 已暂停
    CANCELLED = "cancelled"    # 已取消

class Project(Base):
    """项目信息表"""
    __tablename__ = "project"
    
    id = Column(BigInteger, primary_key=True, autoincrement=True, comment="项目ID")
    project_no = Column(String(50), unique=True, nullable=False, comment="项目编号")
    project_name = Column(String(200), nullable=False, comment="项目名称")
    description = Column(Text, comment="项目描述")
    department_id = Column(BigInteger, comment="负责部门ID")
    
    # 项目时间
    start_date = Column(Date, comment="开始日期")
    end_date = Column(Date, comment="结束日期")
    actual_end_date = Column(Date, comment="实际完成日期")
    
    # 项目状态
    status = Column(
        Enum(ProjectStatus), 
        default=ProjectStatus.PLANNING, 
        comment="项目状态"
    )
    
    # 项目负责人
    manager_id = Column(BigInteger, comment="项目经理ID（员工ID）")
    
    # 项目预算和实际成本
    budget = Column(String(50), comment="预算")
    actual_cost = Column(String(50), comment="实际成本")
    
    # 附件
    attachments = Column(Text, comment="附件（JSON格式存储文件路径）")
    
    # 创建时间
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, onupdate=func.now(), comment="更新时间")
    
    def __repr__(self):
        return f"<Project(id={self.id}, name={self.project_name})>"