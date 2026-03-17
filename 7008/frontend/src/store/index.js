import Vue from 'vue'
import Vuex from 'vuex'
import Cookies from 'js-cookie'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    token: Cookies.get('token') || '',
    userInfo: Cookies.get('userInfo') ? JSON.parse(Cookies.get('userInfo')) : null,
    userRole: Cookies.get('userRole') || ''
  },
  mutations: {
    SET_TOKEN(state, token) {
      state.token = token
      Cookies.set('token', token, { expires: 7 })
    },
    SET_USER_INFO(state, userInfo) {
      state.userInfo = userInfo
      Cookies.set('userInfo', JSON.stringify(userInfo), { expires: 7 })
    },
    SET_USER_ROLE(state, role) {
      state.userRole = role
      Cookies.set('userRole', role, { expires: 7 })
    },
    LOGOUT(state) {
      state.token = ''
      state.userInfo = null
      state.userRole = ''
      Cookies.remove('token')
      Cookies.remove('userInfo')
      Cookies.remove('userRole')
    }
  },
  actions: {
    login({ commit }, { token, user, role }) {
      commit('SET_TOKEN', token)
      commit('SET_USER_INFO', user)
      commit('SET_USER_ROLE', role)
    },
    logout({ commit }) {
      commit('LOGOUT')
    }
  },
  getters: {
    isLoggedIn: state => !!state.token,
    userInfo: state => state.userInfo,
    userRole: state => state.userRole,
    isAdmin: state => state.userRole === '管理员'
  }
})

