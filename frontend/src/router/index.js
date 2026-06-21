import { createRouter, createWebHistory } from 'vue-router'

import Login from '../components/Login.vue'
import AdminDashboard from '../components/AdminDashboard.vue'
import StaffDashboard from '../components/StaffDashboard.vue'
import UserDashboard from '../components/UserDashboard.vue'

const routes = [
  { path: '/', component: Login },
  { path: '/admin-dashboard', component: AdminDashboard },
  { path: '/staff-dashboard', component: StaffDashboard },
  { path: '/user-dashboard', component: UserDashboard }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router