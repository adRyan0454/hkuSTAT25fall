<template>
  <div class="analytics-container">
    <!-- 部门绩效对比 -->
    <el-card class="chart-card">
      <div slot="header" class="card-header">
        <span><i class="el-icon-data-analysis"></i> 部门绩效对比</span>
        <el-date-picker
          v-model="selectedMonth"
          type="month"
          placeholder="选择月份"
          value-format="yyyy-MM"
          @change="loadDepartmentData"
          size="small"
        />
      </div>
      
      <el-row :gutter="20">
        <!-- 部门得分柱状图 -->
        <el-col :span="16">
          <div class="chart-title">各部门平均绩效得分</div>
          <div id="departmentBarChart" style="width: 100%; height: 400px;"></div>
        </el-col>
        
        <!-- 部门维度饼图 -->
        <el-col :span="8">
          <div class="chart-title">选择部门查看维度分布</div>
          <el-select v-model="selectedDepartment" placeholder="选择部门" @change="loadDepartmentDetail" style="width: 100%; margin-bottom: 10px;">
            <el-option
              v-for="dept in departmentList"
              :key="dept"
              :label="dept"
              :value="dept"
            />
          </el-select>
          <div id="departmentPieChart" style="width: 100%; height: 350px;"></div>
        </el-col>
      </el-row>
      
      <!-- 部门详细数据表格 -->
      <el-divider></el-divider>
      <div class="chart-title">部门绩效详细数据</div>
      <el-table :data="departmentTableData" border stripe style="margin-top: 10px;">
        <el-table-column prop="department" label="部门" width="150" align="center" />
        <el-table-column prop="employee_count" label="员工数" width="100" align="center" />
        <el-table-column prop="avg_common_score" label="平均通用得分" width="130" align="center">
          <template slot-scope="scope">
            {{ scope.row.avg_common_score.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="avg_kpi_score" label="平均KPI得分" width="130" align="center">
          <template slot-scope="scope">
            {{ scope.row.avg_kpi_score.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="avg_total_score" label="平均总分" width="120" align="center">
          <template slot-scope="scope">
            <strong style="color: #409EFF;">{{ scope.row.avg_total_score.toFixed(2) }}</strong>
          </template>
        </el-table-column>
        <el-table-column label="等级分布" align="center">
          <template slot-scope="scope">
            <el-tag v-for="(count, level) in scope.row.level_distribution" :key="level" :type="getLevelType(level)" size="small" style="margin: 0 2px;">
              {{ level }}:{{ count }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
    
    <!-- 员工绩效趋势分析 -->
    <el-card class="chart-card" style="margin-top: 20px;">
      <div slot="header" class="card-header">
        <span><i class="el-icon-trend-charts"></i> 员工绩效趋势分析</span>
        <div>
          <el-select v-model="trendDepartment" placeholder="选择部门" @change="loadTrendData" size="small" style="width: 150px; margin-right: 10px;">
            <el-option label="全部部门" value="" />
            <el-option
              v-for="dept in departmentList"
              :key="dept"
              :label="dept"
              :value="dept"
            />
          </el-select>
          <el-select v-model="trendEmployee" placeholder="选择员工" @change="loadTrendData" size="small" style="width: 200px;" clearable>
            <el-option
              v-for="emp in employeeList"
              :key="emp.employee_number"
              :label="`${emp.employee_name} (${emp.employee_number})`"
              :value="emp.employee_number"
            />
          </el-select>
        </div>
      </div>
      
      <el-row :gutter="20">
        <!-- 趋势折线图 -->
        <el-col :span="24">
          <div class="chart-title">绩效得分趋势</div>
          <div id="trendLineChart" style="width: 100%; height: 400px;"></div>
        </el-col>
      </el-row>
      
      <!-- 趋势数据表格 -->
      <el-divider></el-divider>
      <div class="chart-title">趋势数据详情</div>
      <el-table :data="trendTableData" border stripe style="margin-top: 10px;">
        <el-table-column prop="performance_month" label="月份" width="120" align="center" />
        <el-table-column prop="employee_count" label="员工数" width="100" align="center" />
        <el-table-column prop="avg_total_score" label="平均总分" width="120" align="center">
          <template slot-scope="scope">
            <strong style="color: #409EFF;">{{ scope.row.avg_total_score.toFixed(2) }}</strong>
          </template>
        </el-table-column>
        <el-table-column prop="max_score" label="最高分" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.max_score.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column prop="min_score" label="最低分" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.min_score.toFixed(2) }}
          </template>
        </el-table-column>
        <el-table-column label="等级分布" align="center">
          <template slot-scope="scope">
            <el-tag v-for="(count, level) in scope.row.level_distribution" :key="level" :type="getLevelType(level)" size="small" style="margin: 0 2px;">
              {{ level }}:{{ count }}
            </el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
import * as echarts from 'echarts'
import { getAppraisalList } from '@/api/appraisal'
import { getEmployeeList } from '@/api/employee'

export default {
  name: 'Analytics',
  data() {
    return {
      selectedMonth: '',
      selectedDepartment: '',
      trendDepartment: '',
      trendEmployee: '',
      departmentList: ['技术部', '运营市场部', '产品部', '人力资源部', '财务部'],
      employeeList: [],
      departmentTableData: [],
      trendTableData: [],
      barChart: null,
      pieChart: null,
      lineChart: null,
      allAppraisalData: []
    }
  },
  mounted() {
    // 设置默认月份为当前月份
    const now = new Date()
    this.selectedMonth = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`
    
    this.initCharts()
    this.loadAllData()
    this.loadEmployeeList()
  },
  beforeDestroy() {
    if (this.barChart) this.barChart.dispose()
    if (this.pieChart) this.pieChart.dispose()
    if (this.lineChart) this.lineChart.dispose()
  },
  methods: {
    getLevelType(level) {
      const typeMap = {
        'S': 'danger',
        'A': 'success',
        'B': '',
        'C': 'warning',
        'D': 'info'
      }
      return typeMap[level] || 'info'
    },
    
    initCharts() {
      this.barChart = echarts.init(document.getElementById('departmentBarChart'))
      this.pieChart = echarts.init(document.getElementById('departmentPieChart'))
      this.lineChart = echarts.init(document.getElementById('trendLineChart'))
      
      // 响应式
      window.addEventListener('resize', () => {
        this.barChart.resize()
        this.pieChart.resize()
        this.lineChart.resize()
      })
    },
    
    async loadAllData() {
      try {
        // 加载所有绩效数据
        const res = await getAppraisalList({ page: 1, page_size: 10000 })
        this.allAppraisalData = res.data.list || []
        
        this.loadDepartmentData()
        this.loadTrendData()
      } catch (error) {
        console.error('加载数据失败:', error)
        this.$message.error('加载数据失败')
      }
    },
    
    async loadEmployeeList() {
      try {
        const res = await getEmployeeList({ page: 1, page_size: 1000 })
        this.employeeList = res.data.list || []
      } catch (error) {
        console.error('加载员工列表失败:', error)
      }
    },
    
    loadDepartmentData() {
      // 筛选当前月份的数据
      const monthData = this.allAppraisalData.filter(item => 
        item.performance_month === this.selectedMonth
      )
      
      if (monthData.length === 0) {
        this.$message.warning('该月份暂无数据')
        this.departmentTableData = []
        this.updateBarChart([])
        return
      }
      
      // 按部门统计
      const deptStats = {}
      this.departmentList.forEach(dept => {
        deptStats[dept] = {
          department: dept,
          employee_count: 0,
          total_common_score: 0,
          total_kpi_score: 0,
          total_score: 0,
          level_distribution: {}
        }
      })
      
      monthData.forEach(item => {
        const dept = item.department
        if (deptStats[dept]) {
          deptStats[dept].employee_count++
          deptStats[dept].total_common_score += item.common_score || 0
          deptStats[dept].total_kpi_score += item.kpi_score || 0
          deptStats[dept].total_score += item.total_score || 0
          
          const level = item.performance_level || 'N/A'
          deptStats[dept].level_distribution[level] = (deptStats[dept].level_distribution[level] || 0) + 1
        }
      })
      
      // 计算平均值
      this.departmentTableData = Object.values(deptStats).map(dept => ({
        department: dept.department,
        employee_count: dept.employee_count,
        avg_common_score: dept.employee_count > 0 ? dept.total_common_score / dept.employee_count : 0,
        avg_kpi_score: dept.employee_count > 0 ? dept.total_kpi_score / dept.employee_count : 0,
        avg_total_score: dept.employee_count > 0 ? dept.total_score / dept.employee_count : 0,
        level_distribution: dept.level_distribution
      })).filter(dept => dept.employee_count > 0)
      
      this.updateBarChart(this.departmentTableData)
      
      // 默认选择第一个部门
      if (this.departmentTableData.length > 0 && !this.selectedDepartment) {
        this.selectedDepartment = this.departmentTableData[0].department
        this.loadDepartmentDetail()
      }
    },
    
    loadDepartmentDetail() {
      if (!this.selectedDepartment) return
      
      // 获取选中部门的数据
      const deptData = this.allAppraisalData.filter(item => 
        item.department === this.selectedDepartment && 
        item.performance_month === this.selectedMonth
      )
      
      if (deptData.length === 0) {
        this.updatePieChart([])
        return
      }
      
      // 计算四个维度的平均得分
      let totalCommon = 0
      let totalKpi = 0
      let totalWorkHours = 0
      let totalSupervisor = 0
      let totalPeer = 0
      let count = deptData.length
      
      deptData.forEach(item => {
        totalCommon += item.common_score || 0
        totalKpi += item.kpi_score || 0
        totalWorkHours += item.work_hours || 0
        totalSupervisor += item.supervisor_score || 0
        totalPeer += item.peer_score || 0
      })
      
      const pieData = [
        { name: '通用指标得分', value: (totalCommon / count).toFixed(2) },
        { name: 'KPI得分', value: (totalKpi / count).toFixed(2) },
        { name: '上级评分', value: (totalSupervisor / count).toFixed(2) },
        { name: '同级评分', value: (totalPeer / count).toFixed(2) }
      ]
      
      this.updatePieChart(pieData)
    },
    
    loadTrendData() {
      // 筛选数据
      let filteredData = this.allAppraisalData
      
      if (this.trendDepartment) {
        filteredData = filteredData.filter(item => item.department === this.trendDepartment)
      }
      
      if (this.trendEmployee) {
        filteredData = filteredData.filter(item => item.employee_number === this.trendEmployee)
      }
      
      if (filteredData.length === 0) {
        this.$message.warning('暂无趋势数据')
        this.trendTableData = []
        this.updateLineChart([])
        return
      }
      
      // 按月份统计
      const monthStats = {}
      
      filteredData.forEach(item => {
        const month = item.performance_month
        if (!monthStats[month]) {
          monthStats[month] = {
            performance_month: month,
            employee_count: 0,
            total_score: 0,
            scores: [],
            level_distribution: {}
          }
        }
        
        monthStats[month].employee_count++
        monthStats[month].total_score += item.total_score || 0
        monthStats[month].scores.push(item.total_score || 0)
        
        const level = item.performance_level || 'N/A'
        monthStats[month].level_distribution[level] = (monthStats[month].level_distribution[level] || 0) + 1
      })
      
      // 计算统计值并排序
      this.trendTableData = Object.values(monthStats).map(month => ({
        performance_month: month.performance_month,
        employee_count: month.employee_count,
        avg_total_score: month.total_score / month.employee_count,
        max_score: Math.max(...month.scores),
        min_score: Math.min(...month.scores),
        level_distribution: month.level_distribution
      })).sort((a, b) => a.performance_month.localeCompare(b.performance_month))
      
      this.updateLineChart(this.trendTableData)
    },
    
    updateBarChart(data) {
      const option = {
        title: {
          text: `${this.selectedMonth} 各部门平均绩效得分`,
          left: 'center'
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'shadow'
          }
        },
        xAxis: {
          type: 'category',
          data: data.map(item => item.department),
          axisLabel: {
            interval: 0,
            rotate: 0
          }
        },
        yAxis: {
          type: 'value',
          name: '平均得分',
          min: 0,
          max: 100
        },
        series: [
          {
            name: '平均总分',
            type: 'bar',
            data: data.map(item => item.avg_total_score.toFixed(2)),
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
              formatter: '{c}'
            }
          }
        ]
      }
      
      this.barChart.setOption(option)
    },
    
    updatePieChart(data) {
      const option = {
        title: {
          text: `${this.selectedDepartment} 维度分布`,
          left: 'center'
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a} <br/>{b}: {c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          left: 'left',
          top: 'middle'
        },
        series: [
          {
            name: '得分',
            type: 'pie',
            radius: '60%',
            data: data,
            emphasis: {
              itemStyle: {
                shadowBlur: 10,
                shadowOffsetX: 0,
                shadowColor: 'rgba(0, 0, 0, 0.5)'
              }
            },
            label: {
              formatter: '{b}: {c}'
            }
          }
        ]
      }
      
      this.pieChart.setOption(option)
    },
    
    updateLineChart(data) {
      const option = {
        title: {
          text: '绩效得分趋势',
          left: 'center'
        },
        tooltip: {
          trigger: 'axis'
        },
        legend: {
          data: ['平均总分', '最高分', '最低分'],
          top: 30
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        xAxis: {
          type: 'category',
          boundaryGap: false,
          data: data.map(item => item.performance_month)
        },
        yAxis: {
          type: 'value',
          name: '得分',
          min: 0,
          max: 100
        },
        series: [
          {
            name: '平均总分',
            type: 'line',
            data: data.map(item => item.avg_total_score.toFixed(2)),
            smooth: true,
            itemStyle: {
              color: '#409EFF'
            },
            lineStyle: {
              width: 3
            }
          },
          {
            name: '最高分',
            type: 'line',
            data: data.map(item => item.max_score.toFixed(2)),
            smooth: true,
            itemStyle: {
              color: '#67C23A'
            }
          },
          {
            name: '最低分',
            type: 'line',
            data: data.map(item => item.min_score.toFixed(2)),
            smooth: true,
            itemStyle: {
              color: '#E6A23C'
            }
          }
        ]
      }
      
      this.lineChart.setOption(option)
    }
  }
}
</script>

<style scoped>
.analytics-container {
  padding: 20px;
}

.chart-card {
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.chart-title {
  font-size: 14px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 10px;
}
</style>
