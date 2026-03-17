import Vue from 'vue'
import VueRouter from 'vue-router'
import Cookies from 'js-cookie'

Vue.use(VueRouter)

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { title: '登录' }
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    redirect: '/home',
    meta: { requiresAuth: true },
    children: [
      {
        path: 'home',
        name: 'Home',
        component: () => import('@/views/Home.vue'),
        meta: { title: '首页', requiresAuth: true }
      },
      {
        path: 'department',
        name: 'Department',
        component: () => import('@/views/DepartmentStats.vue'),
        meta: { title: '部门情况', requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'employee',
        name: 'Employee',
        component: () => import('@/views/Employee.vue'),
        meta: { title: '员工管理', requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'appraisal',
        name: 'Appraisal',
        component: () => import('@/views/Appraisal.vue'),
        meta: { title: '绩效考核管理', requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'analytics',
        name: 'Analytics',
        component: () => import('@/views/Analytics.vue'),
        meta: { title: '绩效可视化', requiresAuth: true, requiresAdmin: true }
      },
      {
        path: 'employee/info',
        name: 'EmployeeInfo',
        component: () => import('@/views/EmployeeInfo.vue'),
        meta: { title: '我的信息', requiresAuth: true }
      },
      {
        path: 'employee/performance',
        name: 'EmployeePerformance',
        component: () => import('@/views/EmployeePerformance.vue'),
        meta: { title: '我的绩效', requiresAuth: true }
      }
    ]
  },
  {
    path: '*',
    redirect: '/login'
  }
]

const router = new VueRouter({
  mode: 'hash',
  base: process.env.BASE_URL,
  routes
})

// 路由守卫
router.beforeEach((to, from, next) => {
  const token = Cookies.get('token')
  const userRole = Cookies.get('userRole')
  
  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - 员工绩效考核管理系统`
  }
  
  // 需要登录
  if (to.meta.requiresAuth) {
    if (!token) {
      next('/login')
      return
    }
    
    // 需要管理员权限
    if (to.meta.requiresAdmin && userRole !== '管理员') {
      next('/home')
      return
    }
  }
  
  // 已登录用户访问登录页，跳转到首页
  if (to.path === '/login' && token) {
    next('/home')
    return
  }
  
  next()
})

export default router

