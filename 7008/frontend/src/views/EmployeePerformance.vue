<template>
  <div class="page-container">
    <el-card>
      <div slot="header">
        <i class="el-icon-star-off"></i> 我的绩效
      </div>
      
      <el-table
        :data="tableData"
        v-loading="loading"
        border
        stripe
      >
        <el-table-column prop="performance_month" label="考核月份" width="120" align="center" />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="job_level" label="职级" width="80" align="center" />
        <el-table-column label="通用指标" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.common_score || '-' }}
          </template>
        </el-table-column>
        <el-table-column label="专属KPI" width="100" align="center">
          <template slot-scope="scope">
            {{ scope.row.kpi_score || '-' }}
          </template>
        </el-table-column>
        <el-table-column prop="total_score" label="总得分" width="100" align="center">
          <template slot-scope="scope">
            <span style="font-weight: bold; color: #409EFF;">{{ scope.row.total_score }}</span>
          </template>
        </el-table-column>
        <el-table-column prop="performance_level" label="绩效等级" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getRatingType(scope.row.performance_level)">
              {{ scope.row.performance_level }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="remarks" label="备注" show-overflow-tooltip />
        <el-table-column prop="addtime" label="创建时间" width="160" />
        <el-table-column label="操作" width="100" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="text" @click="handleViewDetail(scope.row)">查看详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.page"
        :page-sizes="[10, 20, 50]"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; text-align: right;"
      />
    </el-card>
    
    <!-- 绩效详情对话框 -->
    <el-dialog
      title="绩效考核详情"
      :visible.sync="detailVisible"
      width="800px"
    >
      <div v-if="currentDetail">
        <!-- 基本信息 -->
        <el-descriptions title="基本信息" :column="2" border>
          <el-descriptions-item label="考核月份">{{ currentDetail.performance_month }}</el-descriptions-item>
          <el-descriptions-item label="部门">{{ currentDetail.department }}</el-descriptions-item>
          <el-descriptions-item label="职级">{{ currentDetail.job_level }}</el-descriptions-item>
          <el-descriptions-item label="绩效等级">
            <el-tag :type="getRatingType(currentDetail.performance_level)">
              {{ currentDetail.performance_level }}
            </el-tag>
          </el-descriptions-item>
        </el-descriptions>
        
        <!-- 通用指标 -->
        <el-divider content-position="left">
          <h3 style="margin: 0;"><i class="el-icon-s-data"></i> 通用指标（权重40%）</h3>
        </el-divider>
        <el-row :gutter="20">
          <el-col :span="12">
            <div class="score-item">
              <span class="score-label">工作时长：</span>
              <span class="score-value">{{ currentDetail.work_hours || 0 }} 小时</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="score-item">
              <span class="score-label">资源成本：</span>
              <span class="score-value">{{ currentDetail.resource_cost || 0 }} 元</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="score-item">
              <span class="score-label">上级评分：</span>
              <span class="score-value">{{ currentDetail.supervisor_score || 0 }} 分</span>
            </div>
          </el-col>
          <el-col :span="12">
            <div class="score-item">
              <span class="score-label">同级评分：</span>
              <span class="score-value">{{ currentDetail.peer_score || 0 }} 分</span>
            </div>
          </el-col>
        </el-row>
        <div class="total-score-item">
          <span class="score-label">通用指标得分：</span>
          <span class="score-value highlight">{{ currentDetail.common_score || 0 }} 分</span>
        </div>
        
        <!-- 部门专属KPI -->
        <el-divider content-position="left">
          <h3 style="margin: 0;"><i class="el-icon-trophy"></i> 部门专属KPI（权重60%）</h3>
        </el-divider>
        <div v-if="currentDetail.department_kpi && Object.keys(currentDetail.department_kpi).length > 0">
          <el-row :gutter="20">
            <el-col :span="12" v-for="(value, key) in currentDetail.department_kpi" :key="key">
              <div class="score-item">
                <span class="score-label">{{ getKpiLabel(key) }}：</span>
                <span class="score-value">{{ value }} {{ getKpiUnit(key) }}</span>
              </div>
            </el-col>
          </el-row>
        </div>
        <div v-else style="text-align: center; color: #909399; padding: 20px;">
          暂无KPI数据
        </div>
        <div class="total-score-item">
          <span class="score-label">专属KPI得分：</span>
          <span class="score-value highlight">{{ currentDetail.kpi_score || 0 }} 分</span>
        </div>
        
        <!-- 总分 -->
        <el-divider></el-divider>
        <div class="final-score">
          <div class="final-score-item">
            <span class="final-label">总得分：</span>
            <span class="final-value">{{ currentDetail.total_score || 0 }} 分</span>
          </div>
          <div class="final-score-item">
            <span class="final-label">绩效等级：</span>
            <el-tag size="large" :type="getRatingType(currentDetail.performance_level)">
              {{ currentDetail.performance_level }}
            </el-tag>
          </div>
        </div>
        
        <!-- 备注 -->
        <div v-if="currentDetail.remarks" style="margin-top: 20px;">
          <el-divider content-position="left">备注</el-divider>
          <p style="color: #606266;">{{ currentDetail.remarks }}</p>
        </div>
      </div>
      
      <div slot="footer">
        <el-button @click="detailVisible = false">关闭</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getAppraisalList } from '@/api/appraisal'

export default {
  name: 'EmployeePerformance',
  data() {
    return {
      loading: false,
      tableData: [],
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      detailVisible: false,
      currentDetail: null,
      // KPI字段配置
      kpiConfig: {
        // 技术部
        project_count: { label: '上线项目数量', unit: '个' },
        bug_rate: { label: '代码BUG率', unit: '%' },
        ontime_rate: { label: '项目按时上线率', unit: '%' },
        // 运营市场部
        customer_count: { label: '新增客户数', unit: '个' },
        conversion_rate: { label: '客户转化率', unit: '%' },
        revenue: { label: '营收贡献', unit: '元' },
        // 产品部
        feature_count: { label: '需求完成数', unit: '个' },
        user_satisfaction: { label: '用户满意度', unit: '分' },
        prototype_count: { label: '原型设计数', unit: '个' },
        // 人力资源部
        recruitment_count: { label: '招聘完成数', unit: '人' },
        training_hours: { label: '培训时长', unit: '小时' },
        employee_retention: { label: '员工留存率', unit: '%' },
        // 财务部
        report_accuracy: { label: '报表准确率', unit: '%' },
        audit_pass_rate: { label: '审计通过率', unit: '%' },
        cost_saving: { label: '成本节约', unit: '元' }
      }
    }
  },
  mounted() {
    this.loadData()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const userInfo = this.$store.getters.userInfo
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
          employee_number: userInfo.employee_number
        }
        const res = await getAppraisalList(params)
        this.tableData = res.data.list
        this.pagination.total = res.data.total
      } catch (error) {
        console.error('加载数据失败:', error)
      } finally {
        this.loading = false
      }
    },
    
    getRatingType(rating) {
      const typeMap = {
        'S': 'success',
        'A': 'primary',
        'B': 'warning',
        'C': 'warning',
        'D': 'danger'
      }
      return typeMap[rating] || 'info'
    },
    
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadData()
    },
    
    handleCurrentChange(val) {
      this.pagination.page = val
      this.loadData()
    },
    
    handleViewDetail(row) {
      this.currentDetail = row
      this.detailVisible = true
    },
    
    getKpiLabel(key) {
      return this.kpiConfig[key] ? this.kpiConfig[key].label : key
    },
    
    getKpiUnit(key) {
      return this.kpiConfig[key] ? this.kpiConfig[key].unit : ''
    }
  }
}
</script>

<style scoped>
.page-container {
  padding: 20px;
}

.score-item {
  padding: 15px;
  background: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 10px;
}

.score-label {
  font-weight: bold;
  color: #606266;
  margin-right: 10px;
}

.score-value {
  color: #409EFF;
  font-size: 16px;
}

.score-value.highlight {
  font-size: 18px;
  font-weight: bold;
  color: #67C23A;
}

.total-score-item {
  padding: 20px;
  background: #ecf5ff;
  border-radius: 4px;
  margin-top: 15px;
  text-align: center;
  border-left: 4px solid #409EFF;
}

.final-score {
  display: flex;
  justify-content: space-around;
  align-items: center;
  padding: 30px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 8px;
  color: white;
}

.final-score-item {
  text-align: center;
}

.final-label {
  font-size: 18px;
  font-weight: bold;
  display: block;
  margin-bottom: 10px;
}

.final-value {
  font-size: 32px;
  font-weight: bold;
}
</style>

