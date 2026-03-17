# 员工绩效考核管理系统 - Vue前端

## 快速开始

### 1. 安装依赖

```bash
npm install
```

### 2. 启动开发服务器

```bash
npm run serve
```

### 3. 构建生产版本

```bash
npm run build
```

## 技术栈

- Vue 2.7
- Vue Router 3
- Vuex 3
- Element UI 2.15
- Axios

## 目录结构

```
vue-frontend/
├── public/              # 静态资源
├── src/
│   ├── api/            # API接口
│   ├── assets/         # 资源文件
│   ├── components/     # 公共组件
│   ├── router/         # 路由配置
│   ├── store/          # Vuex状态管理
│   ├── utils/          # 工具函数
│   ├── views/          # 页面组件
│   ├── App.vue         # 根组件
│   └── main.js         # 入口文件
├── package.json
└── vue.config.js
```

## 默认账号

- 管理员: admin / admin
- 员工: 根据员工工号登录

## 注意事项

- 确保后端API服务在 http://localhost:8000 运行
- 开发环境会自动代理API请求到后端

