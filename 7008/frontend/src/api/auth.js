import request from '@/utils/request'

/**
 * 管理员登录
 */
export function adminLogin(data) {
  return request({
    url: '/api/auth/login/admin',
    method: 'post',
    data
  })
}

/**
 * 员工登录
 */
export function employeeLogin(data) {
  return request({
    url: '/api/auth/login/employee',
    method: 'post',
    data
  })
}

/**
 * 退出登录
 */
export function logout() {
  return request({
    url: '/api/auth/logout',
    method: 'post'
  })
}

