<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">员工绩效考核管理系统</h2>
      
      <el-tabs v-model="loginType" class="login-tabs">
        <el-tab-pane label="管理员登录" name="admin">
          <el-form
            :model="adminForm"
            :rules="adminRules"
            ref="adminForm"
            class="login-form"
            @keyup.enter.native="handleAdminLogin"
          >
            <el-form-item prop="username">
              <el-input
                v-model="adminForm.username"
                placeholder="请输入管理员账号"
                prefix-icon="el-icon-user"
                clearable
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="adminForm.password"
                type="password"
                placeholder="请输入密码"
                prefix-icon="el-icon-lock"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                class="login-button"
                :loading="loading"
                @click="handleAdminLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        
        <el-tab-pane label="员工登录" name="employee">
          <el-form
            :model="employeeForm"
            :rules="employeeRules"
            ref="employeeForm"
            class="login-form"
            @keyup.enter.native="handleEmployeeLogin"
          >
            <el-form-item prop="employee_number">
              <el-input
                v-model="employeeForm.employee_number"
                placeholder="请输入员工工号"
                prefix-icon="el-icon-user"
                clearable
              />
            </el-form-item>
            <el-form-item prop="password">
              <el-input
                v-model="employeeForm.password"
                type="password"
                placeholder="请输入密码"
                prefix-icon="el-icon-lock"
                show-password
              />
            </el-form-item>
            <el-form-item>
              <el-button
                type="primary"
                class="login-button"
                :loading="loading"
                @click="handleEmployeeLogin"
              >
                登录
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      
      <div class="login-tips">
        <p>默认管理员账号：admin / admin</p>
        <p>员工账号：使用员工工号登录</p>
      </div>
    </div>
  </div>
</template>

<script>
import { adminLogin, employeeLogin } from '@/api/auth'

export default {
  name: 'Login',
  data() {
    return {
      loginType: 'admin',
      loading: false,
      adminForm: {
        username: '',
        password: ''
      },
      employeeForm: {
        employee_number: '',
        password: ''
      },
      adminRules: {
        username: [
          { required: true, message: '请输入管理员账号', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      },
      employeeRules: {
        employee_number: [
          { required: true, message: '请输入员工工号', trigger: 'blur' }
        ],
        password: [
          { required: true, message: '请输入密码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    handleAdminLogin() {
      this.$refs.adminForm.validate(async valid => {
        if (!valid) return
        
        this.loading = true
        try {
          const res = await adminLogin(this.adminForm)
          if (res.code === 200) {
            // 保存登录信息
            this.$store.dispatch('login', {
              token: res.data.token,
              user: res.data.user,
              role: '管理员'
            })
            
            this.$message.success('登录成功')
            this.$router.push('/home')
          }
        } catch (error) {
          console.error('登录失败:', error)
        } finally {
          this.loading = false
        }
      })
    },
    
    handleEmployeeLogin() {
      this.$refs.employeeForm.validate(async valid => {
        if (!valid) return
        
        this.loading = true
        try {
          const res = await employeeLogin(this.employeeForm)
          if (res.code === 200) {
            // 保存登录信息
            this.$store.dispatch('login', {
              token: res.data.token,
              user: res.data.employee,
              role: '员工'
            })
            
            this.$message.success('登录成功')
            this.$router.push('/home')
          }
        } catch (error) {
          console.error('登录失败:', error)
        } finally {
          this.loading = false
        }
      })
    }
  }
}
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-box {
  width: 420px;
  padding: 40px;
  background: white;
  border-radius: 10px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-title {
  text-align: center;
  margin-bottom: 30px;
  color: #333;
  font-size: 24px;
  font-weight: 600;
}

.login-tabs {
  margin-bottom: 20px;
}

.login-form {
  margin-top: 20px;
}

.login-button {
  width: 100%;
  margin-top: 10px;
}

.login-tips {
  margin-top: 20px;
  padding-top: 20px;
  border-top: 1px solid #eee;
  font-size: 12px;
  color: #999;
  text-align: center;
}

.login-tips p {
  margin: 5px 0;
}
</style>

