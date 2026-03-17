"""
Excel 数据导入示例脚本
使用方法：python backend/import_excel_example.py
"""
import sys
from pathlib import Path

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from backend.database import SessionLocal
from backend.utils.excel_import import import_from_excel


def main():
    """主函数"""
    # Excel 文件路径
    excel_file = "datasets.xls"
    
    print("=" * 80)
    print("Excel 数据导入工具")
    print("=" * 80)
    print(f"文件路径: {excel_file}")
    print()
    
    # 询问是否更新已存在的记录
    update_choice = input("是否更新已存在的记录？(y/n，默认n): ").strip().lower()
    update_existing = update_choice == 'y'
    
    print("\n开始导入...")
    print("-" * 80)
    
    # 创建数据库会话
    db = SessionLocal()
    
    try:
        # 导入数据
        result = import_from_excel(db, excel_file, update_existing)
        
        # 显示结果
        print("\n" + "=" * 80)
        print("导入完成！")
        print("=" * 80)
        
        if 'error' in result:
            print(f"\n❌ 错误: {result['error']}")
        else:
            print(f"\n📊 总行数: {result['total_rows']}")
            
            print("\n【员工数据】")
            emp_result = result['employees']
            print(f"  ✅ 成功: {emp_result['success']} 条")
            print(f"  ⏭️  跳过: {emp_result['skipped']} 条")
            print(f"  ❌ 错误: {emp_result['errors']} 条")
            
            if emp_result['error_messages']:
                print("\n  错误详情:")
                for error in emp_result['error_messages'][:5]:  # 只显示前5个错误
                    print(f"    - {error}")
                if len(emp_result['error_messages']) > 5:
                    print(f"    ... 还有 {len(emp_result['error_messages']) - 5} 个错误")
            
            print("\n【绩效数据】")
            app_result = result['appraisals']
            print(f"  ✅ 成功: {app_result['success']} 条")
            print(f"  ⏭️  跳过: {app_result['skipped']} 条")
            print(f"  ❌ 错误: {app_result['errors']} 条")
            
            if app_result['error_messages']:
                print("\n  错误详情:")
                for error in app_result['error_messages'][:5]:
                    print(f"    - {error}")
                if len(app_result['error_messages']) > 5:
                    print(f"    ... 还有 {len(app_result['error_messages']) - 5} 个错误")
        
        print("\n" + "=" * 80)
        
    except Exception as e:
        print(f"\n❌ 导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        db.close()


if __name__ == "__main__":
    main()
