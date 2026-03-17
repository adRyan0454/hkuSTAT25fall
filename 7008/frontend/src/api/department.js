import request from '@/utils/request'

/**
 * 获取部门列表（分页）
 */
export function getDepartmentList(params) {
  return request({
    url: '/api/department/list',
    method: 'get',
    params
  })
}

/**
 * 获取所有部门（不分页）
 */
export function getAllDepartments() {
  return request({
    url: '/api/department/all',
    method: 'get'
  })
}

/**
 * 获取部门详情
 */
export function getDepartment(id) {
  return request({
    url: `/api/department/${id}`,
    method: 'get'
  })
}

/**
 * 创建部门
 */
export function createDepartment(data) {
  return request({
    url: '/api/department/create',
    method: 'post',
    data
  })
}

/**
 * 更新部门
 */
export function updateDepartment(id, data) {
  return request({
    url: `/api/department/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除部门
 */
export function deleteDepartment(id) {
  return request({
    url: `/api/department/delete/${id}`,
    method: 'delete'
  })
}

