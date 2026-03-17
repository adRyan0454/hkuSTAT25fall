"""
Excel 数据导入工具
用于从 Excel 文件批量导入员工和绩效数据
"""
import pandas as pd
from typing import Dict, List, Optional
from datetime import datetime
from sqlalchemy.orm import Session

from backend.models.employee import Employee
from backend.models.appraisal import PerformanceAppraisal
from backend.models.department import Department


class ExcelImporter:
    """Excel 数据导入器"""
    
    def __init__(self, db: Session):
        self.db = db
        self.errors = []
        self.success_count = 0
        self.skip_count = 0
    
    def read_excel(self, file_path: str) -> pd.DataFrame:
        """
        读取 Excel 文件
        
        Args:
            file_path: Excel 文件路径
            
        Returns:
            DataFrame: 读取的数据
        """
        try:
            # 读取 Excel 文件，支持 .xls 和 .xlsx
            df = pd.read_excel(file_path)
            return df
        except Exception as e:
            raise Exception(f"读取 Excel 文件失败: {str(e)}")
    
    def parse_employee_data(self, row: pd.Series) -> Optional[Dict]:
        """
        解析员工数据
        
        Args:
            row: DataFrame 的一行数据
            
        Returns:
            Dict: 解析后的员工数据，如果解析失败返回 None
        """
        try:
            # 映射字段
            employee_data = {
                'employee_number': str(row['员工id']),
                'employee_name': str(row['姓名']),
                'age': int(row['年龄']) if pd.notna(row['年龄']) else None,
                'education': str(row['最高学历']) if pd.notna(row['最高学历']) else None,
                'department': str(row['部门']) if pd.notna(row['部门']) else None,
                'supervisor_number': str(row['领导id']) if pd.notna(row['领导id']) and str(row['领导id']) != '' else None,
                'job_level': str(row['职级']) if pd.notna(row['职级']) else None,
                'join_date': self._parse_date(row['入职时间']) if pd.notna(row['入职时间']) else None,
                'password': '123456'  # 默认密码
            }
            return employee_data
        except Exception as e:
            self.errors.append(f"解析员工数据失败 (行 {row.name}): {str(e)}")
            return None
    
    def parse_appraisal_data(self, row: pd.Series) -> Optional[Dict]:
        """
        解析绩效考核数据
        
        Args:
            row: DataFrame 的一行数据
            
        Returns:
            Dict: 解析后的绩效数据，如果解析失败返回 None
        """
        try:
            # 解析统计月份
            performance_month = self._parse_month(row['统计月份'])
            
            # 解析上级评分和同级评分（可能是字母等级）
            supervisor_score = self._parse_score(row['上级评分'])
            peer_score = self._parse_score(row['同级评分'])
            
            # 通用指标
            appraisal_data = {
                'employee_number': str(row['员工id']),
                'employee_name': str(row['姓名']),
                'department': str(row['部门']) if pd.notna(row['部门']) else None,
                'job_level': str(row['职级']) if pd.notna(row['职级']) else None,
                'performance_month': performance_month,
                'work_hours': float(row['每月工作时长']) if pd.notna(row['每月工作时长']) else 0,
                'supervisor_score': supervisor_score,
                'peer_score': peer_score,
                'resource_cost': float(row['培训投入']) if pd.notna(row['培训投入']) else 0,
            }
            
            # 部门专属 KPI
            department_kpi = self._parse_department_kpi(row)
            appraisal_data['department_kpi'] = department_kpi
            
            # 计算得分（如果 Excel 中有 KPI 综合得分）
            if pd.notna(row['KPI综合得分']):
                appraisal_data['kpi_score'] = float(row['KPI综合得分']) * 100
            
            return appraisal_data
        except Exception as e:
            self.errors.append(f"解析绩效数据失败 (行 {row.name}): {str(e)}")
            return None
    
    def _parse_date(self, date_value) -> Optional[datetime]:
        """解析日期"""
        if pd.isna(date_value):
            return None
        
        try:
            # 如果已经是 datetime 对象
            if isinstance(date_value, datetime):
                return date_value.date()
            
            # 尝试解析字符串格式的日期
            if isinstance(date_value, str):
                # 支持多种日期格式
                for fmt in ['%Y-%m-%d', '%Y/%m/%d', '%Y.%m.%d']:
                    try:
                        return datetime.strptime(date_value, fmt).date()
                    except:
                        continue
            
            return None
        except:
            return None
    
    def _parse_month(self, month_value) -> Optional[str]:
        """解析月份格式"""
        if pd.isna(month_value):
            return None
        
        try:
            month_str = str(month_value)
            
            # 如果是 "Dec-24" 格式
            if '-' in month_str:
                month_map = {
                    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04',
                    'May': '05', 'Jun': '06', 'Jul': '07', 'Aug': '08',
                    'Sep': '09', 'Oct': '10', 'Nov': '11', 'Dec': '12'
                }
                parts = month_str.split('-')
                if len(parts) == 2:
                    month_abbr = parts[0]
                    year = '20' + parts[1] if len(parts[1]) == 2 else parts[1]
                    month_num = month_map.get(month_abbr, '01')
                    return f"{year}-{month_num}"
            
            return month_str
        except:
            return None
    
    def _parse_score(self, score_value) -> int:
        """解析评分（支持字母等级和数字）"""
        if pd.isna(score_value):
            return 0
        
        # 如果是数字，直接返回
        try:
            return int(float(score_value))
        except:
            pass
        
        # 如果是字母等级，转换为分数
        score_str = str(score_value).upper()
        grade_map = {
            'S': 95, 'A': 85, 'B': 75, 'C': 65, 'D': 55, 'E': 45
        }
        return grade_map.get(score_str, 0)
    
    def _parse_department_kpi(self, row: pd.Series) -> Dict:
        """解析部门专属 KPI"""
        department = str(row['部门']) if pd.notna(row['部门']) else ''
        kpi = {}
        
        if '技术' in department:
            # 技术部 KPI
            if pd.notna(row['上线项目数']):
                kpi['project_count'] = int(row['上线项目数'])
            if pd.notna(row['代码Bug率']):
                bug_rate_str = str(row['代码Bug率']).replace('%', '')
                kpi['bug_rate'] = float(bug_rate_str) / 100
            if pd.notna(row['项目按时上线率']):
                ontime_str = str(row['项目按时上线率']).replace('%', '')
                kpi['ontime_rate'] = float(ontime_str) / 100
        
        elif '运营' in department or '市场' in department:
            # 运营市场部 KPI
            if pd.notna(row['用户增长率']):
                growth_str = str(row['用户增长率']).replace('%', '')
                kpi['user_growth_rate'] = float(growth_str) / 100
            if pd.notna(row['用户转化率']):
                conversion_str = str(row['用户转化率']).replace('%', '')
                kpi['conversion_rate'] = float(conversion_str) / 100
            if pd.notna(row['营销活动ROI']):
                kpi['marketing_roi'] = float(row['营销活动ROI'])
            if pd.notna(row['市场占有率']):
                market_str = str(row['市场占有率']).replace('%', '')
                kpi['market_share'] = float(market_str) / 100
        
        elif '产品' in department:
            # 产品部 KPI
            if pd.notna(row['产品上线率']):
                launch_str = str(row['产品上线率']).replace('%', '')
                kpi['product_launch_rate'] = float(launch_str) / 100
            if pd.notna(row['关键功能使用率']):
                feature_str = str(row['关键功能使用率']).replace('%', '')
                kpi['feature_usage_rate'] = float(feature_str) / 100
            if pd.notna(row['用户留存率']):
                retention_str = str(row['用户留存率']).replace('%', '')
                kpi['user_retention_rate'] = float(retention_str) / 100
            if pd.notna(row['市场份额']):
                share_str = str(row['市场份额']).replace('%', '')
                kpi['market_share'] = float(share_str) / 100
        
        elif '人力' in department or '资源' in department:
            # 人力资源部 KPI
            if pd.notna(row['推荐面试量']):
                kpi['recruitment_count'] = int(row['推荐面试量'])
            if pd.notna(row['面试通过率']):
                pass_str = str(row['面试通过率']).replace('%', '')
                kpi['interview_pass_rate'] = float(pass_str) / 100
            if pd.notna(row['招聘成本控制率']):
                cost_str = str(row['招聘成本控制率']).replace('%', '')
                kpi['recruitment_cost_control'] = float(cost_str) / 100
            if pd.notna(row['员工流失率']):
                turnover_str = str(row['员工流失率']).replace('%', '')
                kpi['employee_turnover'] = float(turnover_str) / 100
            if pd.notna(row['培训完成率']):
                training_str = str(row['培训完成率']).replace('%', '')
                kpi['training_completion'] = float(training_str) / 100
        
        elif '财务' in department:
            # 财务部 KPI
            if pd.notna(row['财务报表准确率']):
                accuracy_str = str(row['财务报表准确率']).replace('%', '')
                kpi['report_accuracy'] = float(accuracy_str) / 100
            if pd.notna(row['预算执行率']):
                budget_str = str(row['预算执行率']).replace('%', '')
                kpi['budget_execution'] = float(budget_str) / 100
            if pd.notna(row['审计通过率']):
                audit_str = str(row['审计通过率']).replace('%', '')
                kpi['audit_pass_rate'] = float(audit_str) / 100
        
        return kpi
    
    def import_employees(self, df: pd.DataFrame, update_existing: bool = False) -> Dict:
        """
        导入员工数据
        
        Args:
            df: 包含员工数据的 DataFrame
            update_existing: 是否更新已存在的员工
            
        Returns:
            Dict: 导入结果统计
        """
        self.errors = []
        self.success_count = 0
        self.skip_count = 0
        
        # 去重（按员工ID）
        df_unique = df.drop_duplicates(subset=['员工id'], keep='first')
        
        for idx, row in df_unique.iterrows():
            employee_data = self.parse_employee_data(row)
            if not employee_data:
                continue
            
            try:
                # 检查员工是否已存在
                existing = self.db.query(Employee).filter(
                    Employee.employee_number == employee_data['employee_number']
                ).first()
                
                if existing:
                    if update_existing:
                        # 更新现有员工
                        for key, value in employee_data.items():
                            if key != 'password':  # 不更新密码
                                setattr(existing, key, value)
                        self.success_count += 1
                    else:
                        self.skip_count += 1
                else:
                    # 创建新员工
                    new_employee = Employee(**employee_data)
                    self.db.add(new_employee)
                    self.success_count += 1
                
            except Exception as e:
                self.errors.append(f"导入员工失败 ({employee_data.get('employee_number')}): {str(e)}")
        
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.errors.append(f"提交数据库失败: {str(e)}")
        
        return {
            'success': self.success_count,
            'skipped': self.skip_count,
            'errors': len(self.errors),
            'error_messages': self.errors
        }
    
    def import_appraisals(self, df: pd.DataFrame, update_existing: bool = False) -> Dict:
        """
        导入绩效考核数据
        
        Args:
            df: 包含绩效数据的 DataFrame
            update_existing: 是否更新已存在的记录
            
        Returns:
            Dict: 导入结果统计
        """
        self.errors = []
        self.success_count = 0
        self.skip_count = 0
        
        for idx, row in df.iterrows():
            appraisal_data = self.parse_appraisal_data(row)
            if not appraisal_data:
                continue
            
            try:
                # 检查记录是否已存在
                existing = self.db.query(PerformanceAppraisal).filter(
                    PerformanceAppraisal.employee_number == appraisal_data['employee_number'],
                    PerformanceAppraisal.performance_month == appraisal_data['performance_month']
                ).first()
                
                if existing:
                    if update_existing:
                        # 更新现有记录
                        for key, value in appraisal_data.items():
                            setattr(existing, key, value)
                        self.success_count += 1
                    else:
                        self.skip_count += 1
                else:
                    # 创建新记录
                    new_appraisal = PerformanceAppraisal(**appraisal_data)
                    self.db.add(new_appraisal)
                    self.success_count += 1
                
            except Exception as e:
                self.errors.append(
                    f"导入绩效数据失败 ({appraisal_data.get('employee_number')} - "
                    f"{appraisal_data.get('performance_month')}): {str(e)}"
                )
        
        try:
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            self.errors.append(f"提交数据库失败: {str(e)}")
        
        return {
            'success': self.success_count,
            'skipped': self.skip_count,
            'errors': len(self.errors),
            'error_messages': self.errors
        }
    
    def import_all(self, file_path: str, update_existing: bool = False) -> Dict:
        """
        导入所有数据（员工 + 绩效）
        
        Args:
            file_path: Excel 文件路径
            update_existing: 是否更新已存在的记录
            
        Returns:
            Dict: 导入结果统计
        """
        try:
            # 读取 Excel
            df = self.read_excel(file_path)
            
            # 导入员工数据
            employee_result = self.import_employees(df, update_existing)
            
            # 导入绩效数据
            appraisal_result = self.import_appraisals(df, update_existing)
            
            return {
                'total_rows': len(df),
                'employees': employee_result,
                'appraisals': appraisal_result
            }
        
        except Exception as e:
            return {
                'error': str(e),
                'employees': {'success': 0, 'skipped': 0, 'errors': 0},
                'appraisals': {'success': 0, 'skipped': 0, 'errors': 0}
            }


def import_from_excel(db: Session, file_path: str, update_existing: bool = False) -> Dict:
    """
    便捷函数：从 Excel 导入数据
    
    Args:
        db: 数据库会话
        file_path: Excel 文件路径
        update_existing: 是否更新已存在的记录
        
    Returns:
        Dict: 导入结果
    """
    importer = ExcelImporter(db)
    return importer.import_all(file_path, update_existing)
