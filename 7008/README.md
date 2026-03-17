# StaffAPT - 员工绩效管理系统

典型 FastAPI + Vue.js 的员工绩效管理系统。

## 🚀 核心功能

### 1. 基础管理

- **部门管理**: 部门信息的增删改查，部门统计分析
- **岗位管理**: 岗位信息管理，职级体系（P1-P5）
- **员工管理**: 员工档案管理，照片上传，信息维护

### 2. 绩效管理

- **绩效指标**: 自定义KPI指标，部门专属指标配置
- **绩效考核**: 员工绩效评估，多维度评分
- **项目管理**: 项目信息管理，项目成员管理，项目绩效跟踪

### 3. 数据分析

- **部门统计**: 部门人数分布，职级结构分析
- **绩效可视化**: 
  - 部门绩效对比（柱状图、饼图）
  - 员工绩效趋势（折线图）
  - 12个月历史数据分析
- **员工绩效**: 个人绩效记录查询，趋势分析

### 4. 数据导入

- **Excel导入**: 批量导入员工信息和绩效数据
- **格式支持**: .xls 和 .xlsx 格式
- **智能识别**: 自动识别部门KPI指标

## 🛠️ 技术栈

### 后端技术

- **框架**: FastAPI 0.104.1
- **ORM**: SQLAlchemy 2.0.23
- **数据库**: MySQL 8.0+ (通过 PyMySQL 连接)
- **认证**: JWT (python-jose)
- **密码加密**: Passlib + Bcrypt
- **数据处理**: Pandas, OpenPyXL, XLRD

### 前端技术

- **框架**: Vue 2.7.14
- **UI组件**: Element UI 2.15.14
- **状态管理**: Vuex 3.6.2
- **路由**: Vue Router 3.6.5
- **HTTP客户端**: Axios 1.6.0
- **图表**: ECharts 6.0.0

## 📋 环境要求

- **Python**: 3.8 或更高版本
- **Node.js**: 16.0 或更高版本
- **MySQL**: 8.0 或更高版本
- **浏览器**: Chrome, Firefox, Edge (最新版本)

## 📦 快速开始

### # 1. 克隆项目

```bash
git clone <repository-url>
cd StaffAPT
```

`repository-url` 尚未完善，忽略此步。

### 2. 数据库配置

#### 2.1 创建数据库

启动 MySQL 服务并创建数据库：

```sql
CREATE DATABASE staffapt CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

#### 2.2 配置环境变量

在项目根目录创建 `.env` 文件：

```env
# 数据库配置
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/staffapt
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=staffapt

# JWT 配置
SECRET_KEY=your-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> ⚠️ **重要**: 将 `your_password` 替换为 MySQL 密码，并在生产环境中更改 `SECRET_KEY`。

### 3. 后端部署

```bash
# 1. 创建并激活虚拟环境
conda create -n staffEnv python=3.10 -y
activate staffEnv

# 2. 安装依赖
pip install -r requirements.txt

# 3. 初始化数据库（创建表结构和管理员账号）
python backend\init_db.py

# 4. 启动后端服务
python backend\main.py
```

后端服务将在 `http://localhost:8000` 启动。

### 4. 前端部署

```bash
# 1. 进入前端目录
cd frontend

# 2. 安装依赖
npm install

# 3. 启动开发服务器
npm run serve
```

前端服务将在 `http://localhost:8080` 启动。

### 5. 访问系统

浏览器访问: **http://localhost:8080**

**默认管理员账号:**

- 用户名: `admin`
- 密码: `admin123`

> 💡 **提示**: 首次登录后请及时修改默认密码。

## 📁 项目结构

```
StaffAPT/
├── backend/                      # 后端服务
│   ├── models/                   # 数据模型
│   │   ├── user.py              # 用户模型
│   │   ├── department.py        # 部门模型
│   │   ├── position.py          # 岗位模型
│   │   ├── employee.py          # 员工模型
│   │   ├── indicator.py         # 指标模型
│   │   ├── appraisal.py         # 考核模型
│   │   ├── project.py           # 项目模型
│   │   └── ...
│   ├── routers/                 # API 路由
│   │   ├── auth.py             # 认证路由
│   │   ├── department.py       # 部门路由
│   │   ├── employee.py         # 员工路由
│   │   ├── appraisal.py        # 考核路由
│   │   ├── data_import.py      # 数据导入路由
│   │   └── ...
│   ├── schemas/                # 数据验证模式
│   ├── utils/                  # 工具函数
│   │   ├── auth.py            # 认证工具
│   │   ├── kpi_config.py      # KPI配置
│   │   └── file_utils.py      # 文件处理
│   ├── demoData/              # 测试数据生成工具
│   ├── database.py            # 数据库配置
│   ├── init_db.py            # 数据库初始化
│   ├── main.py               # 应用入口
│   └── import_excel_example.py # Excel导入示例
├── frontend/                    # 前端应用
│   ├── src/
│   │   ├── api/               # API 接口封装
│   │   ├── views/             # 页面组件
│   │   │   ├── Login.vue      # 登录页
│   │   │   ├── Home.vue       # 首页
│   │   │   ├── Department.vue # 部门管理
│   │   │   ├── Employee.vue   # 员工管理
│   │   │   ├── Appraisal.vue  # 绩效考核
│   │   │   ├── Analytics.vue  # 数据分析
│   │   │   └── ...
│   │   ├── router/            # 路由配置
│   │   ├── store/             # Vuex 状态管理
│   │   ├── utils/             # 工具函数
│   │   ├── App.vue            # 根组件
│   │   └── main.js            # 入口文件
│   ├── public/                # 静态资源
│   ├── package.json           # 前端依赖
│   └── vue.config.js          # Vue 配置
├── uploads/                    # 上传文件目录
├── .env                        # 环境变量配置
├── .gitignore                 # Git 忽略文件
├── requirements.txt           # Python 依赖
└── README.md                  # 项目文档
```

## 🔧 调试指南

### 后端开发

#### 添加新功能模块

1. **创建数据模型** (`backend/models/`)

   ```python
   from sqlalchemy import Column, Integer, String
   from backend.database import Base
   
   class NewModel(Base):
       __tablename__ = "new_table"
       id = Column(Integer, primary_key=True, index=True)
       name = Column(String(100))
   ```

2. **创建数据验证模式** (`backend/schemas/`)

   ```python
   from pydantic import BaseModel
   
   class NewModelCreate(BaseModel):
       name: str
   ```

3. **创建API路由** (`backend/routers/`)

   ```python
   from fastapi import APIRouter
   router = APIRouter(prefix="/api/newmodel", tags=["新模块"])
   ```

4. **在 main.py 中注册路由**

   ```python
   from backend.routers import newmodel
   app.include_router(newmodel.router)
   ```

### 前端开发

#### 添加新页面

1. **创建页面组件** (`frontend/src/views/NewPage.vue`)

2. **创建API接口** (`frontend/src/api/newpage.js`)

3. **配置路由** (`frontend/src/router/index.js`)

   ```javascript
   {
     path: '/newpage',
     name: 'NewPage',
     component: () => import('@/views/NewPage.vue')
   }
   ```

### 数据库管理

#### 重新初始化数据库

```bash
python backend\init_db.py
```

> ⚠️ **警告**: 此操作将清空所有数据，请谨慎使用！

#### 生成测试数据

```bash
# 1. 重置数据库
python backend\demoData\reset_and_init.py

# 2. 生成测试数据（155名员工，1860条绩效记录）
python backend\demoData\generate_full_data.py
```

### Excel 数据导入

系统支持批量导入 Excel 数据：

```bash
python backend\import_excel_example.py
```

**支持的功能**：

- ✅ 批量导入员工信息
- ✅ 批量导入绩效数据
- ✅ 智能识别部门KPI
- ✅ 支持 .xls 和 .xlsx 格式
