"""
重置数据库并初始化完整数据（测试用）
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.database import SessionLocal
from backend.models.employee import Employee
from backend.models.department import Department
from backend.models.user import User
from backend.models.appraisal import PerformanceAppraisal
from backend.models.position import Position


def clear_all_data():
    """清空所有业务数据（保留表结构）"""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("清空现有数据")
        print("=" * 80)
        
        # 删除绩效数据
        appraisal_count = db.query(PerformanceAppraisal).count()
        db.query(PerformanceAppraisal).delete()
        print(f"✓ 删除绩效记录: {appraisal_count} 条")
        
        # 删除员工数据
        employee_count = db.query(Employee).count()
        db.query(Employee).delete()
        print(f"✓ 删除员工数据: {employee_count} 人")
        
        # 删除岗位数据
        position_count = db.query(Position).count()
        db.query(Position).delete()
        print(f"✓ 删除岗位数据: {position_count} 个")
        
        # 删除部门数据（保留或重建）
        dept_count = db.query(Department).count()
        db.query(Department).delete()
        print(f"✓ 删除部门数据: {dept_count} 个")
        
        db.commit()
        print("\n✓ 数据清空完成！")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ 清空失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def init_basic_data():
    """初始化基础数据（管理员、部门）"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 80)
        print("初始化基础数据")
        print("=" * 80)
        
        # 检查管理员是否存在
        admin = db.query(User).filter(User.username == "admin").first()
        if not admin:
            admin = User(
                username="admin",
                password="123456",
                role="管理员"
            )
            db.add(admin)
            print("✓ 创建管理员账号: admin / 123456")
        else:
            print("✓ 管理员账号已存在")
        
        # 创建部门
        departments = [
            {"department": "技术部", "description": "负责技术研发和系统维护"},
            {"department": "运营市场部", "description": "负责市场运营和客户管理"},
            {"department": "产品部", "description": "负责产品设计和需求管理"},
            {"department": "人力资源部", "description": "负责人力资源管理和培训"},
            {"department": "财务部", "description": "负责财务管理和成本控制"}
        ]
        
        for dept_data in departments:
            dept = Department(**dept_data)
            db.add(dept)
            print(f"✓ 创建部门: {dept_data['department']}")
        
        db.commit()
        print("\n✓ 基础数据初始化完成！")
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ 初始化失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("数据库重置和初始化（测试用）")
    print("=" * 80)
    print("此操作将：")
    print("1. 清空所有员工和绩效数据")
    print("2. 重新初始化基础数据（管理员、部门）")
    print("3. 准备好生成新的完整数据")
    print("=" * 80)
    
    confirm = input("\n确认执行？(输入 yes): ")
    if confirm.lower() != "yes":
        print("已取消")
        return
    
    # 清空数据
    clear_all_data()
    
    # 初始化基础数据
    init_basic_data()
    
    print("\n" + "=" * 80)
    print("✓ 重置完成！")
    print("\n下一步：运行以下命令生成完整数据")
    print("  python backend\\dataTest\\generate_full_data.py")
    print("=" * 80)


if __name__ == "__main__":
    main()
