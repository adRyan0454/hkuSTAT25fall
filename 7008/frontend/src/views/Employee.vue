<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="card-header">
        <span><i class="el-icon-user"></i> 员工管理</span>
        <el-button type="primary" size="small" @click="handleAdd">
          <i class="el-icon-plus"></i> 新增员工
        </el-button>
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
      
      <!-- 表格 -->
      <el-table
        :data="tableData"
        v-loading="loading"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="60" align="center" />
        <el-table-column prop="employee_number" label="工号" width="120" />
        <el-table-column prop="employee_name" label="姓名" width="100" />
        <el-table-column prop="age" label="年龄" width="80" align="center" />
        <el-table-column prop="education" label="最高学历" width="100" />
        <el-table-column prop="department" label="部门" width="120" />
        <el-table-column prop="supervisor_number" label="领导工号" width="120" />
        <el-table-column prop="job_level" label="职级" width="100" />
        <el-table-column prop="join_date" label="入职时间" width="120" />
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
            <el-form-item label="员工工号" prop="employee_number">
              <el-input v-model="form.employee_number" placeholder="请输入员工工号" :disabled="isEdit" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="员工姓名" prop="employee_name">
              <el-input v-model="form.employee_name" placeholder="请输入员工姓名" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="年龄" prop="age">
              <el-input-number v-model="form.age" :min="18" :max="100" placeholder="请输入年龄" style="width: 100%;" />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="最高学历" prop="education">
              <el-select v-model="form.education" placeholder="请选择学历" style="width: 100%;">
                <el-option label="高中" value="高中" />
                <el-option label="大专" value="大专" />
                <el-option label="本科" value="本科" />
                <el-option label="硕士" value="硕士" />
                <el-option label="博士" value="博士" />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="部门" prop="department">
              <el-select v-model="form.department" placeholder="请选择部门" style="width: 100%;">
                <el-option v-for="item in departmentList" :key="item.id" :label="item.department" :value="item.department" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="领导工号" prop="supervisor_number">
              <el-input v-model="form.supervisor_number" placeholder="请输入领导工号" />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="职级" prop="job_level">
              <el-select v-model="form.job_level" placeholder="请选择职级" style="width: 100%;">
                <el-option label="P1" value="P1" />
                <el-option label="P2" value="P2" />
                <el-option label="P3" value="P3" />
                <el-option label="P4" value="P4" />
                <el-option label="P5" value="P5" />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="入职时间" prop="join_date">
              <el-date-picker
                v-model="form.join_date"
                type="date"
                placeholder="选择入职时间"
                value-format="yyyy-MM-dd"
                style="width: 100%;"
              />
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="密码" prop="password">
              <el-input v-model="form.password" type="password" placeholder="请输入密码" />
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      
      <div slot="footer">
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleSubmit" :loading="submitLoading">确定</el-button>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import { getEmployeeList, createEmployee, updateEmployee, deleteEmployee } from '@/api/employee'
import { getAllDepartments } from '@/api/department'

export default {
  name: 'Employee',
  data() {
    return {
      loading: false,
      submitLoading: false,
      tableData: [],
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
      dialogVisible: false,
      dialogTitle: '新增员工',
      isEdit: false,
      form: {
        id: null,
        employee_number: '',
        employee_name: '',
        age: null,
        education: '',
        department: '',
        supervisor_number: '',
        job_level: '',
        join_date: '',
        password: '123456'
      },
      rules: {
        employee_number: [
          { required: true, message: '请输入员工工号', trigger: 'blur' }
        ],
        employee_name: [
          { required: true, message: '请输入员工姓名', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.loadData()
    this.loadDepartmentList()
  },
  methods: {
    async loadData() {
      this.loading = true
      try {
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
          ...this.searchForm
        }
        const res = await getEmployeeList(params)
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
      this.dialogTitle = '新增员工'
      this.isEdit = false
      this.dialogVisible = true
    },
    
    handleEdit(row) {
      this.dialogTitle = '编辑员工'
      this.isEdit = true
      this.form = { ...row }
      this.dialogVisible = true
    },
    
    handleDelete(row) {
      this.$confirm('确定要删除该员工吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteEmployee(row.id)
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
            await updateEmployee(this.form.id, this.form)
            this.$message.success('更新成功')
          } else {
            await createEmployee(this.form)
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
        age: null,
        education: '',
        department: '',
        supervisor_number: '',
        job_level: '',
        join_date: '',
        password: '123456'
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

