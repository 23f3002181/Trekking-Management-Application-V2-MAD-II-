import { createRouter, createWebHistory } from 'vue-router'

import Login from '../components/Login.vue'
import PublicDashboard from '../components/PublicDashboard.vue'
import StaffDashboard from '../components/StaffDashboard.vue'
import UserDashboard from '../components/UserDashboard.vue'

// Admin Components
import AdminDashboard from '../components/AdminDashboard.vue' // This is now your layout shell
import DashboardHome from '../components/admin/DashboardHome.vue'
import TreksManager from '../components/admin/TreksManager.vue'
import StaffManager from '../components/admin/StaffManager.vue'
import UserManager from '../components/admin/UserManager.vue'

const routes = [
  { path: '/', component: PublicDashboard },
  { path: '/login', component: Login },
  { path: '/staff-dashboard', component: StaffDashboard },
  { path: '/user-dashboard', component: UserDashboard },
  
  // Nested Admin Routes
  { 
    path: '/admin-dashboard', 
    component: AdminDashboard,
    children: [
      { path: '', redirect: '/admin-dashboard/home' }, // Default to home stats
      { path: 'home', component: DashboardHome },
      { path: 'treks', component: TreksManager },
      { path: 'staff', component: StaffManager },
      { path: 'users', component: UserManager }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router