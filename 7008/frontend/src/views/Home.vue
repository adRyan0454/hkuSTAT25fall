<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="24">
        <el-card class="welcome-card">
          <h2>
            <i class="el-icon-s-home"></i>
            欢迎使用员工绩效考核管理系统
          </h2>
          <p class="welcome-text">
            您好，{{ userInfo.username || userInfo.yuangongxingming }}！
            {{ isAdmin ? '管理员' : '员工' }}
          </p>
          <p class="system-time">
            当前时间：{{ currentTime }}
          </p>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;" v-if="isAdmin">
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #409EFF;">
            <i class="el-icon-office-building"></i>
          </div>
          <div class="stat-info">
            <div class="stat-label">部门数量</div>
            <div class="stat-value">{{ stats.department }}</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #E6A23C;">
            <i class="el-icon-user"></i>
          </div>
          <div class="stat-info">
            <div class="stat-label">员工数量</div>
            <div class="stat-value">{{ stats.employee }}</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="8">
        <el-card class="stat-card">
          <div class="stat-icon" style="background: #F56C6C;">
            <i class="el-icon-star-off"></i>
          </div>
          <div class="stat-info">
            <div class="stat-label">考核记录</div>
            <div class="stat-value">{{ stats.appraisal }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row :gutter="20" style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <div slot="header">
            <i class="el-icon-info"></i>
            系统说明
          </div>
          <div class="system-intro">
            <h3>功能介绍</h3>
            <ul v-if="isAdmin">
              <li>部门管理：管理公司各部门信息</li>
              <li>岗位管理：管理各岗位职责和要求</li>
              <li>员工管理：管理员工基本信息</li>
              <li>绩效指标：设置和管理绩效考核指标</li>
              <li>绩效考核：对员工进行绩效评估</li>
              <li>公告信息：发布和管理系统公告</li>
            </ul>
            <ul v-else>
              <li>我的信息：查看和修改个人信息</li>
              <li>我的绩效：查看个人绩效考核记录</li>
              <li>公告查看：查看系统公告信息</li>
            </ul>
            
            <h3 style="margin-top: 20px;">技术栈</h3>
            <p>前端：Vue 2 + Element UI + Axios</p>
            <p>后端：FastAPI + SQLAlchemy + MySQL</p>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import { getAllDepartments } from '@/api/department'
import { getAllPositions } from '@/api/position'
import { getEmployeeList } from '@/api/employee'
import { getAppraisalList } from '@/api/appraisal'

export default {
  name: 'Home',
  data() {
    return {
      currentTime: '',
      stats: {
        department: 0,
        position: 0,
        employee: 0,
        appraisal: 0
      }
    }
  },
  computed: {
    userInfo() {
      return this.$store.getters.userInfo || {}
    },
    isAdmin() {
      return this.$store.getters.isAdmin
    }
  },
  mounted() {
    this.updateTime()
    setInterval(this.updateTime, 1000)
    
    if (this.isAdmin) {
      this.loadStats()
    }
  },
  methods: {
    updateTime() {
      const now = new Date()
      this.currentTime = now.toLocaleString('zh-CN')
    },
    
    async loadStats() {
      try {
        // 分别加载，避免一个失败影响全部
        
        // 加载部门数据
        try {
          const departmentRes = await getAllDepartments()
          if (Array.isArray(departmentRes.data)) {
            this.stats.department = departmentRes.data.length
          } else if (departmentRes.data && Array.isArray(departmentRes.data.list)) {
            this.stats.department = departmentRes.data.list.length
          }
        } catch (error) {
          console.error('加载部门数据失败:', error)
        }
        
        // 加载岗位数据
        try {
          const positionRes = await getAllPositions()
          if (Array.isArray(positionRes.data)) {
            this.stats.position = positionRes.data.length
          } else if (positionRes.data && Array.isArray(positionRes.data.list)) {
            this.stats.position = positionRes.data.list.length
          }
        } catch (error) {
          console.error('加载岗位数据失败:', error)
        }
        
        // 加载员工数据
        try {
          const employeeRes = await getEmployeeList({ page: 1, page_size: 1 })
          this.stats.employee = employeeRes.data?.total || 0
        } catch (error) {
          console.error('加载员工数据失败:', error)
        }
        
        // 加载绩效数据
        try {
          const appraisalRes = await getAppraisalList({ page: 1, page_size: 1 })
          this.stats.appraisal = appraisalRes.data?.total || 0
        } catch (error) {
          console.error('加载绩效数据失败:', error)
        }
      } catch (error) {
        console.error('加载统计数据失败:', error)
      }
    }
  }
}
</script>

<style scoped>
.home-container {
  padding: 20px;
}

.welcome-card {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.welcome-card h2 {
  margin: 0;
  font-size: 28px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.welcome-text {
  margin: 15px 0 10px;
  font-size: 18px;
}

.system-time {
  margin: 5px 0 0;
  font-size: 14px;
  opacity: 0.9;
}

.stat-card {
  display: flex;
  align-items: center;
}

.stat-card >>> .el-card__body {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 30px;
  color: white;
}

.stat-info {
  flex: 1;
}

.stat-label {
  color: #909399;
  font-size: 14px;
  margin-bottom: 5px;
}

.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #303133;
}

.system-intro {
  line-height: 1.8;
}

.system-intro h3 {
  margin-top: 0;
  color: #409EFF;
}

.system-intro ul {
  margin: 10px 0;
  padding-left: 20px;
}

.system-intro li {
  margin: 5px 0;
}
</style>

