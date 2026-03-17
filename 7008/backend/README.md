# Backend 后端架构说明

## 📁 文件夹结构

```
backend/
├── main.py              # FastAPI 应用入口
├── database.py          # 数据库配置
├── init_db.py          # 数据库初始化
│
├── models/             # 数据模型（SQLAlchemy ORM）
├── schemas/            # 数据验证（Pydantic）
├── routers/            # API 路由
├── utils/              # 工具函数
├── services/           # 业务逻辑（可选）
└── demoData/           # 测试数据工具
```

---

## 🎯 各文件夹作用

### 1. `models/` - 数据模型层

**作用**：定义数据库表结构（ORM）

**示例**：

```python
# models/employee.py
class Employee(Base):
    __tablename__ = "employee"
    id = Column(BigInteger, primary_key=True)
    employee_number = Column(String(200), unique=True)
    employee_name = Column(String(200))
    department = Column(String(200))
```

**文件列表**：

- `employee.py` - 员工模型
- `department.py` - 部门模型
- `appraisal.py` - 绩效考核模型
- `user.py` - 用户模型

---

### 2. `schemas/` - 数据验证层

**作用**：定义数据验证和序列化规则（Pydantic）

**示例**：

```python
# schemas/employee.py
class EmployeeCreate(BaseModel):
    employee_number: str
    employee_name: str
    department: Optional[str] = None

class EmployeeResponse(BaseModel):
    id: int
    employee_number: str
    employee_name: str
    
    class Config:
        from_attributes = True
```

**常见模式**：

- `Base` - 基础字段
- `Create` - 创建时的字段
- `Update` - 更新时的字段
- `Response` - 响应时的字段

---

### 3. `routers/` - API 路由层

**作用**：定义 API 端点，处理 HTTP 请求

**示例**：

```python
# routers/employee.py
router = APIRouter(prefix="/api/employee", tags=["员工管理"])

@router.get("/list")
async def get_employee_list(
    db: Session = Depends(get_db)
):
    employees = db.query(Employee).all()
    return ResponseModel(code=200, data=employees)

@router.post("/create")
async def create_employee(
    employee: EmployeeCreate,
    db: Session = Depends(get_db)
):
    db_employee = Employee(**employee.dict())
    db.add(db_employee)
    db.commit()
    return ResponseModel(code=200, msg="创建成功")
```

**HTTP 方法**：

- `GET` - 查询
- `POST` - 创建
- `PUT` - 更新
- `DELETE` - 删除

---

### 4. `utils/` - 工具函数层

**作用**：提供通用工具和辅助功能

**文件列表**：

- `auth.py` - JWT 认证、用户验证
- `security.py` - 密码加密
- `kpi_config.py` - KPI 计算配置
- `file_utils.py` - 文件处理

---

### 5. `services/` - 业务逻辑层

**作用**：封装复杂业务逻辑（可选）

**使用场景**：

- 复杂的数据处理
- 多表联合查询
- 事务处理

---

### 6. `demoData/` - 测试数据工具

**作用**：生成测试数据（仅开发/测试环境）

**文件列表**：

- `generate_full_data.py` - 生成完整测试数据
- `reset_and_init.py` - 重置数据库

---

## 🔄 请求处理流程

```
客户端请求
    ↓
FastAPI 接收
    ↓
中间件（CORS、认证）
    ↓
路由匹配（routers/）
    ↓
依赖注入（database、auth）
    ↓
数据验证（schemas/）
    ↓
业务处理（查询 models/）
    ↓
返回响应（序列化 schemas/）
```

---

## 📚 快速开始

### 启动服务

```bash
python backend/main.py
```

### 查看 API 文档

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 初始化数据库

```bash
python backend/init_db.py
```

### 生成测试数据

```bash
python backend/demoData/reset_and_init.py
python backend/demoData/generate_full_data.py
```

---

## 📖 详细文档

查看完整的架构说明：`FASTAPI_ARCHITECTURE_GUIDE.md`
