"""
数据库初始化脚本
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import engine, Base, SessionLocal
from backend.models.user import User
from backend.models.department import Department
from backend.models.position import Position
from backend.models.employee import Employee


def init_db():
    """初始化数据库"""
    # 先删除所有表（重置数据库）
    print("⚠️  警告：将删除所有现有表和数据！")
    confirm = input("确认继续？(输入 yes): ")
    if confirm.lower() != 'yes':
        print("操作已取消")
        return
    
    print("\n正在删除旧表...")
    # 禁用外键检查，然后删除所有表
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.commit()
    
    Base.metadata.drop_all(bind=engine)
    
    # 重新启用外键检查
    with engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
        conn.commit()
    
    print("✓ 旧表已删除")
    
    # 创建所有表
    print("正在创建新表...")
    Base.metadata.create_all(bind=engine)
    print("✓ 新表已创建")
    
    # 创建会话
    db = SessionLocal()
    
    try:
        # 检查是否已有管理员用户
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            # 创建默认管理员用户
            admin = User(
                username="admin",
                password="123456",  # 生产环境应该使用加密密码
                role="管理员"
            )
            db.add(admin)
            print("✓ 创建默认管理员用户: admin/123456")
        
        # 创建示例部门（五个部门）
        department_list = ["技术部", "运营市场部", "产品部", "人力资源部", "财务部"]
        for department_name in department_list:
            existing = db.query(Department).filter(Department.department == department_name).first()
            if not existing:
                department = Department(department=department_name)
                db.add(department)
                print(f"✓ 创建部门: {department_name}")
        
        # 创建示例岗位
        position_list = ["经理", "主管", "员工", "助理", "专员"]
        for position_name in position_list:
            existing = db.query(Position).filter(Position.position == position_name).first()
            if not existing:
                position = Position(position=position_name)
                db.add(position)
                print(f"✓ 创建岗位: {position_name}")
        
        # 创建示例员工（使用新的字段结构）- 每个部门至少2人
        employee_list = [
            # 技术部
            {
                "employee_number": "EMP001",
                "password": "123456",
                "employee_name": "张三",
                "age": 32,
                "education": "硕士",
                "department": "技术部",
                "supervisor_number": None,
                "job_level": "P5",
                "join_date": "2021-03-15"
            },
            {
                "employee_number": "EMP002",
                "password": "123456",
                "employee_name": "李明",
                "age": 28,
                "education": "本科",
                "department": "技术部",
                "supervisor_number": "EMP001",
                "job_level": "P3",
                "join_date": "2022-06-20"
            },
            # 运营市场部
            {
                "employee_number": "EMP003",
                "password": "123456",
                "employee_name": "赵敏",
                "age": 30,
                "education": "硕士",
                "department": "运营市场部",
                "supervisor_number": None,
                "job_level": "P4",
                "join_date": "2021-08-10"
            },
            {
                "employee_number": "EMP004",
                "password": "123456",
                "employee_name": "孙丽",
                "age": 27,
                "education": "本科",
                "department": "运营市场部",
                "supervisor_number": "EMP003",
                "job_level": "P3",
                "join_date": "2022-11-15"
            },
            # 产品部
            {
                "employee_number": "EMP005",
                "password": "123456",
                "employee_name": "吴芳",
                "age": 29,
                "education": "硕士",
                "department": "产品部",
                "supervisor_number": None,
                "job_level": "P4",
                "join_date": "2021-12-01"
            },
            {
                "employee_number": "EMP006",
                "password": "123456",
                "employee_name": "郑浩",
                "age": 26,
                "education": "本科",
                "department": "产品部",
                "supervisor_number": "EMP005",
                "job_level": "P3",
                "join_date": "2023-02-15"
            },
            # 人力资源部
            {
                "employee_number": "EMP007",
                "password": "123456",
                "employee_name": "钱小雨",
                "age": 31,
                "education": "本科",
                "department": "人力资源部",
                "supervisor_number": None,
                "job_level": "P4",
                "join_date": "2020-05-20"
            },
            {
                "employee_number": "EMP008",
                "password": "123456",
                "employee_name": "冯婷",
                "age": 25,
                "education": "本科",
                "department": "人力资源部",
                "supervisor_number": "EMP007",
                "job_level": "P2",
                "join_date": "2023-07-10"
            },
            # 财务部
            {
                "employee_number": "EMP009",
                "password": "123456",
                "employee_name": "陈会计",
                "age": 35,
                "education": "硕士",
                "department": "财务部",
                "supervisor_number": None,
                "job_level": "P5",
                "join_date": "2019-03-01"
            },
            {
                "employee_number": "EMP010",
                "password": "123456",
                "employee_name": "林静",
                "age": 27,
                "education": "本科",
                "department": "财务部",
                "supervisor_number": "EMP009",
                "job_level": "P3",
                "join_date": "2022-09-15"
            }
        ]
        
        for employee_data in employee_list:
            existing = db.query(Employee).filter(
                Employee.employee_number == employee_data["employee_number"]
            ).first()
            if not existing:
                employee = Employee(**employee_data)
                db.add(employee)
                print(f"✓ 创建员工: {employee_data['employee_name']} ({employee_data['employee_number']})")
        
        # 提交所有更改
        db.commit()
        print("\n✓ 数据库初始化完成！")
        
    except Exception as e:
        print(f"\n✗ 数据库初始化失败: {str(e)}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db()