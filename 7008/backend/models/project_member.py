"""
项目成员关联表（多对多中间表）
"""
from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from backend.database import Base

class ProjectMember(Base):
    """项目成员表"""
    __tablename__ = "project_member"
    
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
    
    # 成员角色
    role = Column(String(50), comment="项目角色（如：项目经理、开发、测试等）")
    
    # 工作量
    workload = Column(String(50), comment="工作量（如：100%、50%等）")
    
    # 加入和离开时间
    join_date = Column(DateTime, server_default=func.now(), comment="加入项目时间")
    leave_date = Column(DateTime, comment="离开项目时间")
    
    # 是否活跃
    is_active = Column(String(10), default='是', comment="是否在项目中（是/否）")
    
    created_at = Column(DateTime, server_default=func.now())
    
    def __repr__(self):
        return f"<ProjectMember(project_id={self.project_id}, employee_id={self.employee_id})>"