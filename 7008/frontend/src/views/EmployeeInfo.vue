<template>
  <div class="page-container">
    <el-card>
      <div slot="header">
        <i class="el-icon-user"></i> 我的信息
      </div>
      
      <div v-if="userInfo" class="info-container">
        <el-descriptions title="个人信息" :column="2" border>
          <el-descriptions-item label="员工工号">{{ userInfo.employee_number }}</el-descriptions-item>
          <el-descriptions-item label="员工姓名">{{ userInfo.employee_name }}</el-descriptions-item>
          <el-descriptions-item label="年龄">{{ userInfo.age }}</el-descriptions-item>
          <el-descriptions-item label="最高学历">{{ userInfo.education }}</el-descriptions-item>
          <el-descriptions-item label="所属部门">{{ userInfo.department }}</el-descriptions-item>
          <el-descriptions-item label="领导工号">{{ userInfo.supervisor_number }}</el-descriptions-item>
          <el-descriptions-item label="职级">{{ userInfo.job_level }}</el-descriptions-item>
          <el-descriptions-item label="入职时间">{{ userInfo.join_date }}</el-descriptions-item>
        </el-descriptions>
        
        <div style="margin-top: 20px;">
          <el-button type="primary" @click="dialogVisible = true">修改密码</el-button>
        </div>
      </div>
    </el-card>
    
    <!-- 修改密码对话框 -->
    <el-dialog
      title="修改密码"
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
        <el-form-item label="新密码" prop="password">
          <el-input v-model="form.password" type="password" placeholder="请输入新密码" />
        </el-form-item>
        
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="form.confirmPassword" type="password" placeholder="请再次输入新密码" />
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
import { getEmployee, updateEmployee } from '@/api/employee'

export default {
  name: 'EmployeeInfo',
  data() {
    const validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.form.password) {
        callback(new Error('两次输入的密码不一致'))
      } else {
        callback()
      }
    }
    
    return {
      userInfo: null,
      dialogVisible: false,
      submitLoading: false,
      form: {
        password: '',
        confirmPassword: ''
      },
      rules: {
        password: [
          { required: true, message: '请输入新密码', trigger: 'blur' },
          { min: 6, message: '密码长度至少6位', trigger: 'blur' }
        ],
        confirmPassword: [
          { required: true, message: '请再次输入新密码', trigger: 'blur' },
          { validator: validateConfirmPassword, trigger: 'blur' }
        ]
      }
    }
  },
  mounted() {
    this.loadUserInfo()
  },
  methods: {
    async loadUserInfo() {
      try {
        const storeUserInfo = this.$store.getters.userInfo
        if (storeUserInfo && storeUserInfo.id) {
          const res = await getEmployee(storeUserInfo.id)
          this.userInfo = res.data
        }
      } catch (error) {
        console.error('加载用户信息失败:', error)
      }
    },
    
    handleSubmit() {
      this.$refs.form.validate(async valid => {
        if (!valid) return
        
        this.submitLoading = true
        try {
          await updateEmployee(this.userInfo.id, { password: this.form.password })
          this.$message.success('密码修改成功')
          this.dialogVisible = false
        } catch (error) {
          console.error('修改密码失败:', error)
        } finally {
          this.submitLoading = false
        }
      })
    },
    
    resetForm() {
      this.form = {
        password: '',
        confirmPassword: ''
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

.info-container {
  padding: 20px;
}
</style>

