<template>
  <div class="d-flex" style="min-height: 100vh; background-color: #f8f9fa;">

    <div class="bg-light border-end shadow-sm d-flex flex-column" style="width: 220px;">
      <div class="p-3 text-center border-bottom">
        <router-link to="/">
          <span class="glyphicon glyphicon-th-list"><i class="bi bi-list"></i></span>
        </router-link>
      </div>

      <div class="nav flex-column p-3 flex-grow-1">
        <router-link to="/user-dashboard/home" class="nav-link mb-1 text-dark px-3 py-2 rounded-3"
          active-class="active">
          <span class="me-2"><i class="bi bi-house-door-fill me-2"></i></span> Dashboard
        </router-link>

        <router-link to="/user-dashboard/browse" class="nav-link mb-1 text-dark px-3 py-2 rounded-3"
          active-class="active">
          <span class="me-2"><i class="bi bi-backpack2 me-2"></i></span> Browse Treks
        </router-link>

        <router-link to="/user-dashboard/bookings" class="nav-link mb-1 text-dark px-3 py-2 rounded-3"
          active-class="active">
          <span class="me-2"><i class="bi bi-calendar-check me-2"></i></span> My Bookings
        </router-link>

        <router-link to="/user-dashboard/history" class="nav-link mb-1 text-dark px-3 py-2 rounded-3"
          active-class="active">
          <span class="me-2"><i class="bi bi-clock-history me-2"></i></span> History
        </router-link>

        <router-link to="/user-dashboard/profile" class="nav-link mb-1 text-dark px-3 py-2 rounded-3"
          active-class="active">
          <span class="me-2"><i class="bi bi-person me-2"></i></span> Profile
        </router-link>

        <hr class="my-2 text-muted">

        <button class="btn btn-light text-start text-danger fw-bold px-3 py-2 mt-1 rounded-3" @click="logout"
          style="border: none;">
          <span class="me-2"><i class="bi bi-box-arrow-right me-2"></i></span> Logout
        </button>
      </div>
    </div>

    <div class="flex-grow-1 d-flex flex-column">

      <div class="bg-light border-bottom px-4 py-2 d-flex justify-content-between align-items-center">
        <h4 class="fw-bold mb-0 py-0 fs-3 text-black">
          Trekking Management Application
        </h4>
        <div class="dropdown">
          <button class="btn bg-white border shadow-sm dropdown-toggle d-flex align-items-center rounded-pill px-4 py-1"
            type="button" data-bs-toggle="dropdown">
            <i class="bi bi-person-circle fs-5 me-2"></i>
            <span class="fw-normal fs-5">{{ fullName }}</span>
          </button>

          <ul class="dropdown-menu dropdown-menu-end shadow-sm border-0 mt-2">
            <li>
              <router-link to="/user-dashboard/profile" class="dropdown-item py-2">My Profile</router-link>
            </li>
            <li>
              <hr class="dropdown-divider">
            </li>
            <li>
              <button class="dropdown-item text-danger fw-bold py-2" @click="logout">Logout</button>
            </li>
          </ul>
        </div>
      </div>

      <div class="p-5 bg-white flex-grow-1 overflow-auto">
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

      }
    },
    logout() {
      Swal.fire({
        title: 'Ready to leave?',
        text: 'You will need to log in again to access your dashboard.',
        icon: 'info',
        showCancelButton: true,
        confirmButtonColor: '#dc3545',
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

.nav-link {
  transition: all 0.2s ease-in-out;
  font-weight: 500;
}
.nav-link:hover:not(.active) {
  background-color: #f5f6fa;
}

.nav-link.active {
  background: #dce8ff;
  color: #0d6efd !important;
  font-weight: 600;
  border-radius: 10px;
}

.nav-link:hover {
  background: #eef3ff;
}
</style>