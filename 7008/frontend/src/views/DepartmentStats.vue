<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="card-header">
        <span><i class="el-icon-office-building"></i> 部门情况</span>
      </div>
      
      <!-- 统计表格 -->
      <el-table
        :data="tableData"
        v-loading="loading"
        border
        stripe
        show-summary
        :summary-method="getSummaries"
      >
        <el-table-column prop="department" label="部门名称" width="180" align="center" />
        <el-table-column prop="total_count" label="总人数" width="120" align="center">
          <template slot-scope="scope">
            <el-tag type="success" size="medium">{{ scope.row.total_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="p5_count" label="P5（经理）" width="120" align="center">
          <template slot-scope="scope">
            <el-tag type="danger" size="small">{{ scope.row.p5_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="p4_count" label="P4（主管）" width="120" align="center">
          <template slot-scope="scope">
            <el-tag type="warning" size="small">{{ scope.row.p4_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="p3_count" label="P3（资深）" width="120" align="center">
          <template slot-scope="scope">
            <el-tag type="primary" size="small">{{ scope.row.p3_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="p2_count" label="P2（中级）" width="120" align="center">
          <template slot-scope="scope">
            <el-tag type="info" size="small">{{ scope.row.p2_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="p1_count" label="P1（初级）" width="120" align="center">
          <template slot-scope="scope">
            <el-tag size="small">{{ scope.row.p1_count }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="职级分布" min-width="300">
          <template slot-scope="scope">
            <div class="level-chart">
              <div 
                v-for="level in ['P5', 'P4', 'P3', 'P2', 'P1']" 
                :key="level"
                class="level-bar"
                :style="getLevelBarStyle(scope.row, level)"
              >
                <span class="level-label">{{ level }}</span>
              </div>
            </div>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 图表展示 -->
      <el-row :gutter="20" style="margin-top: 30px;">
        <el-col :span="12">
          <el-card shadow="hover">
            <div slot="header">
              <i class="el-icon-pie-chart"></i> 部门人数分布
            </div>
            <div id="departmentChart" style="height: 350px;"></div>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover">
            <div slot="header">
              <i class="el-icon-s-data"></i> 职级人数分布
            </div>
            <div id="levelChart" style="height: 350px;"></div>
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script>
import { getAllDepartments } from '@/api/department'
import { getEmployeeList } from '@/api/employee'
import * as echarts from 'echarts'

export default {
  name: 'DepartmentStats',
  data() {
    return {
      loading: false,
      tableData: [],
      departmentChart: null,
      levelChart: null
    }
  },
  mounted() {
    this.loadData()
  },
  beforeDestroy() {
    if (this.departmentChart) {
      this.departmentChart.dispose()
    }
    if (this.levelChart) {
      this.levelChart.dispose()
    }
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        // 获取所有部门
        const deptRes = await getAllDepartments()
        
        // 处理部门数据
        let departments = []
        if (Array.isArray(deptRes.data)) {
          departments = deptRes.data
        } else if (deptRes.data && Array.isArray(deptRes.data.list)) {
          departments = deptRes.data.list
        } else {
          this.$message.warning('部门数据格式异常')
          return
        }
        
        // 获取所有员工（不分页）
        const empRes = await getEmployeeList({ page: 1, page_size: 10000 })
        
        // 处理员工数据
        let employees = []
        if (empRes.data && Array.isArray(empRes.data.list)) {
          employees = empRes.data.list
        } else if (Array.isArray(empRes.data)) {
          employees = empRes.data
        } else {
          this.$message.warning('员工数据格式异常')
          return
        }
        
        // 统计每个部门的职级分布
        this.tableData = departments.map(dept => {
          const deptEmployees = employees.filter(emp => emp.department === dept.department)
          
          return {
            department: dept.department,
            total_count: deptEmployees.length,
            p5_count: deptEmployees.filter(emp => emp.job_level === 'P5').length,
            p4_count: deptEmployees.filter(emp => emp.job_level === 'P4').length,
            p3_count: deptEmployees.filter(emp => emp.job_level === 'P3').length,
            p2_count: deptEmployees.filter(emp => emp.job_level === 'P2').length,
            p1_count: deptEmployees.filter(emp => emp.job_level === 'P1').length
          }
        })
        
        // 渲染图表
        this.$nextTick(() => {
          this.renderCharts()
        })
      } catch (error) {
        console.error('加载数据失败:', error)
        this.$message.error('加载数据失败: ' + (error.message || '未知错误'))
      } finally {
        this.loading = false
      }
    },
    
    getSummaries(param) {
      const { columns, data } = param
      const sums = []
      columns.forEach((column, index) => {
        if (index === 0) {
          sums[index] = '合计'
          return
        }
        const values = data.map(item => Number(item[column.property]))
        if (!values.every(value => isNaN(value))) {
          sums[index] = values.reduce((prev, curr) => {
            const value = Number(curr)
            if (!isNaN(value)) {
              return prev + curr
            } else {
              return prev
            }
          }, 0)
        } else {
          sums[index] = ''
        }
      })
      return sums
    },
    
    getLevelBarStyle(row, level) {
      const count = row[`${level.toLowerCase()}_count`]
      const total = row.total_count
      const percentage = total > 0 ? (count / total * 100) : 0
      
      const colors = {
        'P5': '#f56c6c',
        'P4': '#e6a23c',
        'P3': '#409eff',
        'P2': '#909399',
        'P1': '#67c23a'
      }
      
      return {
        width: `${percentage}%`,
        backgroundColor: colors[level],
        minWidth: count > 0 ? '30px' : '0'
      }
    },
    
    renderCharts() {
      this.renderDepartmentChart()
      this.renderLevelChart()
    },
    
    renderDepartmentChart() {
      const chartDom = document.getElementById('departmentChart')
      if (!chartDom) return
      
      if (this.departmentChart) {
        this.departmentChart.dispose()
      }
      this.departmentChart = echarts.init(chartDom)
      
      const option = {
        tooltip: {
          trigger: 'item',
          formatter: '{b}: {c}人 ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left'
        },
        series: [
          {
            name: '部门人数',
            type: 'pie',
            radius: '60%',
            data: this.tableData.map(item => ({
              name: item.department,
              value: item.total_count
            })),
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            label: {
              formatter: '{b}\n{c}人'
            }
          }
        ]
      }
      
      this.departmentChart.setOption(option)
    },
    
    renderLevelChart() {
      const chartDom = document.getElementById('levelChart')
      if (!chartDom) return
      
      if (this.levelChart) {
        this.levelChart.dispose()
      }
      this.levelChart = echarts.init(chartDom)
      
      // 计算各职级总人数
      const levelData = {
        'P5': 0,
        'P4': 0,
        'P3': 0,
        'P2': 0,
        'P1': 0
      }
      
      this.tableData.forEach(dept => {
        levelData['P5'] += dept.p5_count
        levelData['P4'] += dept.p4_count
        levelData['P3'] += dept.p3_count
        levelData['P2'] += dept.p2_count
        levelData['P1'] += dept.p1_count
      })
      
      const option = {
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: ['P5\n经理', 'P4\n主管', 'P3\n资深', 'P2\n中级', 'P1\n初级']
        },
        yAxis: {
          type: 'value',
          name: '人数'
        },
        series: [
          {
            name: '人数',
            type: 'bar',
            data: Object.values(levelData),
            itemStyle: {
              color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                { offset: 0, color: '#83bff6' },
                { offset: 0.5, color: '#188df0' },
                { offset: 1, color: '#188df0' }
              ])
            },
            label: {
              show: true,
              position: 'top',
              formatter: '{c}人'
            }
          }
        ]
      }
      
      this.levelChart.setOption(option)
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 16px;
  font-weight: bold;
}

.level-chart {
  display: flex;
  height: 30px;
  border-radius: 4px;
  overflow: hidden;
}

.level-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 12px;
  font-weight: bold;
  transition: all 0.3s;
}

.level-bar:hover {
  opacity: 0.8;
}

.level-label {
  padding: 0 5px;
  white-space: nowrap;
}
</style>
