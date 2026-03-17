<template>
  <div class="page-container">
    <el-card>
      <div slot="header" class="card-header">
        <span><i class="el-icon-office-building"></i> 部门管理</span>
        <el-button type="primary" size="small" @click="handleAdd">
          <i class="el-icon-plus"></i> 新增部门
        </el-button>
      </div>
      
      <!-- 搜索栏 -->
      <div class="search-bar">
        <el-input
          v-model="searchForm.department"
          placeholder="请输入部门名称"
          clearable
          style="width: 300px;"
          @keyup.enter.native="handleSearch"
        >
          <el-button slot="append" icon="el-icon-search" @click="handleSearch"></el-button>
        </el-input>
      </div>
      
      <!-- 表格 -->
      <el-table
        :data="tableData"
        v-loading="loading"
        border
        stripe
      >
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="department" label="部门名称" />
        <el-table-column prop="addtime" label="创建时间" width="180" />
        <el-table-column label="操作" width="200" align="center">
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
      width="500px"
      @close="resetForm"
    >
      <el-form
        :model="form"
        :rules="rules"
        ref="form"
        label-width="100px"
      >
        <el-form-item label="部门名称" prop="department">
          <el-input v-model="form.department" placeholder="请输入部门名称" />
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
import { getDepartmentList, createDepartment, updateDepartment, deleteDepartment } from '@/api/department'

export default {
  name: 'Department',
  data() {
    return {
      loading: false,
      submitLoading: false,
      tableData: [],
      searchForm: {
        department: ''
      },
      pagination: {
        page: 1,
        pageSize: 10,
        total: 0
      },
      dialogVisible: false,
      dialogTitle: '新增部门',
      isEdit: false,
      form: {
        id: null,
        department: ''
      },
      rules: {
        department: [
          { required: true, message: '请输入部门名称', trigger: 'blur' }
        ]
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
        const params = {
          page: this.pagination.page,
          page_size: this.pagination.pageSize,
          ...this.searchForm
        }
        const res = await getDepartmentList(params)
        
        // 处理响应数据
        if (res.data && res.data.list) {
          this.tableData = res.data.list
          this.pagination.total = res.data.total || 0
        } else {
          this.tableData = []
          this.pagination.total = 0
        }
      } catch (error) {
        console.error('加载数据失败:', error)
        this.$message.error('加载数据失败: ' + (error.message || '未知错误'))
      } finally {
        this.loading = false
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
      this.dialogTitle = '新增部门'
      this.isEdit = false
      this.dialogVisible = true
    },
    
    handleEdit(row) {
      this.dialogTitle = '编辑部门'
      this.isEdit = true
      this.form = { ...row }
      this.dialogVisible = true
    },
    
    handleDelete(row) {
      this.$confirm('确定要删除该部门吗？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(async () => {
        try {
          await deleteDepartment(row.id)
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
            await updateDepartment(this.form.id, this.form)
            this.$message.success('更新成功')
          } else {
            await createDepartment(this.form)
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
        department: ''
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

