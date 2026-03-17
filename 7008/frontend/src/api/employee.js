import request from '@/utils/request'

/**
 * 获取员工列表（分页）
 */
export function getEmployeeList(params) {
  return request({
    url: '/api/employee/list',
    method: 'get',
    params
  })
}

/**
 * 获取员工详情
 */
export function getEmployee(id) {
  return request({
    url: `/api/employee/${id}`,
    method: 'get'
  })
}

/**
 * 创建员工
 */
export function createEmployee(data) {
  return request({
    url: '/api/employee/create',
    method: 'post',
    data
  })
}

/**
 * 更新员工
 */
export function updateEmployee(id, data) {
  return request({
    url: `/api/employee/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除员工
 */
export function deleteEmployee(id) {
  return request({
    url: `/api/employee/delete/${id}`,
    method: 'delete'
  })
}

/**
 * 上传员工照片
 */
export function uploadPhoto(file) {
  const formData = new FormData()
  formData.append('file', file)
  return request({
    url: '/api/employee/upload',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

