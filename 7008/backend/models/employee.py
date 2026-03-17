"""
数据库模型 - 员工表
"""
from sqlalchemy import Column, BigInteger, String, Integer, Date, DateTime
from sqlalchemy.sql import func
from backend.database import Base


class Employee(Base):
    """员工表"""
    __tablename__ = "employee"

    id = Column(BigInteger, primary_key=True, index=True, autoincrement=True, comment="主键")
    employee_number = Column(String(200), unique=True, nullable=False, comment="员工工号")
    password = Column(String(200), nullable=False, comment="密码")
    employee_name = Column(String(200), nullable=False, comment="员工姓名")
    age = Column(Integer, comment="年龄")
    education = Column(String(200), comment="最高学历")
    department = Column(String(200), comment="所属部门")
    supervisor_number = Column(String(200), comment="领导工号")
    job_level = Column(String(200), comment="职级")
    join_date = Column(Date, comment="入职时间")
    addtime = Column(DateTime, server_default=func.now(), comment="创建时间")

    def __repr__(self):
        return f"<Employee(id={self.id}, employee_number={self.employee_number}, employee_name={self.employee_name})>"


