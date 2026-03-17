import request from '@/utils/request'

/**
 * 获取绩效指标列表（分页）
 */
export function getIndicatorList(params) {
  return request({
    url: '/api/indicator/list',
    method: 'get',
    params
  })
}

/**
 * 获取所有绩效指标（不分页）
 */
export function getAllIndicators() {
  return request({
    url: '/api/indicator/all',
    method: 'get'
  })
}

/**
 * 获取绩效指标详情
 */
export function getIndicator(id) {
  return request({
    url: `/api/indicator/${id}`,
    method: 'get'
  })
}

/**
 * 创建绩效指标
 */
export function createIndicator(data) {
  return request({
    url: '/api/indicator/create',
    method: 'post',
    data
  })
}

/**
 * 更新绩效指标
 */
export function updateIndicator(id, data) {
  return request({
    url: `/api/indicator/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除绩效指标
 */
export function deleteIndicator(id) {
  return request({
    url: `/api/indicator/delete/${id}`,
    method: 'delete'
  })
}

