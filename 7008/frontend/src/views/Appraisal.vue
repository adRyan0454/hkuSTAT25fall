<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="card-header">
        <span><i class="el-icon-star-off"></i> 绩效考核管理</span>
        <div>
          <el-button type="success" size="small" @click="handleImportExcel">
            <i class="el-icon-upload2"></i> 导入Excel
          </el-button>
          <el-button type="primary" size="small" @click="handleAdd">
            <i class="el-icon-plus"></i> 新增考核
          </el-button>
        </div>
      </div>
      
      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item label="部门">
            <el-select v-model="searchForm.department" placeholder="请选择" clearable style="width: 150px;">
              <el-option v-for="item in departmentList" :key="item.id" :label="item.department" :value="item.department" />
            </el-select>
          </el-form-item>
          <el-form-item label="员工工号">
            <el-input v-model="searchForm.employee_number" placeholder="请输入" clearable style="width: 150px;" />
          </el-form-item>
          <el-form-item label="员工姓名">
            <el-input v-model="searchForm.employee_name" placeholder="请输入" clearable style="width: 150px;" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" icon="el-icon-search" @click="handleSearch">搜索</el-button>
            <el-button icon="el-icon-refresh" @click="handleReset">重置</el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 表格 - 按员工展示近12个月绩效 -->
      <el-table
        :data="tableData"
        v-loading="loading"
        border
        stripe
        style="width: 100%"
      >
        <el-table-column prop="employee_number" label="员工工号" width="120" fixed />
        <el-table-column prop="employee_name" label="员工姓名" width="100" fixed />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="job_level" label="职级" width="80" align="center" />
        
        <!-- 近12个月绩效得分 -->
        <el-table-column 
          v-for="month in recentMonths" 
          :key="month.value" 
          :label="month.label" 
          width="100" 
          align="center"
        >
          <template slot-scope="scope">
            <div v-if="scope.row.monthly_scores && scope.row.monthly_scores[month.value]">
              <div style="font-weight: bold; color: #409EFF;">
                {{ scope.row.monthly_scores[month.value].total_score }}
              </div>
              <el-tag 
                size="mini" 
                :type="getRatingType(scope.row.monthly_scores[month.value].performance_level)"
              >
                {{ scope.row.monthly_scores[month.value].performance_level }}
              </el-tag>
            </div>
            <span v-else style="color: #C0C4CC;">-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="150" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="handleAddForEmployee(scope.row)">新增考核</el-button>
            <el-button type="text" size="mini" @click="handleViewDetail(scope.row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="pagination.page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="pagination.pageSize"
        :total="pagination.total"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; text-align: right;"
      />
    </el-card>
    
    <!-- 新增/编辑对话框 -->
    <el-dialog
      :title="dialogTitle"
      :visible.sync="dialogVisible"
      width="700px"
      @close="resetForm"
    >
      <el-form
        :model="form"
        :rules="rules"
        ref="form"
        label-width="100px"
      >
        <el-form-item label="部门" prop="department">
          <el-select 
            v-model="form.department" 
            placeholder="请先选择部门" 
            @change="handleDepartmentChange" 
            clearable 
            style="width: 100%;"
          >
            <el-option 
              v-for="item in departmentList" 
              :key="item.id" 
              :label="item.department" 
              :value="item.department" 
            />
          </el-select>
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="员工工号" prop="employee_number">
              <el-select 
                v-model="form.employee_number" 
                placeholder="请先选择部门" 
                @change="handleEmployeeChange" 
                :disabled="!form.department"
                filterable
                style="width: 100%;"
              >
                <el-option 
                  v-for="item in filteredEmployeeList" 
                  :key="item.id" 
                  :label="`${item.employee_number} - ${item.employee_name}`" 
                  :value="item.employee_number"
                >
                  <span>{{ item.employee_number }} - {{ item.employee_name }}</span>
                </el-option>
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="员工姓名" prop="employee_name">
              <el-input v-model="form.employee_name" placeholder="自动填充" :disabled="true" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="职级" prop="position">
              <el-input v-model="form.position" placeholder="自动填充" :disabled="true" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="绩效月份" prop="performance_month">
              <el-date-picker
                v-model="form.performance_month"
                type="month"
                placeholder="选择月份"
                value-format="yyyy-MM"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <!-- 绩效评分细则说明 -->
        <el-alert
          title="绩效评分细则"
          type="info"
          :closable="false"
          style="margin-bottom: 20px;"
        >
          <div style="line-height: 1.8;">
            <p><strong>评分体系：通用指标（40%）+ 部门专属KPI（60%）</strong></p>
            <p style="margin-top: 10px;"><strong>一、通用指标（所有部门共有）</strong></p>
            <p style="margin-left: 20px; color: #606266;">
              1. <strong>工作时长</strong>：本月实际工作时长（小时）<br>
              2. <strong>上级评分</strong>：直属上级对员工的综合评价（0-100分）<br>
              3. <strong>同级评分</strong>：同事对员工的协作评价（0-100分）<br>
              4. <strong>资源成本</strong>：员工本月耗费的资源金额（元）
            </p>
            <p style="margin-top: 10px;"><strong>二、部门专属KPI（根据部门自动显示）</strong></p>
            <p style="margin-left: 20px; color: #606266;">
              • <strong>技术部</strong>：上线项目数、代码BUG率、按时上线率<br>
              • <strong>运营市场部</strong>：新增客户数、客户转化率、营收贡献<br>
              • <strong>产品部</strong>：需求完成数、用户满意度、原型设计数<br>
              • <strong>人力资源部</strong>：招聘完成数、培训时长、员工留存率<br>
              • <strong>财务部</strong>：报表准确率、审计通过率、成本节约
            </p>
            <p style="margin-top: 10px;"><strong>三、绩效等级</strong></p>
            <p style="margin-left: 20px; color: #606266;">
              S级（≥90分）| A级（80-89分）| B级（70-79分）| C级（60-69分）| D级（<60分）
            </p>
          </div>
        </el-alert>
        
        <!-- 通用指标 -->
        <div style="margin-bottom: 15px; padding: 10px; background: #f5f7fa; border-radius: 4px;">
          <h4 style="margin: 0 0 15px 0; color: #409EFF;">
            <i class="el-icon-s-data"></i> 通用指标（权重40%）
          </h4>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="工作时长" prop="work_hours">
                <el-input-number v-model="form.work_hours" :min="0" :max="300" :precision="1" style="width: 100%;" />
                <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                  本月实际工作时长（小时）
                </div>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="资源成本" prop="resource_cost">
                <el-input-number v-model="form.resource_cost" :min="0" :max="100000" :precision="2" style="width: 100%;" />
                <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                  员工耗费资源金额（元）
                </div>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="上级评分" prop="supervisor_score">
                <el-input-number v-model="form.supervisor_score" :min="0" :max="100" style="width: 100%;" />
                <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                  直属上级综合评价（0-100分）
                </div>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="同级评分" prop="peer_score">
                <el-input-number v-model="form.peer_score" :min="0" :max="100" style="width: 100%;" />
                <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                  同事协作评价（0-100分）
                </div>
              </el-form-item>
            </el-col>
          </el-row>
        </div>
        
        <!-- 部门专属KPI -->
        <div v-if="form.department" style="margin-bottom: 15px; padding: 10px; background: #f0f9ff; border-radius: 4px;">
          <h4 style="margin: 0 0 15px 0; color: #67C23A;">
            <i class="el-icon-trophy"></i> {{ form.department }} - 专属KPI（权重60%）
          </h4>
          <div v-if="departmentKpiFields.length > 0">
            <el-row :gutter="20">
              <el-col :span="12" v-for="field in departmentKpiFields" :key="field.field">
                <el-form-item :label="field.label" :prop="'department_kpi.' + field.field">
                  <el-input-number 
                    v-model="form.department_kpi[field.field]" 
                    :min="0" 
                    :precision="field.unit === '%' ? 4 : 2"
                    style="width: 100%;" 
                  />
                  <div style="font-size: 12px; color: #909399; margin-top: 5px;">
                    {{ field.scoring_rule.description }}（权重{{ Math.round(field.weight * 100) }}%）
                  </div>
                </el-form-item>
              </el-col>
            </el-row>
          </div>
          <div v-else style="color: #909399; text-align: center; padding: 20px;">
            该部门暂无专属KPI配置
          </div>
        </div>
        
        <!-- 评分结果 -->
        <div style="margin-top: 20px; padding: 15px; background: #fef0f0; border-radius: 4px; border-left: 4px solid #F56C6C;">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-form-item label="通用指标得分">
                <el-input v-model="form.common_score" placeholder="自动计算" :disabled="true">
                  <template slot="append">分（40%）</template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="专属KPI得分">
                <el-input v-model="form.kpi_score" placeholder="自动计算" :disabled="true">
                  <template slot="append">分（60%）</template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="8">
              <el-form-item label="总得分">
                <el-input v-model="form.total_score" placeholder="自动计算" :disabled="true">
                  <template slot="append">分</template>
                </el-input>
              </el-form-item>
            </el-col>
          </el-row>
          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="绩效等级">
                <el-input v-model="form.performance_level" placeholder="自动评级" :disabled="true">
                  <template slot="prepend">
                    <i :class="getLevelIcon(form.performance_level)" :style="{color: getLevelColor(form.performance_level)}"></i>
                  </template>
                </el-input>
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="备注">
                <el-input v-model="form.remarks" placeholder="选填" />
              </el-form-item>
            </el-col>
          </el-row>
        </div>
      </el-form>
      
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </div>
    </el-dialog>
    
    <!-- 导入Excel对话框 -->
    <el-dialog
      title="导入Excel数据"
      :visible.sync="importDialogVisible"
      width="600px"
      @close="resetImportForm"
    >
      <el-alert
        title="导入说明"
        type="info"
        :closable="false"
        style="margin-bottom: 20px;"
      >
        <div style="line-height: 1.8; font-size: 13px;">
          <p><strong>支持的文件格式：</strong>.xls 和 .xlsx</p>
          <p><strong>必填字段：</strong>姓名、员工id、部门、职级、入职时间、统计月份、每月工作时长、上级评分、同级评分、培训投入</p>
          <p><strong>部门专属KPI：</strong>根据部门自动识别对应的KPI指标</p>
          <p style="margin-top: 10px;"><strong>注意事项：</strong></p>
          <ul style="margin: 5px 0 0 20px; padding: 0;">
            <li>确保Excel文件格式正确，字段名称与模板一致</li>
            <li>员工id必须在系统中已存在</li>
            <li>日期格式：YYYY-MM-DD，月份格式：YYYY-MM 或 Mon-YY</li>
          </ul>
        </div>
      </el-alert>
      
      <el-form label-width="120px">
        <el-form-item label="选择文件">
          <el-upload
            ref="upload"
            :auto-upload="false"
            :on-change="handleFileChange"
            :file-list="fileList"
            :limit="1"
            accept=".xls,.xlsx"
            drag
          >
            <i class="el-icon-upload"></i>
            <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
            <div class="el-upload__tip" slot="tip">只能上传 .xls/.xlsx 文件</div>
          </el-upload>
        </el-form-item>
        
        <el-form-item label="更新策略">
          <el-radio-group v-model="importOptions.updateExisting">
            <el-radio :label="false">仅新增（跳过已存在的记录）</el-radio>
            <el-radio :label="true">更新已存在的记录</el-radio>
          </el-radio-group>
        </el-form-item>
      </el-form>
      
      <!-- 导入结果 -->
      <el-alert
        v-if="importResult"
        :title="importResult.success ? '导入成功' : '导入失败'"
        :type="importResult.success ? 'success' : 'error'"
        :closable="false"
        style="margin-top: 20px;"
      >
        <div v-if="importResult.success">
          <p>成功导入 {{ importResult.data.success_count }} 条记录</p>
          <p v-if="importResult.data.failed_count > 0">
            失败 {{ importResult.data.failed_count }} 条记录
          </p>
          <div v-if="importResult.data.errors && importResult.data.errors.length > 0">
            <p><strong>错误详情：</strong></p>
            <ul style="max-height: 200px; overflow-y: auto;">
              <li v-for="(error, index) in importResult.data.errors" :key="index">
                {{ error }}
              </li>
            </ul>
          </div>
        </div>
        <div v-else>
          <p>{{ importResult.message }}</p>
        </div>
      </el-alert>
      
      <div slot="footer">
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleImportSubmit" :loading="importLoading" :disabled="!selectedFile">
          <i class="el-icon-upload"></i> 开始导入
        </el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getAppraisalList, createAppraisal, updateAppraisal, deleteAppraisal } from '@/api/appraisal'
import { getEmployeeList } from '@/api/employee'
import { getAllDepartments } from '@/api/department'
import { importExcel } from '@/api/dataImport'

export default {
  name: 'Appraisal',
  data() {
    return {
      loading: false,
      submitLoading: false,
      tableData: [],
      employeeList: [],
      departmentList: [],
      searchForm: {
        employee_number: '',
        employee_name: '',
        department: ''
      },
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      // 近12个月的月份列表
      recentMonths: [],
      dialogVisible: false,
      // 导入Excel相关
      importDialogVisible: false,
      importLoading: false,
      selectedFile: null,
      fileList: [],
      importOptions: {
        updateExisting: false
      },
      importResult: null,
      dialogTitle: '新增考核',
      isEdit: false,
      form: {
        id: null,
        employee_number: '',
        employee_name: '',
        department: '',
        job_level: '',
        performance_month: '',
        // 通用指标
        work_hours: 0,
        supervisor_score: 0,
        peer_score: 0,
        resource_cost: 0,
        // 部门专属KPI
        department_kpi: {},
        // 评分结果
        common_score: '',
        kpi_score: '',
        total_score: '',
        performance_level: '',
        remarks: ''
      },
      rules: {
        employee_number: [
          { required: true, message: '请选择员工', trigger: 'change' }
        ],
        performance_month: [
          { required: true, message: '请选择绩效月份', trigger: 'change' }
        ]
      },
      // 部门KPI配置
      departmentKpiConfig: {
        '技术部': {
          kpi_fields: [
            { field: 'project_count', label: '上线项目数量', unit: '个', weight: 0.3, scoring_rule: { description: '每完成1个项目得20分，最高100分' } },
            { field: 'bug_rate', label: '代码BUG率', unit: '%', weight: 0.35, scoring_rule: { description: 'BUG率越低分数越高' } },
            { field: 'ontime_rate', label: '项目按时上线率', unit: '%', weight: 0.35, scoring_rule: { description: '按时率直接转换为分数' } }
          ]
        },
        '运营市场部': {
          kpi_fields: [
            { field: 'customer_count', label: '新增客户数', unit: '个', weight: 0.3, scoring_rule: { description: '完成目标100个客户得满分' } },
            { field: 'conversion_rate', label: '客户转化率', unit: '%', weight: 0.35, scoring_rule: { description: '转化率达到15%为满分' } },
            { field: 'revenue', label: '营收贡献', unit: '元', weight: 0.35, scoring_rule: { description: '完成50万营收目标得满分' } }
          ]
        },
        '产品部': {
          kpi_fields: [
            { field: 'feature_count', label: '需求完成数', unit: '个', weight: 0.3, scoring_rule: { description: '完成10个需求为目标' } },
            { field: 'user_satisfaction', label: '用户满意度', unit: '分', weight: 0.35, scoring_rule: { description: '用户满意度评分（0-100）' } },
            { field: 'prototype_count', label: '原型设计数', unit: '个', weight: 0.35, scoring_rule: { description: '完成8个原型设计为目标' } }
          ]
        },
        '人力资源部': {
          kpi_fields: [
            { field: 'recruitment_count', label: '招聘完成数', unit: '人', weight: 0.35, scoring_rule: { description: '完成10人招聘为目标' } },
            { field: 'training_hours', label: '培训时长', unit: '小时', weight: 0.30, scoring_rule: { description: '完成50小时培训为目标' } },
            { field: 'employee_retention', label: '员工留存率', unit: '%', weight: 0.35, scoring_rule: { description: '留存率90%为目标' } }
          ]
        },
        '财务部': {
          kpi_fields: [
            { field: 'report_accuracy', label: '报表准确率', unit: '%', weight: 0.4, scoring_rule: { description: '报表准确率99%为目标' } },
            { field: 'audit_pass_rate', label: '审计通过率', unit: '%', weight: 0.35, scoring_rule: { description: '审计通过率95%为目标' } },
            { field: 'cost_saving', label: '成本节约', unit: '元', weight: 0.25, scoring_rule: { description: '节约成本5万为目标' } }
          ]
        }
      }
    }
  },
  computed: {
    // 根据选择的部门过滤员工列表
    filteredEmployeeList() {
      if (!this.form.department) {
        return []
      }
      return this.employeeList.filter(emp => emp.department === this.form.department)
    },
    // 获取当前部门的KPI字段配置
    departmentKpiFields() {
      if (!this.form.department || !this.departmentKpiConfig[this.form.department]) {
        return []
      }
      return this.departmentKpiConfig[this.form.department].kpi_fields
    }
  },
  watch: {
    // 监听通用指标变化
    'form.work_hours': 'calculateScore',
    'form.supervisor_score': 'calculateScore',
    'form.peer_score': 'calculateScore',
    'form.resource_cost': 'calculateScore',
    // 监听部门KPI变化
    'form.department_kpi': {
      handler: 'calculateScore',
      deep: true
    },
    // 监听部门变化，初始化KPI字段
    'form.department'(newVal) {
      if (newVal && this.departmentKpiConfig[newVal]) {
        // 初始化部门KPI字段
        const kpiData = {}
        this.departmentKpiConfig[newVal].kpi_fields.forEach(field => {
          kpiData[field.field] = 0
        })
        this.$set(this.form, 'department_kpi', kpiData)
      }
    }
  },
  mounted() {
    this.initRecentMonths()
    this.loadData()
    this.loadEmployeeList()
    this.loadDepartmentList()
  },
  methods: {
    // 初始化近12个月的月份列表
    initRecentMonths() {
      const months = []
      const now = new Date()
      for (let i = 11; i >= 0; i--) {
        const date = new Date(now.getFullYear(), now.getMonth() - i, 1)
        const year = date.getFullYear()
        const month = String(date.getMonth() + 1).padStart(2, '0')
        months.push({
          value: `${year}-${month}`,
          label: `${month}月`
        })
      }
      this.recentMonths = months
    },
    
    getRatingType(rating) {
      const typeMap = {
        'S': 'success',
        'A': '',
        'B': 'warning',
        'C': 'warning',
        'D': 'danger'
      }
      return typeMap[rating] || 'info'
    },
    
    getLevelIcon(level) {
      const iconMap = {
        'S': 'el-icon-trophy',
        'A': 'el-icon-medal',
        'B': 'el-icon-star-on',
        'C': 'el-icon-check',
        'D': 'el-icon-close'
      }
      return iconMap[level] || 'el-icon-question'
    },
    
    getLevelColor(level) {
      const colorMap = {
        'S': '#67C23A',
        'A': '#409EFF',
        'B': '#E6A23C',
        'C': '#F56C6C',
        'D': '#909399'
      }
      return colorMap[level] || '#909399'
    },
    
    calculateScore() {
      // 这里只是简单计算，实际应该调用后端API计算
      // 通用指标得分（简化计算，实际应该有更复杂的算法）
      const commonScore = (
        (this.form.supervisor_score || 0) * 0.4 +
        (this.form.peer_score || 0) * 0.3 +
        Math.min(100, (this.form.work_hours || 0) / 1.6) * 0.2 +
        Math.max(0, 100 - (this.form.resource_cost || 0) / 100) * 0.1
      )
      
      // KPI得分（简化计算）
      let kpiScore = 0
      if (this.form.department_kpi && Object.keys(this.form.department_kpi).length > 0) {
        const kpiValues = Object.values(this.form.department_kpi)
        kpiScore = kpiValues.reduce((sum, val) => sum + (val || 0), 0) / kpiValues.length
      }
      
      // 总分 = 通用指标40% + KPI 60%
      const totalScore = commonScore * 0.4 + kpiScore * 0.6
      
      this.form.common_score = commonScore.toFixed(2)
      this.form.kpi_score = kpiScore.toFixed(2)
      this.form.total_score = totalScore.toFixed(2)
      
      // 自动评级
      if (totalScore >= 90) {
        this.form.performance_level = 'S'
      } else if (totalScore >= 80) {
        this.form.performance_level = 'A'
      } else if (totalScore >= 70) {
        this.form.performance_level = 'B'
      } else if (totalScore >= 60) {
        this.form.performance_level = 'C'
      } else {
        this.form.performance_level = 'D'
      }
    },
    
    handleDepartmentChange() {
      // 部门变化时，清空员工选择
      this.form.employee_number = ''
      this.form.employee_name = ''
      this.form.job_level = ''
    },
    
    handleEmployeeChange(employeeNumber) {
      const employee = this.employeeList.find(e => e.employee_number === employeeNumber)
      if (employee) {
        this.form.employee_name = employee.employee_name
        this.form.job_level = employee.job_level
        this.form.department = employee.department
      }
    },
    
    async loadData() {
      this.loading = true
      try {
        // 1. 加载员工列表（分页）
        const employeeParams = {
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
          ...this.searchForm
        }
        const employeeRes = await getEmployeeList(employeeParams)
        const employees = employeeRes.data.list || []
        this.pagination.total = employeeRes.data.total
        
        // 2. 加载所有绩效考核数据（不分页，获取所有数据）
        const appraisalRes = await getAppraisalList({ page: 1, page_size: 10000 })
        const allAppraisals = appraisalRes.data.list || []
        
        // 3. 组织数据：按员工维度，每个员工包含近12个月的绩效数据
        this.tableData = employees.map(employee => {
          // 获取该员工的所有绩效记录
          const employeeAppraisals = allAppraisals.filter(
            a => a.employee_number === employee.employee_number
          )
          
          // 组织成月度得分对象
          const monthly_scores = {}
          employeeAppraisals.forEach(appraisal => {
            if (appraisal.performance_month) {
              monthly_scores[appraisal.performance_month] = {
                total_score: appraisal.total_score,
                performance_level: appraisal.performance_level,
                common_score: appraisal.common_score,
                kpi_score: appraisal.kpi_score,
                id: appraisal.id
              }
            }
          })
          
          return {
            employee_number: employee.employee_number,
            employee_name: employee.employee_name,
            department: employee.department,
            job_level: employee.job_level,
            monthly_scores: monthly_scores
          }
        })
      } catch (error) {
        console.error('加载数据失败:', error)
        this.$message.error('加载数据失败')
      } finally {
        this.loading = false
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
    
    async loadDepartmentList() {
      try {
        const res = await getAllDepartments()
        this.departmentList = res.data || []
      } catch (error) {
        console.error('加载部门列表失败:', error)
      }
    },
    
    handleSearch() {
      this.pagination.page = 1
      this.loadData()
    },
    
    handleReset() {
      this.searchForm = {
        employee_number: '',
        employee_name: '',
        department: ''
      }
      this.pagination.page = 1
      this.loadData()
    },
    
    handleSizeChange(val) {
      this.pagination.pageSize = val
      this.loadData()
    },
    
    handleCurrentChange(val) {
      this.pagination.page = val
      this.loadData()
    },
    
    handleAdd() {
      this.dialogTitle = '新增考核'
      this.isEdit = false
      this.resetForm()
      this.dialogVisible = true
    },
    
    handleAddForEmployee(employee) {
      this.dialogTitle = `新增考核 - ${employee.employee_name}`
      this.isEdit = false
      this.resetForm()
      // 预填充员工信息
      this.form.employee_number = employee.employee_number
      this.form.employee_name = employee.employee_name
      this.form.department = employee.department
      this.form.job_level = employee.job_level
      this.dialogVisible = true
    },
    
    handleViewDetail(employee) {
      // 显示该员工的详细绩效历史
      this.$alert(
        `<div style="max-height: 400px; overflow-y: auto;">
          <h3>${employee.employee_name}（${employee.employee_number}）</h3>
          <p>部门：${employee.department} | 职级：${employee.job_level}</p>
          <table style="width: 100%; border-collapse: collapse; margin-top: 10px;">
            <thead>
              <tr style="background: #f5f7fa;">
                <th style="border: 1px solid #ddd; padding: 8px;">月份</th>
                <th style="border: 1px solid #ddd; padding: 8px;">通用指标</th>
                <th style="border: 1px solid #ddd; padding: 8px;">专属KPI</th>
                <th style="border: 1px solid #ddd; padding: 8px;">总分</th>
                <th style="border: 1px solid #ddd; padding: 8px;">等级</th>
              </tr>
            </thead>
            <tbody>
              ${this.recentMonths.map(month => {
                const score = employee.monthly_scores ? employee.monthly_scores[month.value] : null
                if (score) {
                  return '<tr>' +
                    '<td style="border: 1px solid #ddd; padding: 8px;">' + month.value + '</td>' +
                    '<td style="border: 1px solid #ddd; padding: 8px;">' + (score.common_score || '-') + '</td>' +
                    '<td style="border: 1px solid #ddd; padding: 8px;">' + (score.kpi_score || '-') + '</td>' +
                    '<td style="border: 1px solid #ddd; padding: 8px; font-weight: bold;">' + score.total_score + '</td>' +
                    '<td style="border: 1px solid #ddd; padding: 8px;">' + score.performance_level + '</td>' +
                  '</tr>'
                } else {
                  return '<tr>' +
                    '<td style="border: 1px solid #ddd; padding: 8px;">' + month.value + '</td>' +
                    '<td colspan="4" style="border: 1px solid #ddd; padding: 8px; color: #999; text-align: center;">暂无数据</td>' +
                  '</tr>'
                }
              }).join('')}
            </tbody>
          </table>
        </div>`,
        '绩效详情',
        {
          dangerouslyUseHTMLString: true,
          confirmButtonText: '关闭'
        }
      )
    },
    
    handleEdit(row) {
      this.dialogTitle = '编辑考核'
      this.isEdit = true
      this.form = { ...row }
      this.dialogVisible = true
    },
    
    handleDelete(row) {
      this.$confirm('确定要删除该考核记录吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteAppraisal(row.id)
          this.$message.success('删除成功')
          this.loadData()
        } catch (error) {
          console.error('删除失败:', error)
        }
      }).catch(() => {})
    },
    
    handleSubmit() {
      this.$refs.form.validate(async valid => {
        if (!valid) return
        
        this.submitLoading = true
        try {
          if (this.isEdit) {
            await updateAppraisal(this.form.id, this.form)
            this.$message.success('更新成功')
          } else {
            await createAppraisal(this.form)
            this.$message.success('创建成功')
          }
          this.dialogVisible = false
          this.loadData()
        } catch (error) {
          console.error('提交失败:', error)
        } finally {
          this.submitLoading = false
        }
      })
    },
    
    resetForm() {
      this.form = {
        id: null,
        employee_number: '',
        employee_name: '',
        department: '',
        job_level: '',
        performance_month: '',
        // 通用指标
        work_hours: 0,
        supervisor_score: 0,
        peer_score: 0,
        resource_cost: 0,
        // 部门专属KPI
        department_kpi: {},
        // 评分结果
        common_score: '',
        kpi_score: '',
        total_score: '',
        performance_level: '',
        remarks: ''
      }
      if (this.$refs.form) {
        this.$refs.form.resetFields()
      }
    },
    
    handleReset() {
      this.searchForm = {
        employee_number: '',
        employee_name: '',
        department: ''
      }
      this.pagination.page = 1
      this.loadData()
    },
    
    // 导入Excel相关方法
    handleImportExcel() {
      this.importDialogVisible = true
      this.importResult = null
    },
    
    handleFileChange(file, fileList) {
      this.selectedFile = file.raw
      this.fileList = fileList
    },
    
    async handleImportSubmit() {
      if (!this.selectedFile) {
        this.$message.warning('请先选择要导入的文件')
        return
      }
      
      this.importLoading = true
      this.importResult = null
      
      try {
        const res = await importExcel(this.selectedFile, this.importOptions.updateExisting)
        
        this.importResult = {
          success: true,
          data: res.data
        }
        
        this.$message.success('导入完成')
        
        // 刷新列表
        this.loadData()
        
        // 3秒后自动关闭对话框
        setTimeout(() => {
          if (this.importResult && this.importResult.success) {
            this.importDialogVisible = false
          }
        }, 3000)
      } catch (error) {
        this.importResult = {
          success: false,
          message: error.response?.data?.detail || error.message || '导入失败'
        }
        this.$message.error('导入失败：' + this.importResult.message)
      } finally {
        this.importLoading = false
      }
    },
    
    resetImportForm() {
      this.selectedFile = null
      this.fileList = []
      this.importOptions.updateExisting = false
      this.importResult = null
      if (this.$refs.upload) {
        this.$refs.upload.clearFiles()
      }
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
}

.search-bar {
  margin-bottom: 20px;
}
</style>

