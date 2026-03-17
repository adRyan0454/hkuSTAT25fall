<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="card-header">
        <span><i class="el-icon-document"></i> 绩效指标管理</span>
        <el-button type="primary" size="small" @click="handleAdd">
          <i class="el-icon-plus"></i> 新增指标
        </el-button>
      </div>
      
      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-form :inline="true" :model="searchForm">
          <el-form-item>
            <el-select v-model="searchForm.department" placeholder="部门" clearable>
              <el-option v-for="item in departmentList" :key="item.id" :label="item.department" :value="item.department" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-select v-model="searchForm.position" placeholder="岗位" clearable>
              <el-option v-for="item in positionList" :key="item.id" :label="item.position" :value="item.position" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-input v-model="searchForm.project" placeholder="绩效项目" clearable />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="handleSearch">
              <i class="el-icon-search"></i> 搜索
            </el-button>
          </el-form-item>
        </el-form>
      </div>
      
      <!-- 表格 -->
      <el-table
        :data="tableData"
        v-loading="loading"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="60" align="center" />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="position" label="岗位" width="120" />
        <el-table-column prop="project" label="绩效项目" width="150" />
        <el-table-column label="指标1" width="200">
          <template slot-scope="scope">
            {{ scope.row.indicator1 }} ({{ scope.row.score1 }}分)
          </template>
        </el-table-column>
        <el-table-column label="指标2" width="200">
          <template slot-scope="scope">
            {{ scope.row.indicator2 }} ({{ scope.row.score2 }}分)
          </template>
        </el-table-column>
        <el-table-column label="指标3" width="200">
          <template slot-scope="scope">
            {{ scope.row.indicator3 }} ({{ scope.row.score3 }}分)
          </template>
        </el-table-column>
        <el-table-column prop="total_score" label="总评分" width="100" align="center" />
        <el-table-column prop="addtime" label="创建时间" width="160" />
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button type="primary" size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button type="danger" size="mini" @click="handleDelete(scope.row)">删除</el-button>
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
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部门" prop="department">
              <el-select v-model="form.department" placeholder="请选择部门" style="width: 100%;">
                <el-option v-for="item in departmentList" :key="item.id" :label="item.department" :value="item.department" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="岗位" prop="position">
              <el-select v-model="form.position" placeholder="请选择岗位" style="width: 100%;">
                <el-option v-for="item in positionList" :key="item.id" :label="item.position" :value="item.position" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="绩效项目" prop="project">
          <el-input v-model="form.project" placeholder="请输入绩效项目名称" />
        </el-form-item>
        
        <el-row :gutter="20">
          <el-col :span="16">
            <el-form-item label="指标1" prop="indicator1">
              <el-input v-model="form.indicator1" placeholder="请输入指标1" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="分值1" prop="score1">
              <el-input-number v-model="form.score1" :min="0" :max="100" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="16">
            <el-form-item label="指标2" prop="indicator2">
              <el-input v-model="form.indicator2" placeholder="请输入指标2" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="分值2" prop="score2">
              <el-input-number v-model="form.score2" :min="0" :max="100" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="16">
            <el-form-item label="指标3" prop="indicator3">
              <el-input v-model="form.indicator3" placeholder="请输入指标3" />
            </el-form-item>
          </el-col>
          <el-col :span="8">
            <el-form-item label="分值3" prop="score3">
              <el-input-number v-model="form.score3" :min="0" :max="100" style="width: 100%;" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-form-item label="总评分" prop="total_score">
          <el-input v-model="form.total_score" placeholder="总评分（可自动计算）" :disabled="true" />
        </el-form-item>
      </el-form>
      
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getIndicatorList, createIndicator, updateIndicator, deleteIndicator } from '@/api/indicator'
import { getAllDepartments } from '@/api/department'
import { getAllPositions } from '@/api/position'

export default {
  name: 'Indicator',
  data() {
    return {
      loading: false,
      submitLoading: false,
      tableData: [],
      departmentList: [],
      positionList: [],
      searchForm: {
        department: '',
        position: '',
        project: ''
      },
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '新增指标',
      isEdit: false,
      form: {
        id: null,
        department: '',
        position: '',
        project: '',
        indicator1: '',
        score1: 0,
        indicator2: '',
        score2: 0,
        indicator3: '',
        score3: 0,
        total_score: ''
      },
      rules: {
        department: [
          { required: true, message: '请选择部门', trigger: 'change' }
        ],
        position: [
          { required: true, message: '请选择岗位', trigger: 'change' }
        ],
        project: [
          { required: true, message: '请输入绩效项目', trigger: 'blur' }
        ]
      }
    }
  },
  watch: {
    'form.score1': 'calculateTotalScore',
    'form.score2': 'calculateTotalScore',
    'form.score3': 'calculateTotalScore'
  },
  mounted() {
    this.loadData()
    this.loadDepartmentList()
    this.loadPositionList()
  },
  methods: {
    calculateTotalScore() {
      const total = (this.form.score1 || 0) + (this.form.score2 || 0) + (this.form.score3 || 0)
      this.form.total_score = total.toString()
    },
    
    async loadData() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
          ...this.searchForm
        }
        const res = await getIndicatorList(params)
        this.tableData = res.data.list
        this.pagination.total = res.data.total
      } catch (error) {
        console.error('加载数据失败:', error)
      } finally {
        this.loading = false
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
    
    async loadPositionList() {
      try {
        const res = await getAllPositions()
        this.positionList = res.data || []
      } catch (error) {
        console.error('加载岗位列表失败:', error)
      }
    },
    
    handleSearch() {
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
      this.dialogTitle = '新增指标'
      this.isEdit = false
      this.dialogVisible = true
    },
    
    handleEdit(row) {
      this.dialogTitle = '编辑指标'
      this.isEdit = true
      this.form = { ...row }
      this.dialogVisible = true
    },
    
    handleDelete(row) {
      this.$confirm('确定要删除该指标吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteIndicator(row.id)
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
            await updateIndicator(this.form.id, this.form)
            this.$message.success('更新成功')
          } else {
            await createIndicator(this.form)
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
        department: '',
        position: '',
        project: '',
        indicator1: '',
        score1: 0,
        indicator2: '',
        score2: 0,
        indicator3: '',
        score3: 0,
        total_score: ''
      }
      if (this.$refs.form) {
        this.$refs.form.resetFields()
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

