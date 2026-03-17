"""
FastAPI主应用
"""
import sys
from pathlib import Path

# 添加项目根目录到 Python 路径
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn

from backend.database import engine, Base
from backend.routers import auth, department, position, employee, indicator, appraisal, project, project_member, project_performance, data_import

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 创建FastAPI应用
app = FastAPI(
    title="员工绩效考核管理系统",
    description="基于Python的员工绩效考核管理系统API",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# 注册路由
app.include_router(auth.router)
app.include_router(department.router)
app.include_router(position.router)
app.include_router(employee.router)
app.include_router(indicator.router)
app.include_router(appraisal.router)
app.include_router(project.router)
app.include_router(project_member.router)
app.include_router(project_performance.router)
app.include_router(data_import.router)


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用员工绩效考核管理系统API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/api/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


