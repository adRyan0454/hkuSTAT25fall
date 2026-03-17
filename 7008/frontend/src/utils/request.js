import axios from 'axios'
import { Message } from 'element-ui'
import Cookies from 'js-cookie'
import router from '@/router'

// 创建axios实例
const service = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 15000 // 请求超时时间
})

// 请求拦截器
service.interceptors.request.use(
  config => {
    // 从Cookie中获取token
    const token = Cookies.get('token')
    if (token) {
      config.headers['Authorization'] = `Bearer ${token}`
    }
    return config
  },
  error => {
    console.error('Request error:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
service.interceptors.response.use(
  response => {
    const res = response.data
    
    // 如果返回的状态码不是200，则报错
    if (res.code !== 200) {
      Message({
        message: res.msg || 'Error',
        type: 'error',
        duration: 3000
      })
      
      // 401: 未授权，跳转到登录页
      if (response.status === 401) {
        Cookies.remove('token')
        Cookies.remove('userInfo')
        router.push('/login')
      }
      
      return Promise.reject(new Error(res.msg || 'Error'))
    } else {
      return res
    }
  },
  error => {
    console.error('Response error:', error)
    
    if (error.response) {
      if (error.response.status === 401) {
        Message({
          message: '登录已过期，请重新登录',
          type: 'error',
          duration: 3000
        })
        Cookies.remove('token')
        Cookies.remove('userInfo')
        router.push('/login')
      } else {
        Message({
          message: error.response.data.detail || error.message || '请求失败',
          type: 'error',
          duration: 3000
        })
      }
    } else {
      Message({
        message: '网络连接失败，请检查后端服务是否启动',
        type: 'error',
        duration: 3000
      })
    }
    
    return Promise.reject(error)
  }
)

export default service

