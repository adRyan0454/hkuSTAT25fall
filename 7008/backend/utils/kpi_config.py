"""
KPI配置文件 - 定义各部门的专属KPI指标
"""

# 技术部KPI配置
TECH_DEPT_KPI = {
    "department": "技术部",
    "kpi_fields": [
        {
            "field": "project_count",
            "label": "上线项目数量",
            "unit": "个",
            "weight": 0.3,  # 权重30%
            "scoring_rule": {
                "type": "linear",  # 线性评分
                "min": 0,
                "max": 10,
                "target": 5,  # 目标值
                "description": "每完成1个项目得20分，最高100分"
            }
        },
        {
            "field": "bug_rate",
            "label": "代码BUG率",
            "unit": "%",
            "weight": 0.35,  # 权重35%
            "scoring_rule": {
                "type": "reverse",  # 反向评分（越低越好）
                "excellent": 0.01,  # 优秀标准：1%以下
                "good": 0.03,       # 良好标准：3%以下
                "acceptable": 0.05, # 可接受：5%以下
                "description": "BUG率越低分数越高"
            }
        },
        {
            "field": "ontime_rate",
            "label": "项目按时上线率",
            "unit": "%",
            "weight": 0.35,  # 权重35%
            "scoring_rule": {
                "type": "percentage",  # 百分比评分
                "target": 0.90,  # 目标90%
                "description": "按时率直接转换为分数"
            }
        }
    ],
    "common_weight": 0.4,  # 通用指标权重40%
    "kpi_weight": 0.6      # 专属KPI权重60%
}

# 运营市场部KPI配置
OPERATION_DEPT_KPI = {
    "department": "运营市场部",
    "kpi_fields": [
        {
            "field": "customer_count",
            "label": "新增客户数",
            "unit": "个",
            "weight": 0.3,
            "scoring_rule": {
                "type": "linear",
                "min": 0,
                "max": 200,
                "target": 100,
                "description": "完成目标100个客户得满分"
            }
        },
        {
            "field": "conversion_rate",
            "label": "客户转化率",
            "unit": "%",
            "weight": 0.35,
            "scoring_rule": {
                "type": "percentage",
                "target": 0.15,
                "description": "转化率达到15%为满分"
            }
        },
        {
            "field": "revenue",
            "label": "营收贡献",
            "unit": "元",
            "weight": 0.35,
            "scoring_rule": {
                "type": "linear",
                "min": 0,
                "max": 1000000,
                "target": 500000,
                "description": "完成50万营收目标得满分"
            }
        }
    ],
    "common_weight": 0.4,
    "kpi_weight": 0.6
}

# 产品部KPI配置
PRODUCT_DEPT_KPI = {
    "department": "产品部",
    "kpi_fields": [
        {
            "field": "feature_count",
            "label": "需求完成数",
            "unit": "个",
            "weight": 0.3,
            "scoring_rule": {
                "type": "linear",
                "min": 0,
                "max": 20,
                "target": 10,
                "description": "完成10个需求为目标"
            }
        },
        {
            "field": "user_satisfaction",
            "label": "用户满意度",
            "unit": "分",
            "weight": 0.35,
            "scoring_rule": {
                "type": "direct",
                "description": "用户满意度评分（0-100）"
            }
        },
        {
            "field": "prototype_count",
            "label": "原型设计数",
            "unit": "个",
            "weight": 0.35,
            "scoring_rule": {
                "type": "linear",
                "min": 0,
                "max": 15,
                "target": 8,
                "description": "完成8个原型设计为目标"
            }
        }
    ],
    "common_weight": 0.4,
    "kpi_weight": 0.6
}

# 人力资源部KPI配置
HR_DEPT_KPI = {
    "department": "人力资源部",
    "kpi_fields": [
        {
            "field": "recruitment_count",
            "label": "招聘完成数",
            "unit": "人",
            "weight": 0.35,
            "scoring_rule": {
                "type": "linear",
                "min": 0,
                "max": 20,
                "target": 10,
                "description": "完成10人招聘为目标"
            }
        },
        {
            "field": "training_hours",
            "label": "培训时长",
            "unit": "小时",
            "weight": 0.30,
            "scoring_rule": {
                "type": "linear",
                "min": 0,
                "max": 100,
                "target": 50,
                "description": "完成50小时培训为目标"
            }
        },
        {
            "field": "employee_retention",
            "label": "员工留存率",
            "unit": "%",
            "weight": 0.35,
            "scoring_rule": {
                "type": "percentage",
                "target": 0.90,
                "description": "留存率90%为目标"
            }
        }
    ],
    "common_weight": 0.4,
    "kpi_weight": 0.6
}

# 财务部KPI配置
FINANCE_DEPT_KPI = {
    "department": "财务部",
    "kpi_fields": [
        {
            "field": "report_accuracy",
            "label": "报表准确率",
            "unit": "%",
            "weight": 0.4,
            "scoring_rule": {
                "type": "percentage",
                "target": 0.99,
                "description": "报表准确率99%为目标"
            }
        },
        {
            "field": "audit_pass_rate",
            "label": "审计通过率",
            "unit": "%",
            "weight": 0.35,
            "scoring_rule": {
                "type": "percentage",
                "target": 0.95,
                "description": "审计通过率95%为目标"
            }
        },
        {
            "field": "cost_saving",
            "label": "成本节约",
            "unit": "元",
            "weight": 0.25,
            "scoring_rule": {
                "type": "linear",
                "min": 0,
                "max": 100000,
                "target": 50000,
                "description": "节约成本5万为目标"
            }
        }
    ],
    "common_weight": 0.4,
    "kpi_weight": 0.6
}

# 部门KPI映射
DEPARTMENT_KPI_MAP = {
    "技术部": TECH_DEPT_KPI,
    "运营市场部": OPERATION_DEPT_KPI,
    "产品部": PRODUCT_DEPT_KPI,
    "人力资源部": HR_DEPT_KPI,
    "财务部": FINANCE_DEPT_KPI
}


def get_department_kpi_config(department: str):
    """获取部门的KPI配置"""
    return DEPARTMENT_KPI_MAP.get(department)


def calculate_kpi_score(department: str, kpi_data: dict) -> float:
    """
    计算部门专属KPI得分
    
    Args:
        department: 部门名称
        kpi_data: KPI数据字典
        
    Returns:
        KPI得分（0-100）
    """
    config = get_department_kpi_config(department)
    if not config:
        return 0
    
    total_score = 0
    
    for kpi_field in config["kpi_fields"]:
        field = kpi_field["field"]
        weight = kpi_field["weight"]
        rule = kpi_field["scoring_rule"]
        
        if field not in kpi_data:
            continue
        
        value = kpi_data[field]
        score = 0
        
        # 根据评分规则计算得分
        if rule["type"] == "linear":
            # 线性评分
            target = rule["target"]
            score = min(100, (value / target) * 100) if target > 0 else 0
            
        elif rule["type"] == "reverse":
            # 反向评分（越低越好）
            if value <= rule["excellent"]:
                score = 100
            elif value <= rule["good"]:
                score = 85
            elif value <= rule["acceptable"]:
                score = 70
            else:
                score = max(0, 70 - (value - rule["acceptable"]) * 1000)
                
        elif rule["type"] == "percentage":
            # 百分比评分
            target = rule["target"]
            score = min(100, (value / target) * 100) if target > 0 else 0
            
        elif rule["type"] == "direct":
            # 直接使用值作为分数
            score = min(100, max(0, value))
        
        total_score += score * weight
    
    return round(total_score, 2)


def calculate_total_score(common_score: float, kpi_score: float, department: str) -> float:
    """
    计算总得分
    
    Args:
        common_score: 通用指标得分
        kpi_score: 专属KPI得分
        department: 部门名称
        
    Returns:
        总得分（0-100）
    """
    config = get_department_kpi_config(department)
    if not config:
        return common_score
    
    common_weight = config["common_weight"]
    kpi_weight = config["kpi_weight"]
    
    total = common_score * common_weight + kpi_score * kpi_weight
    return round(total, 2)


def get_performance_level(total_score: float) -> str:
    """
    根据总分获取绩效等级
    
    Args:
        total_score: 总得分
        
    Returns:
        绩效等级 (S/A/B/C/D)
    """
    if total_score >= 90:
        return "S"
    elif total_score >= 80:
        return "A"
    elif total_score >= 70:
        return "B"
    elif total_score >= 60:
        return "C"
    else:
        return "D"
