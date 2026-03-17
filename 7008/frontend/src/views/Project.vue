<template>
  <div class="project-container">
    <el-card>
      <div slot="header" class="clearfix">
        <span>项目管理</span>
        <el-button 
          style="float: right; padding: 3px 10px" 
          type="primary" 
          size="small"
          @click="handleAdd"
        >
          新增项目
        </el-button>
      </div>

      <!-- 搜索表单 -->
      <el-form :inline="true" :model="queryParams" size="small">
        <el-form-item label="项目名称">
          <el-input 
            v-model="queryParams.name" 
            placeholder="请输入项目名称"
            clearable
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="getList">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>

      <!-- 表格 -->
      <el-table :data="projectList" border stripe style="margin-top: 20px">
        <el-table-column prop="id" label="ID" width="80" align="center" />
        <el-table-column prop="name" label="项目名称" min-width="150" />
        <el-table-column prop="description" label="项目描述" min-width="200" show-overflow-tooltip />
        <el-table-column prop="status" label="状态" width="100" align="center">
          <template slot-scope="scope">
            <el-tag :type="getStatusType(scope.row.status)">
              {{ getStatusText(scope.row.status) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="start_date" label="开始日期" width="120" align="center" />
        <el-table-column prop="end_date" label="结束日期" width="120" align="center" />
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template slot-scope="scope">
            <el-button size="mini" @click="handleEdit(scope.row)">编辑</el-button>
            <el-button 
              size="mini" 
              type="danger" 
              @click="handleDelete(scope.row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="queryParams.page"
        :page-sizes="[10, 20, 50, 100]"
        :page-size="queryParams.page_size"
        :total="total"
        layout="total, sizes, prev, pager, next, jumper"
        style="margin-top: 20px; text-align: right"
      />
    </el-card>

    <!-- 新增/编辑对话框 -->
    <el-dialog 
      :title="dialogTitle" 
      :visible.sync="dialogVisible"
      width="600px"
    >
      <el-form :model="form" :rules="rules" ref="form" label-width="100px">
        <el-form-item label="项目名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入项目名称" />
        </el-form-item>
        <el-form-item label="项目描述" prop="description">
          <el-input 
            v-model="form.description" 
            type="textarea" 
            :rows="3"
            placeholder="请输入项目描述"
          />
        </el-form-item>
        <el-form-item label="项目状态" prop="status">
          <el-select v-model="form.status" placeholder="请选择状态" style="width: 100%">
            <el-option label="规划中" value="planning" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
            <el-option label="已暂停" value="suspended" />
            <el-option label="已取消" value="cancelled" />
          </el-select>
        </el-form-item>
        <el-form-item label="开始日期" prop="start_date">
          <el-date-picker
            v-model="form.start_date"
            type="date"
            placeholder="选择开始日期"
            value-format="yyyy-MM-dd"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="结束日期" prop="end_date">
          <el-date-picker
            v-model="form.end_date"
            type="date"
            placeholder="选择结束日期"
            value-format="yyyy-MM-dd"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <el-button @click="dialogVisible = false">取 消</el-button>
        <el-button type="primary" @click="submitForm">确 定</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { 
  getProjectList, 
  createProject, 
  updateProject, 
  deleteProject 
} from '@/api/project'

export default {
  name: 'Project',
  data() {
    return {
      // 查询参数
      queryParams: {
        page: 1,
        page_size: 10,
        name: ''
      },
      // 项目列表
      projectList: [],
      // 总数
      total: 0,
      // 对话框
      dialogVisible: false,
      dialogTitle: '新增项目',
      // 表单
      form: {
        name: '',
        description: '',
        status: 'planning',
        start_date: '',
        end_date: ''
      },
      // 表单验证
      rules: {
        name: [
          { required: true, message: '请输入项目名称', trigger: 'blur' }
        ],
        status: [
          { required: true, message: '请选择项目状态', trigger: 'change' }
        ]
      }
    }
  },
  created() {
    this.getList()
  },
  methods: {
    // 获取列表
    async getList() {
      try {
        const { data } = await getProjectList(this.queryParams)
        if (data.code === 200) {
          this.projectList = data.data.list || []
          this.total = data.data.total || 0
        }
      } catch (error) {
        this.$message.error('获取项目列表失败')
      }
    },
    
    // 重置查询
    resetQuery() {
      this.queryParams = {
        page: 1,
        page_size: 10,
        name: ''
      }
      this.getList()
    },
    
    // 新增
    handleAdd() {
      this.form = {
        name: '',
        description: '',
        status: 'planning',
        start_date: '',
        end_date: ''
      }
      this.dialogTitle = '新增项目'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form && this.$refs.form.clearValidate()
      })
    },
    
    // 编辑
    handleEdit(row) {
      this.form = { ...row }
      this.dialogTitle = '编辑项目'
      this.dialogVisible = true
      this.$nextTick(() => {
        this.$refs.form && this.$refs.form.clearValidate()
      })
    },
    
    // 删除
    async handleDelete(row) {
      try {
        await this.$confirm('确认删除该项目？', '提示', { 
          type: 'warning' 
        })
        const { data } = await deleteProject(row.id)
        if (data.code === 200) {
          this.$message.success('删除成功')
          this.getList()
        }
      } catch (error) {
        if (error !== 'cancel') {
          this.$message.error('删除失败')
        }
      }
    },
    
    // 提交表单
    submitForm() {
      this.$refs.form.validate(async (valid) => {
        if (!valid) return
        
        try {
          let result
          if (this.form.id) {
            result = await updateProject(this.form.id, this.form)
          } else {
            result = await createProject(this.form)
          }
          
          if (result.data.code === 200) {
            this.$message.success('操作成功')
            this.dialogVisible = false
            this.getList()
          }
        } catch (error) {
          this.$message.error('操作失败')
        }
      })
    },
    
    // 分页
    handleSizeChange(val) {
      this.queryParams.page_size = val
      this.getList()
    },
    handleCurrentChange(val) {
      this.queryParams.page = val
      this.getList()
    },
    
    // 状态显示
    getStatusText(status) {
      const statusMap = {
        'planning': '规划中',
        'in_progress': '进行中',
        'completed': '已完成',
        'suspended': '已暂停',
        'cancelled': '已取消'
      }
      return statusMap[status] || status
    },
    
    getStatusType(status) {
      const typeMap = {
        'planning': 'info',
        'in_progress': 'primary',
        'completed': 'success',
        'suspended': 'warning',
        'cancelled': 'danger'
      }
      return typeMap[status] || 'info'
    }
  }
}
</script>

<style scoped>
.project-container {
  padding: 20px;
}

.clearfix:before,
.clearfix:after {
  display: table;
  content: "";
}

.clearfix:after {
  clear: both;
}
</style>

