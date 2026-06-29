<template>
  <div class="d-flex" style="min-height: 100vh; background-color: #f8f9fa;">
    
    <div class="bg-white border-end d-flex flex-column" style="width: 260px;">
      
      <div class="p-4 border-bottom text-center">
        <h5 class="text-primary fw-bold mb-0">Trekking App</h5>
      </div>
      
      <div class="nav flex-column p-3 flex-grow-1">
        <router-link to="/user-dashboard/home" class="nav-link mb-2 text-dark px-3 py-2 rounded-3" active-class="active">
          <span class="me-2">🏠</span> Dashboard
        </router-link>
        
        <router-link to="/user-dashboard/browse" class="nav-link mb-2 text-dark px-3 py-2 rounded-3" active-class="active">
          <span class="me-2">⛰️</span> Browse Treks
        </router-link>
        
        <router-link to="/user-dashboard/bookings" class="nav-link mb-2 text-dark px-3 py-2 rounded-3" active-class="active">
          <span class="me-2">📅</span> My Bookings
        </router-link>
        
        <router-link to="/user-dashboard/history" class="nav-link mb-2 text-dark px-3 py-2 rounded-3" active-class="active">
          <span class="me-2">🧭</span> History
        </router-link>
        
        <router-link to="/user-dashboard/profile" class="nav-link mb-2 text-dark px-3 py-2 rounded-3" active-class="active">
          <span class="me-2">👤</span> Profile
        </router-link>

        <hr class="my-2 text-muted">

        <button class="btn btn-light text-start text-danger fw-bold px-3 py-2 mt-1 rounded-3" @click="logout" style="border: none;">
          <span class="me-2">🚪</span> Logout
        </button>
      </div>
    </div>

    <div class="flex-grow-1 d-flex flex-column">
      
      <div class="bg-white border-bottom px-4 py-3 d-flex justify-content-end align-items-center">
        <div class="dropdown">
          <button class="btn btn-light border dropdown-toggle d-flex align-items-center rounded-pill px-3" type="button" data-bs-toggle="dropdown">
            <span class="me-2">👤</span> {{ fullName }}
          </button>
          
          <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0 mt-2">
            <li>
              <router-link to="/user-dashboard/profile" class="dropdown-item py-2">My Profile</router-link>
            </li>
            <li><hr class="dropdown-divider"></li>
            <li>
              <button class="dropdown-item text-danger fw-bold py-2" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>

      <div class="p-4 flex-grow-1 overflow-auto">
        <router-view></router-view>
      </div>
      
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
  data() {
    return {
      fullName: 'Trekker'
    }
  },
  mounted() {
    this.fetchProfileName()
  },
  methods: {
    async fetchProfileName() {
      try {
        const res = await axios.get('http://127.0.0.1:5000/api/user/profile')
        if (res.data.full_name) {
          this.fullName = res.data.full_name
        }
      } catch (err) {
        // Fallback to default if API fails
      }
    },
    logout() {
      Swal.fire({
        title: 'Ready to leave?',
        text: 'You will need to log in again to access your dashboard.',
        icon: 'info',
        showCancelButton: true,
        confirmButtonColor: '#dc3545', // Danger Red
        cancelButtonColor: '#6c757d',
        confirmButtonText: 'Yes, log me out'
      }).then((result) => {
        if (result.isConfirmed) {
          localStorage.removeItem('authToken')
          this.$router.push('/')
        }
      });
    }
  }
}
</script>

<style scoped>
/* Smooth hover transitions */
.nav-link {
  transition: all 0.2s ease-in-out;
  font-weight: 500;
}

/* Subtle hover effect for non-active links */
.nav-link:hover:not(.active) {
  background-color: #f8f9fa;
}

/* The exact styling for the active state to match your mockup */
.nav-link.active {
  background-color: #e9efff !important; /* Very light primary blue */
  color: #0d6efd !important; /* Bootstrap primary text */
  font-weight: 700;
}
</style>