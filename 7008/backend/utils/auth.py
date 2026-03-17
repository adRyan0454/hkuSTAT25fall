"""
认证依赖
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.utils.security import decode_access_token
from backend.models.user import User
from backend.models.employee import Employee

# Bearer Token认证
security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无效的认证凭证",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    username: str = payload.get("sub")
    role: str = payload.get("role")
    table: str = payload.get("table")
    
    if username is None or role is None:
        raise credentials_exception
    
    # 根据表名查询用户
    if table == "users":
        user = db.query(User).filter(User.username == username).first()
    elif table == "employee":
        user = db.query(Employee).filter(Employee.employee_number == username).first()
    else:
        raise credentials_exception
    
    if user is None:
        raise credentials_exception
    
    return {"user": user, "role": role, "table": table}


async def get_current_admin_user(current_user: dict = Depends(get_current_user)):
    """获取当前管理员用户"""
    if current_user["role"] != "管理员":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足"
        )
    return current_user


