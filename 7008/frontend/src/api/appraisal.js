import request from '@/utils/request'

/**
 * 获取绩效考核列表（分页）
 */
export function getAppraisalList(params) {
  return request({
    url: '/api/appraisal/list',
    method: 'get',
    params
  })
}

/**
 * 获取绩效考核详情
 */
export function getAppraisal(id) {
  return request({
    url: `/api/appraisal/${id}`,
    method: 'get'
  })
}

/**
 * 创建绩效考核
 */
export function createAppraisal(data) {
  return request({
    url: '/api/appraisal/create',
    method: 'post',
    data
  })
}

/**
 * 更新绩效考核
 */
export function updateAppraisal(id, data) {
  return request({
    url: `/api/appraisal/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除绩效考核
 */
export function deleteAppraisal(id) {
  return request({
    url: `/api/appraisal/delete/${id}`,
    method: 'delete'
  })
}

