<template>
  <div class="layout-container">
    <el-container>
      <!-- 侧边栏 -->
      <el-aside :width="isCollapse ? '64px' : '200px'">
        <div class="logo">
          <span v-if="!isCollapse">绩效管理</span>
          <span v-else>绩</span>
        </div>
        
        <el-menu
          :default-active="$route.path"
          :collapse="isCollapse"
          background-color="#304156"
          text-color="#bfcbd9"
          active-text-color="#409EFF"
          :unique-opened="true"
          router
        >
          <el-menu-item index="/home">
            <i class="el-icon-s-home"></i>
            <span slot="title">首页</span>
          </el-menu-item>
          
          <!-- 管理员菜单 -->
          <template v-if="isAdmin">
            <el-menu-item index="/department">
              <i class="el-icon-s-data"></i>
              <span slot="title">部门情况</span>
            </el-menu-item>
            
            <el-menu-item index="/employee">
              <i class="el-icon-user"></i>
              <span slot="title">员工管理</span>
            </el-menu-item>
            
            <el-menu-item index="/appraisal">
              <i class="el-icon-star-off"></i>
              <span slot="title">绩效考核</span>
            </el-menu-item>
            
            <el-menu-item index="/analytics">
              <i class="el-icon-data-line"></i>
              <span slot="title">绩效可视化</span>
            </el-menu-item>
          </template>
          
          <!-- 员工菜单 -->
          <template v-else>
            <el-menu-item index="/employee/info">
              <i class="el-icon-user"></i>
              <span slot="title">我的信息</span>
            </el-menu-item>
            
            <el-menu-item index="/employee/performance">
              <i class="el-icon-star-off"></i>
              <span slot="title">我的绩效</span>
            </el-menu-item>
          </template>
        </el-menu>
      </el-aside>
      
      <!-- 主内容区 -->
      <el-container>
        <!-- 顶部栏 -->
        <el-header>
          <div class="header-left">
            <i
              :class="isCollapse ? 'el-icon-s-unfold' : 'el-icon-s-fold'"
              @click="isCollapse = !isCollapse"
            ></i>
            <el-breadcrumb separator="/">
              <el-breadcrumb-item>{{ $route.meta.title || '首页' }}</el-breadcrumb-item>
            </el-breadcrumb>
          </div>
          
          <div class="header-right">
            <el-dropdown @command="handleCommand">
              <span class="user-info">
                <i class="el-icon-user-solid"></i>
                {{ userInfo.username || userInfo.employee_name || '用户' }}
                <i class="el-icon-arrow-down el-icon--right"></i>
              </span>
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item command="logout">
                  <i class="el-icon-switch-button"></i>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </el-header>
        
        <!-- 内容区 -->
        <el-main>
          <router-view />
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>
import { logout } from '@/api/auth'

export default {
  name: 'Layout',
  data() {
    return {
      isCollapse: false
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
  methods: {
    async handleCommand(command) {
      if (command === 'logout') {
        this.$confirm('确定要退出登录吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(async () => {
          try {
            await logout()
          } catch (error) {
            console.error('退出登录失败:', error)
          } finally {
            this.$store.dispatch('logout')
            this.$message.success('已退出登录')
            this.$router.push('/login')
          }
        }).catch(() => {})
      }
    }
  }
}
</script>

<style scoped>
.layout-container {
  height: 100vh;
}

.el-container {
  height: 100%;
}

.el-aside {
  background-color: #304156;
  transition: width 0.3s;
}

.logo {
  height: 60px;
  line-height: 60px;
  text-align: center;
  color: white;
  font-size: 20px;
  font-weight: bold;
  background-color: #2b3a4b;
}

.el-menu {
  border-right: none;
}

.el-header {
  background-color: white;
  box-shadow: 0 1px 4px rgba(0, 21, 41, 0.08);
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0 20px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.header-left i {
  font-size: 20px;
  cursor: pointer;
}

.header-right {
  display: flex;
  align-items: center;
}

.user-info {
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 5px;
}

.el-main {
  background-color: #f0f2f5;
  padding: 20px;
  overflow-y: auto;
}
</style>

