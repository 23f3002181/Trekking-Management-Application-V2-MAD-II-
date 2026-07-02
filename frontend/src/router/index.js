import { createRouter, createWebHistory } from 'vue-router'

import Login from '../components/Login.vue'
import PublicDashboard from '../components/PublicDashboard.vue'

// Admin Components
import AdminDashboard from '../components/AdminDashboard.vue'
import DashboardHome from '../components/admin/DashboardHome.vue'
import TreksManager from '../components/admin/TreksManager.vue'
import StaffManager from '../components/admin/StaffManager.vue'
import UserManager from '../components/admin/UserManager.vue'
import TrekHistory from '../components/admin/TrekHistory.vue'

// User Components 
import UserDashboard from '../components/UserDashboard.vue'
import UserHome from '../components/user/UserHome.vue'
import UserBrowse from '../components/user/UserBrowse.vue'
import UserHistory from '../components/user/UserHistory.vue'
import UserProfile from '../components/user/UserProfile.vue'
import UserBookings from '../components/user/UserBookings.vue'

// Staff Components
import StaffDashboard from '../components/StaffDashboard.vue'
import StaffHome from '../components/staff/StaffHome.vue'
import StaffManageTrek from '../components/staff/StaffManageTrek.vue'

const routes = [
  { path: '/', component: PublicDashboard },
  { path: '/login', component: Login },

  // Nested User Routes
  {
    path: '/user-dashboard',
    component: UserDashboard,
    children: [
      { path: '', redirect: '/user-dashboard/home' },
      { path: 'home', component: UserHome },
      { path: 'browse', component: UserBrowse },
      { path: 'bookings', component: UserBookings },
      { path: 'history', component: UserHistory },
      { path: 'profile', component: UserProfile }
    ]
  },

  // Nested Admin Routes
  {
    path: '/admin-dashboard',
    component: AdminDashboard,
    children: [
      { path: '', redirect: '/admin-dashboard/home' },
      { path: 'home', component: DashboardHome },
      { path: 'treks', component: TreksManager },
      { path: 'staff', component: StaffManager },
      { path: 'users', component: UserManager },
      { path: 'history', component: TrekHistory }
    ]
  },

  // Nested Staff Routes
  {
    path: '/staff-dashboard',
    component: StaffDashboard,
    children: [
      { path: '', redirect: '/staff-dashboard/home' },
      { path: 'home', component: StaffHome },
      { path: 'manage/:id', component: StaffManageTrek }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router