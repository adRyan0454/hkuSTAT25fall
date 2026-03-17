"""
用户认证路由
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.user import User
from backend.models.employee import Employee
from backend.schemas.user import UserLogin
from backend.schemas.employee import EmployeeLogin
from backend.schemas.common import ResponseModel
from backend.utils.security import verify_password, create_access_token

router = APIRouter(prefix="/api/auth", tags=["认证"])


@router.post("/login/admin", response_model=ResponseModel)
async def admin_login(user_data: UserLogin, db: Session = Depends(get_db)):
    """管理员登录"""
    # 查询用户
    user = db.query(User).filter(User.username == user_data.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码（这里先简单比较，后续可以改为加密）
    if user.password != user_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 创建token
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role, "table": "users"}
    )
    
    return ResponseModel(
        code=200,
        msg="登录成功",
        data={
            "token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "role": user.role
            }
        }
    )


@router.post("/login/employee", response_model=ResponseModel)
async def employee_login(employee_data: EmployeeLogin, db: Session = Depends(get_db)):
    """员工登录"""
    # 查询员工
    employee = db.query(Employee).filter(
        Employee.employee_number == employee_data.employee_number
    ).first()
    
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="工号或密码错误"
        )
    
    # 验证密码
    if employee.password != employee_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="工号或密码错误"
        )
    
    # 创建token
    access_token = create_access_token(
        data={"sub": employee.employee_number, "role": "员工", "table": "employee"}
    )
    
    return ResponseModel(
        code=200,
        msg="登录成功",
        data={
            "token": access_token,
            "employee": {
                "id": employee.id,
                "employee_number": employee.employee_number,
                "employee_name": employee.employee_name,
                "department": employee.department,
                "job_level": employee.job_level
            }
        }
    )


@router.post("/logout", response_model=ResponseModel)
async def logout():
    """登出"""
    return ResponseModel(code=200, msg="登出成功")


