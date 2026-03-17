"""
完整数据生成脚本（测试用）
- 生成5个部门，每个部门31人（P5:1, P4:2, P3:4, P2:8, P1:16）
- 建立管理关系（每个上级管理2个下级）
- 生成2024年11月-2025年10月的绩效数据（共12个月）
"""
import sys
from pathlib import Path
import random
from datetime import datetime

# 添加项目根目录到路径
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from backend.database import SessionLocal
from backend.models.employee import Employee
from backend.models.department import Department
from backend.models.position import Position
from backend.models.appraisal import PerformanceAppraisal
from backend.utils.kpi_config import (
    calculate_kpi_score,
    calculate_total_score,
    get_performance_level
)


# 部门配置
DEPARTMENTS = {
    "技术部": "TECH",
    "运营市场部": "OPS",
    "产品部": "PROD",
    "人力资源部": "HR",
    "财务部": "FIN"
}

# 职级配置
JOB_LEVELS = ["P5", "P4", "P3", "P2", "P1"]
LEVEL_COUNTS = {
    "P5": 1,
    "P4": 2,
    "P3": 4,
    "P2": 8,
    "P1": 16
}

# 姓氏和名字库
SURNAMES = ["张", "李", "王", "刘", "陈", "杨", "黄", "赵", "周", "吴", 
            "徐", "孙", "马", "朱", "胡", "郭", "何", "林", "罗", "高",
            "梁", "郑", "谢", "宋", "唐", "许", "韩", "冯", "邓", "曹"]

GIVEN_NAMES = ["伟", "芳", "娜", "敏", "静", "丽", "强", "磊", "军", "洋",
               "勇", "艳", "杰", "涛", "明", "超", "秀英", "娟", "雷", "刚",
               "华", "建", "峰", "浩", "鹏", "辉", "婷", "玲", "霞", "红"]

# 学历
EDUCATIONS = ["本科", "硕士", "博士"]

# 时间配置：2024年11月 - 2025年10月（共12个月）
MONTHS = [
    "2024-11", "2024-12",
    "2025-01", "2025-02", "2025-03", "2025-04", 
    "2025-05", "2025-06", "2025-07", "2025-08", 
    "2025-09", "2025-10"
]


def generate_employee_name():
    """生成随机姓名"""
    surname = random.choice(SURNAMES)
    given_name = random.choice(GIVEN_NAMES)
    return f"{surname}{given_name}"


def calculate_common_score(work_hours, supervisor_score, peer_score, resource_cost):
    """计算通用指标得分"""
    # 工作时长得分 (160-200小时为满分)
    if 160 <= work_hours <= 200:
        hours_score = 100
    elif work_hours < 160:
        hours_score = max(0, 100 - (160 - work_hours) / 160 * 50)
    else:
        hours_score = max(0, 100 - (work_hours - 200) / 40 * 30)
    
    # 上级评分和同级评分直接使用
    supervisor_score_val = supervisor_score
    peer_score_val = peer_score
    
    # 资源成本得分 (成本越低越好，5000-10000为合理区间)
    if 5000 <= resource_cost <= 10000:
        cost_score = 100
    elif resource_cost < 5000:
        cost_score = max(0, 100 - (5000 - resource_cost) / 5000 * 30)
    else:
        cost_score = max(0, 70 - (resource_cost - 10000) / 1000 * 5)
    
    # 加权计算
    total = (
        hours_score * 0.25 +
        supervisor_score_val * 0.35 +
        peer_score_val * 0.25 +
        cost_score * 0.15
    )
    
    return round(total, 2)


def generate_common_indicators(job_level, month_index):
    """生成通用指标数据"""
    # 根据职级和月份生成数据，加入一些随机波动
    base_performance = 1.0 + month_index * 0.008  # 随时间略有提升
    
    if job_level == "P5":
        work_hours = random.uniform(170, 195) * base_performance
        supervisor_score = random.randint(85, 95)
        peer_score = random.randint(85, 95)
        resource_cost = random.uniform(8000, 12000)
    elif job_level == "P4":
        work_hours = random.uniform(165, 190) * base_performance
        supervisor_score = random.randint(80, 92)
        peer_score = random.randint(80, 92)
        resource_cost = random.uniform(6500, 10000)
    elif job_level == "P3":
        work_hours = random.uniform(160, 185) * base_performance
        supervisor_score = random.randint(75, 90)
        peer_score = random.randint(75, 90)
        resource_cost = random.uniform(5500, 8500)
    elif job_level == "P2":
        work_hours = random.uniform(155, 180) * base_performance
        supervisor_score = random.randint(70, 88)
        peer_score = random.randint(70, 88)
        resource_cost = random.uniform(4500, 7000)
    else:  # P1
        work_hours = random.uniform(150, 175) * base_performance
        supervisor_score = random.randint(65, 85)
        peer_score = random.randint(65, 85)
        resource_cost = random.uniform(3500, 6000)
    
    return {
        "work_hours": round(work_hours, 2),
        "supervisor_score": supervisor_score,
        "peer_score": peer_score,
        "resource_cost": round(resource_cost, 2)
    }


def generate_tech_kpi(job_level, month_index):
    """生成技术部KPI数据"""
    performance_boost = 1.0 + month_index * 0.015  # 随时间提升
    
    if job_level == "P5":
        project_count = int(random.randint(5, 7) * performance_boost)
        bug_rate = random.uniform(0.008, 0.025) / performance_boost
        ontime_rate = min(0.98, random.uniform(0.90, 0.96) * performance_boost)
    elif job_level == "P4":
        project_count = int(random.randint(4, 6) * performance_boost)
        bug_rate = random.uniform(0.012, 0.030) / performance_boost
        ontime_rate = min(0.96, random.uniform(0.88, 0.94) * performance_boost)
    elif job_level == "P3":
        project_count = int(random.randint(3, 5) * performance_boost)
        bug_rate = random.uniform(0.018, 0.038) / performance_boost
        ontime_rate = min(0.94, random.uniform(0.85, 0.92) * performance_boost)
    elif job_level == "P2":
        project_count = int(random.randint(2, 4) * performance_boost)
        bug_rate = random.uniform(0.025, 0.050) / performance_boost
        ontime_rate = min(0.92, random.uniform(0.82, 0.90) * performance_boost)
    else:  # P1
        project_count = int(random.randint(1, 3) * performance_boost)
        bug_rate = random.uniform(0.035, 0.065) / performance_boost
        ontime_rate = min(0.90, random.uniform(0.78, 0.88) * performance_boost)
    
    return {
        "project_count": max(1, project_count),
        "bug_rate": round(bug_rate, 4),
        "ontime_rate": round(min(0.99, ontime_rate), 4)
    }


def generate_operation_kpi(job_level, month_index):
    """生成运营市场部KPI数据"""
    performance_boost = 1.0 + month_index * 0.025
    
    if job_level == "P5":
        customer_count = int(random.randint(120, 180) * performance_boost)
        conversion_rate = min(0.30, random.uniform(0.18, 0.25) * performance_boost)
        revenue = random.uniform(800000, 1200000) * performance_boost
    elif job_level == "P4":
        customer_count = int(random.randint(90, 140) * performance_boost)
        conversion_rate = min(0.28, random.uniform(0.16, 0.23) * performance_boost)
        revenue = random.uniform(600000, 900000) * performance_boost
    elif job_level == "P3":
        customer_count = int(random.randint(60, 100) * performance_boost)
        conversion_rate = min(0.25, random.uniform(0.14, 0.20) * performance_boost)
        revenue = random.uniform(400000, 700000) * performance_boost
    elif job_level == "P2":
        customer_count = int(random.randint(40, 70) * performance_boost)
        conversion_rate = min(0.22, random.uniform(0.12, 0.18) * performance_boost)
        revenue = random.uniform(250000, 500000) * performance_boost
    else:  # P1
        customer_count = int(random.randint(20, 50) * performance_boost)
        conversion_rate = min(0.20, random.uniform(0.10, 0.16) * performance_boost)
        revenue = random.uniform(150000, 350000) * performance_boost
    
    return {
        "customer_count": customer_count,
        "conversion_rate": round(conversion_rate, 4),
        "revenue": round(revenue, 2)
    }


def generate_product_kpi(job_level, month_index):
    """生成产品部KPI数据"""
    performance_boost = 1.0 + month_index * 0.020
    
    if job_level == "P5":
        feature_count = int(random.randint(15, 22) * performance_boost)
        user_satisfaction = min(95, int(random.randint(85, 92) * performance_boost))
        prototype_count = int(random.randint(12, 18) * performance_boost)
    elif job_level == "P4":
        feature_count = int(random.randint(12, 18) * performance_boost)
        user_satisfaction = min(93, int(random.randint(82, 90) * performance_boost))
        prototype_count = int(random.randint(10, 15) * performance_boost)
    elif job_level == "P3":
        feature_count = int(random.randint(9, 14) * performance_boost)
        user_satisfaction = min(90, int(random.randint(78, 87) * performance_boost))
        prototype_count = int(random.randint(7, 12) * performance_boost)
    elif job_level == "P2":
        feature_count = int(random.randint(6, 10) * performance_boost)
        user_satisfaction = min(88, int(random.randint(74, 84) * performance_boost))
        prototype_count = int(random.randint(5, 9) * performance_boost)
    else:  # P1
        feature_count = int(random.randint(3, 7) * performance_boost)
        user_satisfaction = min(85, int(random.randint(70, 80) * performance_boost))
        prototype_count = int(random.randint(3, 6) * performance_boost)
    
    return {
        "feature_count": feature_count,
        "user_satisfaction": user_satisfaction,
        "prototype_count": prototype_count
    }


def generate_hr_kpi(job_level, month_index):
    """生成人力资源部KPI数据"""
    performance_boost = 1.0 + month_index * 0.015
    
    if job_level == "P5":
        recruitment_count = int(random.randint(12, 18) * performance_boost)
        training_hours = random.uniform(80, 120) * performance_boost
        employee_retention = min(0.98, random.uniform(0.92, 0.96) * performance_boost)
    elif job_level == "P4":
        recruitment_count = int(random.randint(9, 14) * performance_boost)
        training_hours = random.uniform(65, 100) * performance_boost
        employee_retention = min(0.96, random.uniform(0.90, 0.94) * performance_boost)
    elif job_level == "P3":
        recruitment_count = int(random.randint(6, 10) * performance_boost)
        training_hours = random.uniform(50, 80) * performance_boost
        employee_retention = min(0.94, random.uniform(0.88, 0.92) * performance_boost)
    elif job_level == "P2":
        recruitment_count = int(random.randint(4, 7) * performance_boost)
        training_hours = random.uniform(35, 60) * performance_boost
        employee_retention = min(0.92, random.uniform(0.85, 0.90) * performance_boost)
    else:  # P1
        recruitment_count = int(random.randint(2, 5) * performance_boost)
        training_hours = random.uniform(25, 45) * performance_boost
        employee_retention = min(0.90, random.uniform(0.82, 0.88) * performance_boost)
    
    return {
        "recruitment_count": recruitment_count,
        "training_hours": round(training_hours, 2),
        "employee_retention": round(employee_retention, 4)
    }


def generate_finance_kpi(job_level, month_index):
    """生成财务部KPI数据"""
    performance_boost = 1.0 + month_index * 0.012
    
    if job_level == "P5":
        report_accuracy = min(0.995, random.uniform(0.975, 0.990) * performance_boost)
        audit_pass_rate = min(0.998, random.uniform(0.980, 0.995) * performance_boost)
        cost_saving = random.uniform(150000, 250000) * performance_boost
    elif job_level == "P4":
        report_accuracy = min(0.990, random.uniform(0.965, 0.985) * performance_boost)
        audit_pass_rate = min(0.995, random.uniform(0.975, 0.990) * performance_boost)
        cost_saving = random.uniform(100000, 180000) * performance_boost
    elif job_level == "P3":
        report_accuracy = min(0.985, random.uniform(0.955, 0.975) * performance_boost)
        audit_pass_rate = min(0.990, random.uniform(0.965, 0.985) * performance_boost)
        cost_saving = random.uniform(70000, 130000) * performance_boost
    elif job_level == "P2":
        report_accuracy = min(0.980, random.uniform(0.945, 0.965) * performance_boost)
        audit_pass_rate = min(0.985, random.uniform(0.955, 0.975) * performance_boost)
        cost_saving = random.uniform(40000, 90000) * performance_boost
    else:  # P1
        report_accuracy = min(0.975, random.uniform(0.935, 0.955) * performance_boost)
        audit_pass_rate = min(0.980, random.uniform(0.945, 0.965) * performance_boost)
        cost_saving = random.uniform(20000, 60000) * performance_boost
    
    return {
        "report_accuracy": round(report_accuracy, 4),
        "audit_pass_rate": round(audit_pass_rate, 4),
        "cost_saving": round(cost_saving, 2)
    }


def generate_department_kpi(department, job_level, month_index):
    """根据部门生成KPI数据"""
    if department == "技术部":
        return generate_tech_kpi(job_level, month_index)
    elif department == "运营市场部":
        return generate_operation_kpi(job_level, month_index)
    elif department == "产品部":
        return generate_product_kpi(job_level, month_index)
    elif department == "人力资源部":
        return generate_hr_kpi(job_level, month_index)
    elif department == "财务部":
        return generate_finance_kpi(job_level, month_index)
    return {}


def init_departments_and_positions():
    """初始化部门和岗位数据"""
    db = SessionLocal()
    
    try:
        print("=" * 80)
        print("初始化部门和岗位数据")
        print("=" * 80)
        
        # 清空现有数据
        db.query(Department).delete()
        db.query(Position).delete()
        db.commit()
        
        # 创建部门
        departments = [
            Department(department="技术部"),
            Department(department="运营市场部"),
            Department(department="产品部"),
            Department(department="人力资源部"),
            Department(department="财务部")
        ]
        db.bulk_save_objects(departments)
        
        # 创建岗位
        positions = [
            Position(position="P5"),
            Position(position="P4"),
            Position(position="P3"),
            Position(position="P2"),
            Position(position="P1")
        ]
        db.bulk_save_objects(positions)
        
        db.commit()
        
        print(f"\n✓ 成功创建 {len(departments)} 个部门")
        print(f"✓ 成功创建 {len(positions)} 个岗位")
        print("=" * 80)
        
    except Exception as e:
        db.rollback()
        print(f"\n❌ 初始化失败: {e}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        db.close()


def create_employees():
    """创建员工数据"""
    db = SessionLocal()
    employees = []
    used_names = set()
    
    try:
        print("=" * 80)
        print("开始生成员工数据")
        print("=" * 80)
        
        employee_counter = 1
        
        for dept_name, dept_code in DEPARTMENTS.items():
            print(f"\n【{dept_name}】")
            dept_employees = {}  # 存储本部门的员工，按职级分组
            
            # 为每个职级生成员工
            for level in JOB_LEVELS:
                count = LEVEL_COUNTS[level]
                dept_employees[level] = []
                
                for i in range(count):
                    # 生成唯一姓名
                    while True:
                        name = generate_employee_name()
                        if name not in used_names:
                            used_names.add(name)
                            break
                    
                    employee_number = f"EMP{employee_counter:04d}"
                    
                    # 确定上级（supervisor_number）
                    supervisor_number = None
                    if level == "P4":
                        # P4的上级是P5
                        if "P5" in dept_employees and dept_employees["P5"]:
                            supervisor_number = dept_employees["P5"][0].employee_number
                    elif level == "P3":
                        # P3的上级是P4，每个P4管2个P3
                        if "P4" in dept_employees and dept_employees["P4"]:
                            p4_index = i // 2  # 每2个P3对应1个P4
                            if p4_index < len(dept_employees["P4"]):
                                supervisor_number = dept_employees["P4"][p4_index].employee_number
                    elif level == "P2":
                        # P2的上级是P3，每个P3管2个P2
                        if "P3" in dept_employees and dept_employees["P3"]:
                            p3_index = i // 2
                            if p3_index < len(dept_employees["P3"]):
                                supervisor_number = dept_employees["P3"][p3_index].employee_number
                    elif level == "P1":
                        # P1的上级是P2，每个P2管2个P1
                        if "P2" in dept_employees and dept_employees["P2"]:
                            p2_index = i // 2
                            if p2_index < len(dept_employees["P2"]):
                                supervisor_number = dept_employees["P2"][p2_index].employee_number
                    
                    employee = Employee(
                        employee_number=employee_number,
                        password="123456",
                        employee_name=name,
                        age=random.randint(23, 50),
                        education=random.choice(EDUCATIONS),
                        department=dept_name,
                        supervisor_number=supervisor_number,
                        job_level=level,
                        join_date=datetime(2024, random.randint(1, 10), random.randint(1, 28))
                    )
                    
                    dept_employees[level].append(employee)
                    employees.append(employee)
                    employee_counter += 1
                    
                    supervisor_info = f" → 上级: {supervisor_number}" if supervisor_number else " (部门负责人)"
                    print(f"  {employee_number} {name:8s} {level}{supervisor_info}")
            
            print(f"  小计: {sum(len(v) for v in dept_employees.values())} 人")
        
        # 批量插入员工
        db.bulk_save_objects(employees)
        db.commit()
        
        print("\n" + "=" * 80)
        print(f"✓ 员工数据生成完成！共 {len(employees)} 人")
        print("=" * 80)
        
        return employees
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
        return []
    finally:
        db.close()


def create_appraisals(employees):
    """为所有员工生成2024年11月-2025年10月的绩效数据"""
    db = SessionLocal()
    
    try:
        print("\n" + "=" * 80)
        print("开始生成绩效数据 (2024年11月-2025年10月，共12个月)")
        print("=" * 80)
        
        appraisals = []
        
        for month_index, performance_month in enumerate(MONTHS):
            print(f"\n【{performance_month}】")
            
            month_stats = {}
            
            for employee in employees:
                # 生成通用指标
                common_data = generate_common_indicators(employee.job_level, month_index)
                
                # 计算通用指标得分
                common_score = calculate_common_score(
                    common_data["work_hours"],
                    common_data["supervisor_score"],
                    common_data["peer_score"],
                    common_data["resource_cost"]
                )
                
                # 生成部门专属KPI
                dept_kpi = generate_department_kpi(
                    employee.department,
                    employee.job_level,
                    month_index
                )
                
                # 计算KPI得分
                kpi_score = calculate_kpi_score(employee.department, dept_kpi)
                
                # 计算总分和等级
                total_score = calculate_total_score(common_score, kpi_score, employee.department)
                performance_level = get_performance_level(total_score)
                
                # 创建绩效记录
                appraisal = PerformanceAppraisal(
                    employee_number=employee.employee_number,
                    employee_name=employee.employee_name,
                    department=employee.department,
                    job_level=employee.job_level,
                    performance_month=performance_month,
                    work_hours=common_data["work_hours"],
                    supervisor_score=common_data["supervisor_score"],
                    peer_score=common_data["peer_score"],
                    resource_cost=common_data["resource_cost"],
                    department_kpi=dept_kpi,
                    common_score=common_score,
                    kpi_score=kpi_score,
                    total_score=total_score,
                    performance_level=performance_level,
                    remarks=f"{employee.department}{performance_month}月绩效考核"
                )
                
                appraisals.append(appraisal)
                
                # 统计
                dept = employee.department
                if dept not in month_stats:
                    month_stats[dept] = {"count": 0, "total": 0, "levels": {}}
                month_stats[dept]["count"] += 1
                month_stats[dept]["total"] += total_score
                month_stats[dept]["levels"][performance_level] = \
                    month_stats[dept]["levels"].get(performance_level, 0) + 1
            
            # 显示月度统计
            for dept, stats in month_stats.items():
                avg_score = stats["total"] / stats["count"]
                level_str = " ".join([f"{k}:{v}" for k, v in sorted(stats["levels"].items())])
                print(f"  {dept:12s} | 人数:{stats['count']:3d} | 平均分:{avg_score:5.2f} | {level_str}")
        
        # 批量插入绩效数据
        print(f"\n正在保存 {len(appraisals)} 条绩效记录...")
        db.bulk_save_objects(appraisals)
        db.commit()
        
        print("\n" + "=" * 80)
        print(f"✓ 绩效数据生成完成！")
        print(f"  - 员工数: {len(employees)}")
        print(f"  - 月份数: 12 (2024年11月-2025年10月)")
        print(f"  - 总记录: {len(appraisals)}")
        print("=" * 80)
        
    except Exception as e:
        db.rollback()
        print(f"\n✗ 生成失败: {str(e)}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()


def main():
    """主函数"""
    print("\n" + "=" * 80)
    print("完整数据生成脚本（测试用）")
    print("=" * 80)
    print(f"部门数: {len(DEPARTMENTS)}")
    print(f"每部门人数: {sum(LEVEL_COUNTS.values())} 人")
    print(f"总人数: {len(DEPARTMENTS) * sum(LEVEL_COUNTS.values())} 人")
    print(f"时间范围: 2024年11月-2025年10月（共12个月）")
    print(f"总记录数: {len(DEPARTMENTS) * sum(LEVEL_COUNTS.values()) * 12} 条")
    print("=" * 80)
    
    confirm = input("\n确认生成数据？(输入 yes): ")
    if confirm.lower() != "yes":
        print("已取消")
        return
    
    # 1. 初始化部门和岗位
    try:
        init_departments_and_positions()
    except Exception as e:
        print(f"\n❌ 初始化部门和岗位失败: {e}")
        return
    
    # 2. 生成员工数据
    employees = create_employees()
    
    if not employees:
        print("员工数据生成失败，终止")
        return
    
    # 3. 生成绩效数据
    create_appraisals(employees)
    
    print("\n✓ 全部完成！")


if __name__ == "__main__":
    main()
