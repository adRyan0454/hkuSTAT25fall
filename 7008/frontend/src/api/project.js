import request from '@/utils/request'

/**
 * 获取项目列表（分页）
 */
export function getProjectList(params) {
  return request({
    url: '/api/project/list',
    method: 'get',
    params
  })
}

/**
 * 获取所有项目（不分页）
 */
export function getAllProjects() {
  return request({
    url: '/api/project/all',
    method: 'get'
  })
}

/**
 * 获取项目详情
 */
export function getProject(id) {
  return request({
    url: `/api/project/${id}`,
    method: 'get'
  })
}

/**
 * 创建项目
 */
export function createProject(data) {
  return request({
    url: '/api/project/create',
    method: 'post',
    data
  })
}

/**
 * 更新项目
 */
export function updateProject(id, data) {
  return request({
    url: `/api/project/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除项目
 */
export function deleteProject(id) {
  return request({
    url: `/api/project/delete/${id}`,
    method: 'delete'
  })
}

/**
 * 获取项目成员列表
 */
export function getProjectMembers(projectId) {
  return request({
    url: `/api/project/${projectId}/members`,
    method: 'get'
  })
}

/**
 * 添加项目成员
 */
export function addProjectMember(data) {
  return request({
    url: '/api/project/member/add',
    method: 'post',
    data
  })
}

/**
 * 移除项目成员
 */
export function removeProjectMember(memberId) {
  return request({
    url: `/api/project/member/${memberId}`,
    method: 'delete'
  })
}

/**
 * 获取项目绩效列表
 */
export function getProjectPerformanceList(params) {
  return request({
    url: '/api/project/performance/list',
    method: 'get',
    params
  })
}

/**
 * 创建项目绩效
 */
export function createProjectPerformance(data) {
  return request({
    url: '/api/project/performance/create',
    method: 'post',
    data
  })
}

/**
 * 更新项目绩效
 */
export function updateProjectPerformance(id, data) {
  return request({
    url: `/api/project/performance/update/${id}`,
    method: 'put',
    data
  })
}

/**
 * 删除项目绩效
 */
export function deleteProjectPerformance(id) {
  return request({
    url: `/api/project/performance/delete/${id}`,
    method: 'delete'
  })
}

