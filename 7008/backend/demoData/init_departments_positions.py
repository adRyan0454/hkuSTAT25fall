"""
初始化部门和岗位数据
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.database import SessionLocal
from backend.models.department import Department
from backend.models.position import Position


def init_departments():
    """初始化部门数据"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("初始化部门数据")
        print("=" * 60)
        
        # 检查是否已有数据
        existing_count = db.query(Department).count()
        if existing_count > 0:
            print(f"\n⚠️  部门表已有 {existing_count} 条数据")
            confirm = input("是否清空并重新创建？(输入 yes): ")
            if confirm.lower() == "yes":
                db.query(Department).delete()
                db.commit()
                print("✓ 已清空部门表")
            else:
                print("已取消")
                return
        
        # 创建部门
        departments = [
            Department(department="技术部"),
            Department(department="运营市场部"),
            Department(department="产品部"),
            Department(department="人力资源部"),
            Department(department="财务部")
        ]
        
        db.bulk_save_objects(departments)
        db.commit()
        
        print(f"\n✓ 成功创建 {len(departments)} 个部门:")
        for dept in departments:
            print(f"  - {dept.department}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def init_positions():
    """初始化岗位数据"""
    db = SessionLocal()
    
    try:
        print("=" * 60)
        print("初始化岗位数据")
        print("=" * 60)
        
        # 检查是否已有数据
        existing_count = db.query(Position).count()
        if existing_count > 0:
            print(f"\n⚠️  岗位表已有 {existing_count} 条数据")
            confirm = input("是否清空并重新创建？(输入 yes): ")
            if confirm.lower() == "yes":
                db.query(Position).delete()
                db.commit()
                print("✓ 已清空岗位表")
            else:
                print("已取消")
                return
        
        # 创建岗位（职级）
        positions = [
            Position(position="P5"),
            Position(position="P4"),
            Position(position="P3"),
            Position(position="P2"),
            Position(position="P1")
        ]
        
        db.bulk_save_objects(positions)
        db.commit()
        
        print(f"\n✓ 成功创建 {len(positions)} 个岗位:")
        for pos in positions:
            print(f"  - {pos.position}")
        
        print("\n" + "=" * 60)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def main():
    """主函数"""
    print("\n🔧 初始化部门和岗位数据\n")
    
    # 初始化部门
    init_departments()
    
    # 初始化岗位
    init_positions()
    
    print("\n✅ 全部完成！\n")


if __name__ == "__main__":
    main()
