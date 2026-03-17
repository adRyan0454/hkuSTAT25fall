import request from '@/utils/request'

/**
 * 获取岗位列表（分页）
 */
export function getPositionList(params) {
  return request({
    url: '/api/position/list',
    method: 'get',
    params
  })
}

/**
 * 获取所有岗位（不分页）
 */
export function getAllPositions() {
  return request({
    url: '/api/position/all',
    method: 'get'
  })
}

/**
 * 获取岗位详情
 */
export function getPosition(id) {
  return request({
    url: `/api/position/${id}`,
    method: 'get'
  })
}

/**
 * 创建岗位
 */
export function createPosition(data) {
  return request({
    url: '/api/position/create',
    method: 'post',
    data
  })
}

/**
 * 更新岗位
 */
export function updatePosition(id, data) {
  return request({
    url: `/api/position/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除岗位
 */
export function deletePosition(id) {
  return request({
    url: `/api/position/delete/${id}`,
    method: 'delete'
  })
}

