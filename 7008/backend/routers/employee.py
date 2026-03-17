"""
员工管理路由
"""
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlalchemy.orm import Session
from typing import Optional
from backend.database import get_db
from backend.models.employee import Employee
from backend.schemas.employee import EmployeeCreate, EmployeeUpdate, EmployeeResponse
from backend.schemas.common import ResponseModel
from backend.utils.auth import get_current_user
from backend.utils.file_utils import save_upload_file

router = APIRouter(prefix="/api/employee", tags=["员工管理"])


@router.get("/list")
async def get_employee_list(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=10000),
    employee_number: Optional[str] = None,
    employee_name: Optional[str] = None,
    department: Optional[str] = None,
    job_level: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取员工列表（分页）"""
    try:
        query = db.query(Employee)
        
        if employee_number:
            query = query.filter(Employee.employee_number.like(f"%{employee_number}%"))
        if employee_name:
            query = query.filter(Employee.employee_name.like(f"%{employee_name}%"))
        if department:
            query = query.filter(Employee.department == department)
        if job_level:
            query = query.filter(Employee.job_level == job_level)
        
        total = query.count()
        skip = (page - 1) * page_size
        items = query.offset(skip).limit(page_size).all()
        
        # 序列化员工数据，添加错误处理
        employee_list = []
        for item in items:
            try:
                emp_data = EmployeeResponse.model_validate(item)
                employee_list.append(emp_data)
            except Exception as e:
                # 跳过序列化失败的记录
                continue
        
        return ResponseModel(
            code=200,
            msg="查询成功",
            data={
                "list": employee_list,
                "total": total,
                "page": page,
                "page_size": page_size
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{employee_id}", response_model=ResponseModel)
async def get_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """获取员工详情"""
    employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    return ResponseModel(
        code=200,
        msg="查询成功",
        data=EmployeeResponse.model_validate(employee)
    )


@router.post("/create", response_model=ResponseModel)
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """创建员工"""
    existing = db.query(Employee).filter(
        Employee.employee_number == employee.employee_number
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="员工工号已存在")
    
    db_employee = Employee(**employee.model_dump())
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    
    return ResponseModel(
        code=200,
        msg="创建成功",
        data=EmployeeResponse.model_validate(db_employee)
    )


@router.put("/update/{employee_id}", response_model=ResponseModel)
async def update_employee(
    employee_id: int,
    employee: EmployeeUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """更新员工"""
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    
    update_data = employee.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_employee, field, value)
    
    db.commit()
    db.refresh(db_employee)
    
    return ResponseModel(
        code=200,
        msg="更新成功",
        data=EmployeeResponse.model_validate(db_employee)
    )


@router.delete("/delete/{employee_id}", response_model=ResponseModel)
async def delete_employee(
    employee_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """删除员工"""
    db_employee = db.query(Employee).filter(Employee.id == employee_id).first()
    if not db_employee:
        raise HTTPException(status_code=404, detail="员工不存在")
    
    db.delete(db_employee)
    db.commit()
    
    return ResponseModel(code=200, msg="删除成功")


@router.post("/upload", response_model=ResponseModel)
async def upload_photo(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)
):
    """上传员工照片"""
    file_path = await save_upload_file(file)
    return ResponseModel(
        code=200,
        msg="上传成功",
        data={"file_path": file_path}
    )


