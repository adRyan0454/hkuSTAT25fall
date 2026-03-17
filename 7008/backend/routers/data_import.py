"""
数据导入 API 路由
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, Query
from sqlalchemy.orm import Session
import os
import shutil
from pathlib import Path

from backend.database import get_db
from backend.schemas.common import ResponseModel
from backend.utils.auth import get_current_user
from backend.utils.excel_import import import_from_excel

router = APIRouter(prefix="/api/import", tags=["数据导入"])

# 上传文件保存目录
UPLOAD_DIR = Path("uploads/imports")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@router.post("/excel", response_model=ResponseModel)
async def import_excel_file(
    file: UploadFile = File(...),
    update_existing: bool = Query(False, description="是否更新已存在的记录"),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    上传并导入 Excel 文件
    
    - **file**: Excel 文件 (.xls 或 .xlsx)
    - **update_existing**: 是否更新已存在的记录
    """
    # 检查文件类型
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="只支持 .xls 和 .xlsx 格式的文件")
    
    # 保存上传的文件
    file_path = UPLOAD_DIR / file.filename
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"保存文件失败: {str(e)}")
    
    # 导入数据
    try:
        result = import_from_excel(db, str(file_path), update_existing)
        
        # 删除临时文件
        try:
            os.remove(file_path)
        except:
            pass
        
        if 'error' in result:
            raise HTTPException(status_code=500, detail=result['error'])
        
        return ResponseModel(
            code=200,
            msg="导入成功",
            data=result
        )
    
    except HTTPException:
        raise
    except Exception as e:
        # 删除临时文件
        try:
            os.remove(file_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")


@router.post("/excel/preview", response_model=ResponseModel)
async def preview_excel_file(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """
    预览 Excel 文件内容（前10行）
    
    - **file**: Excel 文件 (.xls 或 .xlsx)
    """
    import pandas as pd
    
    # 检查文件类型
    if not file.filename.endswith(('.xls', '.xlsx')):
        raise HTTPException(status_code=400, detail="只支持 .xls 和 .xlsx 格式的文件")
    
    # 保存临时文件
    file_path = UPLOAD_DIR / f"preview_{file.filename}"
    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # 读取 Excel
        df = pd.read_excel(file_path)
        
        # 删除临时文件
        os.remove(file_path)
        
        # 返回预览数据
        preview_data = {
            'total_rows': len(df),
            'columns': df.columns.tolist(),
            'preview': df.head(10).to_dict('records')
        }
        
        return ResponseModel(
            code=200,
            msg="预览成功",
            data=preview_data
        )
    
    except Exception as e:
        # 删除临时文件
        try:
            os.remove(file_path)
        except:
            pass
        raise HTTPException(status_code=500, detail=f"预览失败: {str(e)}")


@router.get("/template", response_model=ResponseModel)
async def get_import_template(
    current_user: dict = Depends(get_current_user)
):
    """
    获取导入模板说明
    """
    template_info = {
        'required_columns': [
            '姓名', '年龄', '最高学历', '员工id', '部门', '领导id', 
            '职级', '入职时间', '统计月份', '每月工作时长', 
            '上级评分', '同级评分', '培训投入'
        ],
        'optional_columns': {
            '技术部': ['上线项目数', '代码Bug率', '项目按时上线率'],
            '运营/市场部': ['用户增长率', '用户转化率', '营销活动ROI', '市场占有率'],
            '产品部': ['产品上线率', '关键功能使用率', '用户留存率', '市场份额'],
            '人力资源部': ['推荐面试量', '面试通过率', '招聘成本控制率', '员工流失率', '培训完成率'],
            '财务部': ['财务报表准确率', '预算执行率', '审计通过率']
        },
        'field_formats': {
            '员工id': '字符串，唯一标识',
            '入职时间': '日期格式，如 2024-01-01',
            '统计月份': '月份格式，如 Dec-24 或 2024-12',
            '上级评分/同级评分': '数字(0-100)或字母等级(S/A/B/C/D/E)',
            '百分比字段': '可以是 50% 或 0.5 格式'
        },
        'example': {
            '姓名': '张三',
            '年龄': 30,
            '最高学历': '本科',
            '员工id': 'EMP001',
            '部门': '技术部',
            '领导id': 'EMP000',
            '职级': 'P3',
            '入职时间': '2020-01-01',
            '统计月份': 'Dec-24',
            '每月工作时长': 180.5,
            '上级评分': 'A',
            '同级评分': 85,
            '培训投入': 1500,
            '上线项目数': 3,
            '代码Bug率': '5.2%',
            '项目按时上线率': '95%'
        }
    }
    
    return ResponseModel(
        code=200,
        msg="获取成功",
        data=template_info
    )
