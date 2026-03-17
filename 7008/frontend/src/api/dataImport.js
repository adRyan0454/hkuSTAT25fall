import request from '@/utils/request'

/**
 * 导入 Excel 文件
 */
export function importExcel(file, updateExisting = false) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: `/api/import/excel?update_existing=${updateExisting}`,
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    },
    timeout: 60000 // 60秒超时
  })
}

/**
 * 预览 Excel 文件
 */
export function previewExcel(file) {
  const formData = new FormData()
  formData.append('file', file)
  
  return request({
    url: '/api/import/excel/preview',
    method: 'post',
    data: formData,
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  })
}

/**
 * 获取导入模板说明
 */
export function getImportTemplate() {
  return request({
    url: '/api/import/template',
    method: 'get'
  })
}
